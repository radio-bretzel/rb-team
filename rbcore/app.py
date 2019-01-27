# -*- coding: utf-8 -*-
"""
    rbcore.app
    ~~~~~~~~~~

    This module implements the central WSGI application object.

    More info in documentation at https://docs.radiobretzel.org
"""


from flask import Flask

from rbcore import config, errors
from rbcore import channel, source


def create_app(
        environment='production',
        config_file=None,
        instance_path=None,
        **extra_config
    ):
    """Main application fabric entry point.
    """

    if environment not in ['development', 'test', 'production']:
        raise errors.ConfigurationError("Unknown environment '" + environment + "'")

    Flask.config_class = config.RBCoreConfig
    app = Flask(
        __name__,
        instance_path=instance_path,
        instance_relative_config=True
    )

    app.config.load(environment, config_file, **extra_config)

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
        #pylint: disable=unused-argument
        return 'Welcome to Radio Bretzel'


# def register_teardown(app):
#     """Register teardowns """
#     @app.teardown_appcontext
#     def remove_source_network(error):
#         teardown_docker(app)
