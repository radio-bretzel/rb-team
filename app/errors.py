class RadioBretzelException(Exception):
   """
   A base class from which all other exceptions inherit.

   If you want to catch all errors that the Radio Bretzel API might raise,
   catch this base exception.
   """

class DatabaseError(RadioBretzelException):
   pass

class DockerError(RadioBretzelException):
   pass
