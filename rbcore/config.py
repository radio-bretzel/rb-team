import os
import yaml

from flask import Config
from flask import current_app as app

from .errors import ConfigurationError, RadioBretzelException
from .utils.formats import get_prefixed_keys

def get_config():
    try:
        return app.config
    except:
        raise RadioBretzelException("Couldn't get config - is app instanciated ?")

class RBCoreConfig(Config):
    """Main configuration class. This class will be used normally by Flask and
        as a singleton by our app, in order to prevent any unexpected behaviour
    """


    __locked_config = [

    ]


    def load(self, environment='development', config_file=None, debug=False, **config):
        """Load configuration from files, environment, and dict"""

        self.from_mapping(_default)

        if environment == 'production':
            self.from_mapping(_production)
        elif environment == 'test':
            self.from_mapping(_test)
        else:
            self.from_mapping(_development)

        if config_file or os.environ.get('RBCORE_CONFIG_FILE'):
            yaml_config = self.from_yaml(config_file)
            self.config_file = config_file

        env_variables = get_prefixed_keys(os.environ, 'RBCORE_', lowercase=False).get('matching')
        if env_variables:
            env_variables.pop('RBCORE_CONFIG_FILE', None)
            self.update(env_variables)

        if config:
            for item in config:
                if item not in self.__locked_config:
                    c = { item.upper(): config[item] }
                    self.update(c)


    def from_yaml(self, filename, silent=False):
        if not os.path.isabs(filename):
            filename = os.os.path.join(self.root_path, filename)
        try:
            with open(filename, 'r') as file:
                yaml_object = yaml.load(file)
        except yaml.YAMLError as e:
            if not silent:
                raise ConfigurationError("Couldn't parse config file : " + str(e))
        except Exception as e:
            if not silent:
                raise e
        config = {}
        for k,v in config.items():
            key = k.upper()
            config[key] = v

        return self.from_mapping(config)



_default = {
    'SITE_NAME': 'Radio Bretzel Core',
    'OBJECTS_NAME_PREFIX': 'rbcore_',

    'IS_CONTAINER': False,

    'DOCKER_URL': 'unix://var/run/docker.sock',
    'DOCKER_VERSION': 'auto',

    'MONGO_HOST': 'localhost',
    'MONGO_DATABASE': 'rbcore',

    'SOURCE_TYPE': 'docker',
    # DockerSource relative configuration
    'SOURCE_CONTAINER_IMAGE': 'registry.radiobretzel.org/sources/rb-src-liquidsoap',
    'SOURCE_CONTAINER_IMAGE_TAG': 'latest',
    'SOURCE_NETWORK': False,
    'SOURCE_NETWORK_NAME': 'sources',

    'STREAM_HOST': 'None',
    'STREAM_SOURCE_PASSWD': 'None',
}

_development = {
    'DEBUG': True,
    'ASSETS_DEBUG': True,
    'WTF_CSRF_ENABLED': False,

    'SOURCE_CONTAINER_IMAGE_TAG': 'develop',
}

_test = {
    'TESTING': True,
    'WTF_CSRF_ENABLED':  False,

    'OBJECTS_NAME_PREFIX': 'radiobretzel_tests_',

    'MONGO_HOST': 'localhost',
    'MONGO_DATABASE': 'rbcore_test',

    'STREAM_HOST': 'None',
    'STREAM_SOURCE_PASSWD': 'None',
}

_production = {}
