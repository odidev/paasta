#!/usr/bin/env python
# Copyright 2015-2016 Yelp Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# PYTHON_ARGCOMPLETE_OK
"""A command line tool for viewing information from the PaaSTA stack."""
import argparse
import logging
import os
import pkgutil
import subprocess
import sys
import threading
import warnings

import argcomplete
import pkg_resources

from paasta_tools.cli import cmds


TLS = threading.local()


def to_bytes(obj) -> bytes:
    if isinstance(obj, bytes):
        return obj
    elif isinstance(obj, str):
        return obj.encode("UTF-8")
    else:
        return str(obj).encode("UTF-8")


def paasta_print(*args, **kwargs):
    f = kwargs.pop("file", sys.stdout) or sys.stdout
    f = getattr(TLS, "paasta_print_file", f) or f
    buf = getattr(f, "buffer", None)
    # Here we're assuming that the file object works with strings and its
    # `buffer` works with bytes. So, if the file object doesn't have `buffer`,
    # we output via the file object itself using strings.
    if buf is not None:
        f = buf
        obj_to_arg = to_bytes
    else:

        def obj_to_arg(o) -> str:
            return to_bytes(o).decode("UTF-8", errors="ignore")

    end = obj_to_arg(kwargs.pop("end", "\n"))
    sep = obj_to_arg(kwargs.pop("sep", " "))
    assert not kwargs, kwargs
    to_print = sep.join(obj_to_arg(x) for x in args) + end
    f.write(to_print)
    f.flush()


def paasta_commands_dir(pkg):
    """Return the list of modules in a python package (a module with a
    __init__.py file.)

    :return: a list of strings such as `['list', 'check']` that correspond to
             the module names in the package.
    """
    for _, module_name, _ in pkgutil.walk_packages(pkg.__path__):
        yield module_name


def load_method(module_name, method_name):
    """Return a function given a module and method name.

    :param module_name: a string
    :param method_name: a string
    :return: a function
    """
    module = __import__(module_name, fromlist=[method_name])
    method = getattr(module, method_name)
    return method


class PrintsHelpOnErrorArgumentParser(argparse.ArgumentParser):
    """Overriding the error method allows us to print the whole help page,
    otherwise the python arg parser prints a not-so-useful usage message that
    is way too terse"""

    def error(self, message):
        paasta_print("Argument parse error: %s" % message)
        self.print_help()
        sys.exit(1)


def list_external_commands():
    p = subprocess.check_output(["/bin/bash", "-p", "-c", "compgen -A command paasta-"])
    lines = p.decode("utf-8").strip().split("\n")
    return {l.replace("paasta-", "", 1) for l in lines}


def calling_external_command():
    if len(sys.argv) > 1:
        return sys.argv[1] in list_external_commands()
    else:
        return False


def get_command_help(command):
    return f"(run 'paasta {command} -h' for usage)"


def external_commands_items():
    for command in list_external_commands():
        command_help = get_command_help(command)
        yield command, command_help


def exec_subcommand(argv):
    command = sys.argv[1]
    os.execlp(f"paasta-{command}", *argv[1:])


def add_subparser(command, subparsers):
    """Given a command name, paasta_cmd, execute the add_subparser method
    implemented in paasta_cmd.py.

    Each paasta client command must implement a method called add_subparser.
    This allows the client to dynamically add subparsers to its subparser, which
    provides the benefits of argcomplete/argparse but gets it done in a modular
    fashion.

    :param command: a simple string - e.g. 'list'
    :param subparsers: an ArgumentParser object"""
    module_name = "paasta_tools.cli.cmds.%s" % command
    add_subparser_fn = load_method(module_name, "add_subparser")
    add_subparser_fn(subparsers)


def get_argparser():
    parser = PrintsHelpOnErrorArgumentParser(
        description=(
            "The PaaSTA command line tool. The 'paasta' command is the entry point "
            "to multiple subcommands, see below.\n\n"
            "You can see more help for individual commands by appending them with '--help', "
            "for example, 'paasta status --help' or see the man page with 'man paasta status'."
        ),
        epilog=(
            "The 'paasta' command line tool is designed to be used by humans, and therefore has "
            "command line completion for almost all options and uses pretty formatting when "
            "possible."
        ),
        # Suppressing usage prevents it from being printed twice upon print_help
        usage=argparse.SUPPRESS,
    )

    # http://stackoverflow.com/a/8521644/812183
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="paasta-tools {}".format(
            pkg_resources.get_distribution("paasta-tools").version
        ),
    )

    subparsers = parser.add_subparsers(
        help="[-h, --help] for subcommand help", dest="command"
    )
    subparsers.required = True

    # Adding a separate help subparser allows us to respond to "help" without --help
    help_parser = subparsers.add_parser("help", add_help=False)
    help_parser.set_defaults(command=None)

    for command in sorted(paasta_commands_dir(cmds)):
        add_subparser(command, subparsers)

    for command, command_help in external_commands_items():
        subparsers.add_parser(command, help=command_help)

    return parser


def parse_args(argv):
    """Initialize autocompletion and configure the argument parser.

    :return: an argparse.Namespace object mapping parameter names to the inputs
             from sys.argv
    """
    parser = get_argparser()
    argcomplete.autocomplete(parser)

    return parser.parse_args(argv), parser


def main(argv=None):
    """Perform a paasta call. Read args from sys.argv and pass parsed args onto
    appropriate command in paasta_cli/cmds directory.

    Ensure we kill any child pids before we quit
    """
    logging.basicConfig()
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # if we are an external command, we need to exec out early.
    # The reason we exec out early is so we don't bother trying to parse
    # "foreign" arguments, which would cause a stack trace.
    if calling_external_command():
        exec_subcommand(sys.argv)

    try:
        args, parser = parse_args(argv)
        if args.command is None:
            parser.print_help()
            return_code = 0
        else:
            return_code = args.command(args)
    except KeyboardInterrupt:
        return_code = 1
    sys.exit(return_code)


if __name__ == "__main__":
    main()
