"""
    rbteam.config
    ~~~~~~~~~~~~~

    This module describes configuration handling for Flask application.

    More info in documentation at https://docs.radiobretzel.org
"""

import os
import yaml

from flask import Config

from rbteam.errors import ConfigurationError
from rbteam.utils.formats import get_prefixed_keys


class RBCoreConfig(Config):
    """Main configuration class. This class will be used normally by Flask and
        as a singleton by our app, in order to prevent any unexpected behaviour
    """

    __DEFAULT = {
        'SITE_NAME': 'Radio Bretzel Core',
        'OBJECTS_NAME_PREFIX': 'rbteam_',

        'IS_CONTAINER': False,

        'DOCKER_URL': 'unix://var/run/docker.sock',
        'DOCKER_VERSION': 'auto',

        'MONGO_HOST': 'localhost',
        'MONGO_DATABASE': 'rbteam',

        'SOURCE_TYPE': 'docker',
        # DockerSource relative configuration
        'SOURCE_CONTAINER_IMAGE': 'registry.radiobretzel.org/sources/rb-src-liquidsoap',
        'SOURCE_CONTAINER_IMAGE_TAG': 'latest',
        'SOURCE_NETWORK': False,
        'SOURCE_NETWORK_NAME': 'sources',

        'STREAM_HOST': 'None',
        'STREAM_SOURCE_PASSWD': 'None',
    }

    __DEVELOPMENT = {
        'DEBUG': True,
        'ASSETS_DEBUG': True,
        'WTF_CSRF_ENABLED': False,

        'SOURCE_CONTAINER_IMAGE_TAG': 'develop',
    }

    __TEST = {
        'TESTING': True,
        'WTF_CSRF_ENABLED':  False,

        'OBJECTS_NAME_PREFIX': 'radiobretzel_tests_',

        'MONGO_HOST': 'localhost',
        'MONGO_DATABASE': 'rbteam_test',

        'STREAM_HOST': 'None',
        'STREAM_SOURCE_PASSWD': 'None',
    }

    __PRODUCTION = {}

    __locked_config = [

    ]


    def load(self, environment='development', config_file=None, **extra_config):
        """Load configuration from files, environment, and dict"""

        self.from_mapping(self.__DEFAULT)

        if environment == 'production':
            self.from_mapping(self.__PRODUCTION)
        elif environment == 'test':
            self.from_mapping(self.__TEST)
        else:
            self.from_mapping(self.__DEVELOPMENT)

        if config_file or os.environ.get('RBTEAM_CONFIG_FILE'):
            self.from_yaml(config_file)

        env_variables = get_prefixed_keys(os.environ, 'RBTEAM_', lowercase=False).get('matching')
        if env_variables:
            env_variables.pop('RBTEAM_CONFIG_FILE', None)
            self.update(env_variables)

        if extra_config:
            for item in extra_config:
                if item not in self.__locked_config:
                    config = {item.upper(): extra_config[item]}
                    self.update(config)


    def from_yaml(self, filename, silent=False):
        """Load configuration from the given YAML filename and add it to the
        current app configuration.
        """
        if not os.path.isabs(filename):
            filename = os.path.join(self.root_path, filename)
        try:
            with open(filename, 'r') as file:
                yaml_object = yaml.load(file)
        except Exception as err:
            if not silent:
                raise ConfigurationError("Couldn't parse config file : " + str(err))
        config = {}
        for key, value in yaml_object.items():
            key_ = key.upper()
            config[key_] = value

        return self.from_mapping(config)
