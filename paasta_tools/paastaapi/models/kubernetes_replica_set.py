# coding: utf-8

"""
    Paasta API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from paasta_tools.paastaapi.configuration import Configuration


class KubernetesReplicaSet(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'create_timestamp': 'float',
        'name': 'str',
        'ready_replicas': 'int',
        'replicas': 'int'
    }

    attribute_map = {
        'create_timestamp': 'create_timestamp',
        'name': 'name',
        'ready_replicas': 'ready_replicas',
        'replicas': 'replicas'
    }

    def __init__(self, create_timestamp=None, name=None, ready_replicas=None, replicas=None, local_vars_configuration=None):  # noqa: E501
        """KubernetesReplicaSet - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._create_timestamp = None
        self._name = None
        self._ready_replicas = None
        self._replicas = None
        self.discriminator = None

        if create_timestamp is not None:
            self.create_timestamp = create_timestamp
        if name is not None:
            self.name = name
        if ready_replicas is not None:
            self.ready_replicas = ready_replicas
        if replicas is not None:
            self.replicas = replicas

    @property
    def create_timestamp(self):
        """Gets the create_timestamp of this KubernetesReplicaSet.  # noqa: E501

        Time at which the replicaset was created  # noqa: E501

        :return: The create_timestamp of this KubernetesReplicaSet.  # noqa: E501
        :rtype: float
        """
        return self._create_timestamp

    @create_timestamp.setter
    def create_timestamp(self, create_timestamp):
        """Sets the create_timestamp of this KubernetesReplicaSet.

        Time at which the replicaset was created  # noqa: E501

        :param create_timestamp: The create_timestamp of this KubernetesReplicaSet.  # noqa: E501
        :type create_timestamp: float
        """

        self._create_timestamp = create_timestamp

    @property
    def name(self):
        """Gets the name of this KubernetesReplicaSet.  # noqa: E501

        name of the replicaset in Kubernetes  # noqa: E501

        :return: The name of this KubernetesReplicaSet.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this KubernetesReplicaSet.

        name of the replicaset in Kubernetes  # noqa: E501

        :param name: The name of this KubernetesReplicaSet.  # noqa: E501
        :type name: str
        """

        self._name = name

    @property
    def ready_replicas(self):
        """Gets the ready_replicas of this KubernetesReplicaSet.  # noqa: E501

        number of ready replicas for the replicaset  # noqa: E501

        :return: The ready_replicas of this KubernetesReplicaSet.  # noqa: E501
        :rtype: int
        """
        return self._ready_replicas

    @ready_replicas.setter
    def ready_replicas(self, ready_replicas):
        """Sets the ready_replicas of this KubernetesReplicaSet.

        number of ready replicas for the replicaset  # noqa: E501

        :param ready_replicas: The ready_replicas of this KubernetesReplicaSet.  # noqa: E501
        :type ready_replicas: int
        """

        self._ready_replicas = ready_replicas

    @property
    def replicas(self):
        """Gets the replicas of this KubernetesReplicaSet.  # noqa: E501

        number of desired replicas for the replicaset  # noqa: E501

        :return: The replicas of this KubernetesReplicaSet.  # noqa: E501
        :rtype: int
        """
        return self._replicas

    @replicas.setter
    def replicas(self, replicas):
        """Sets the replicas of this KubernetesReplicaSet.

        number of desired replicas for the replicaset  # noqa: E501

        :param replicas: The replicas of this KubernetesReplicaSet.  # noqa: E501
        :type replicas: int
        """

        self._replicas = replicas

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, KubernetesReplicaSet):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, KubernetesReplicaSet):
            return True

        return self.to_dict() != other.to_dict()
