from appdirs import AppDirs
from flask import Flask
from os import path

from rbcore import channel, config, database, docker, errors, source

def create_app(
    environment='production',
    config_file=None,
    instance_path=None,
    debug=False,
    **kwargs
):
    """ Main application entry point """

    if environment not in ['development', 'test', 'production']:
        raise ConfigurationError("Unknown environment '" + environment + "'")

    if debug:
        Flask.debug = True

    Flask.config_class = config.RBCoreConfig
    Flask.default_config.update(config.default)
    app = Flask(
        __name__,
        instance_path=instance_path,
        instance_relative_config=True
    )

    app.config.load(environment, config_file, **kwargs)

    errors.register_handlers(app)
    register_routes(app)
    register_main_routes(app)
    # register_teardown(app)

    return app


def register_routes(app):
    """ Register routes of submodules. """
    channel.routes(app)
    source.routes(app)


def register_main_routes(app):
    """ Register main routes for application. """
    @app.route('/')
    def hello_world():
        return 'Welcome to Radio Bretzel'


# def register_teardown(app):
#     """Register teardowns """
#     @app.teardown_appcontext
#     def remove_source_network(error):
#         teardown_docker(app)
