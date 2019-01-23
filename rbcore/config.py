from flask import Config
from os import path
import yaml

from rbcore.errors import ConfigurationError, RadioBretzelException
from rbcore.utils.formats import get_prefixed_keys

def get_config():
    try:
        return app.config
    except:
        raise RadioBretzelException("Couldn't get config - is app instanciated ?")

class RBCoreConfig(Config):
    """Main configuration class. This class will be used normally by Flask and  as a singleton by our app, in order to prevent any unexpected behaviour
    """


    def load(self, environment='development', config_file='none', debug=False, **config):
        """Load configuration from files, environment, and dict"""
        if environment == 'production':
            self.from_mapping(production)
        elif environment == 'test':
            self.from_mapping(test)
        else:
            self.from_mapping(development)

        # self.from_mapping(self.from_yaml(config_file))

        # env_variables = get_prefixed_keys(os.environ, 'RBCORE_', lowercase=False).get('matching')
        # self.update(env_variables)


    def from_yaml(self, filename, silent=False):
        filename = os.path.join(self.root_path, filename)
        try:
            with open(filename, 'r') as file:
                config = yaml.load(file)
        except yaml.YAMLError as e:
            if not silent:
                raise ConfigurationError("Couldn't parse config file : " + str(e))
        except Exception as e:
            if not silent:
                raise e
        return config



default = {}

development = {}

test = {}

production = {}
