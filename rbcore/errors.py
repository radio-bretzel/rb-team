class RadioBretzelException(Exception):
    """
    A base class from which all other exceptions inherit.

    If you want to catch all errors that the Radio Bretzel API might raise,
    catch this base exception.
    """

class ConfigurationError(RadioBretzelException):
    pass

class DatabaseError(RadioBretzelException):
    pass
class DatabaseNotFound(DatabaseError):
    pass

class DockerError(RadioBretzelException):
    pass

class SourceError(RadioBretzelException):
    pass
class SourceNotFound(SourceError):
    pass

class ValidationError(RadioBretzelException):
    pass


def register_handlers(app):
    @app.errorhandler(DatabaseNotFound)
    def not_found(error):
        return "This page doesn't exist", 404

    @app.errorhandler(ValidationError)
    def validation_error(error):
        return str(error), 400

    @app.errorhandler(RadioBretzelException)
    def default_error(error):
        return str(error), 500
