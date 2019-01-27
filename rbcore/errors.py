# -*- coding: utf-8 -*-
"""
    rbcore.errors
    ~~~~~~~~~~~~~

    All rbcore specific Exceptions are registerd in this module.

    More info in documentation at https://docs.radiobretzel.org
"""

class RadioBretzelException(Exception):
    """A base class from which all other exceptions inherit.

    If you want to catch all errors that the Radio Bretzel API might raise,
    catch this base exception.
    """


class ConfigurationError(RadioBretzelException):
    """A specific Exception for configuration errors.
    """


class DatabaseError(RadioBretzelException):
    """A base Exception for database errors.
    """

class DatabaseNotFound(DatabaseError):
    """A specific Exception raised when a database request returns an empty
    set.
    """


class DockerError(RadioBretzelException):
    """A specific Exception raised instead of docker.errors.
    """


class SourceError(RadioBretzelException):
    """A base Exception for source errors.
    """

class SourceNotFound(SourceError):
    """A specific Exception raised when the asked source doesn't exists.
    """


class ValidationError(RadioBretzelException):
    """A specific Exception raised when an input validation test fails.
    """


def register_handlers(app):
    """This function register the way our application response to HTTP requests
    when an error is raised in the application backend.
    """
    # pylint: disable=unused-argument, unused-variable
    @app.errorhandler(DatabaseNotFound)
    def not_found(error):
        return "This page doesn't exists", 404
    # pylint: enable=unused-argument

    @app.errorhandler(ValidationError)
    def validation_error(error):
        return str(error), 400

    @app.errorhandler(RadioBretzelException)
    def default_error(error):
        return str(error), 500
    # pylint: enable=unused-variable
