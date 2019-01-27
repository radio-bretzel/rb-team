from abc import ABCMeta, abstractmethod

from rbcore.errors import SourceError

class BaseSource(metaclass=ABCMeta):
    """ This astract source will be used to provide generic methods to source classes as a Factory
    """

    def __init__(self, name, **kwargs):
        """ Do not call explicitely. Use factory function init() in ./__init__.py"""
        self.name = name
        self.channel = kwargs.get('channel')
        self.stream_mountpoint = kwargs.pop('stream_mountpoint', self.name)

    def reload(self, quiet=True):
        old_status = self.status
        if old_status not in ['non-existent', 'in error']:
            try:
                self.delete(force=True)
                self.create()
                if old_status == 'playing':
                    self.start()
            except Exception as e:
                if not quiet:
                    raise SourceError("Couldn't reload source after update : " + str(e))
        return self

    @property
    def document(self):
        """ This function generates source's document """
        return {
            'name': self.name,
            'channel': self.channel,
            'status': self.status,
            'stream_mountpoint': self.stream_mountpoint
        }

    @abstractmethod
    def create(self, force=False):
        raise NotImplementedError('Need to implement Source.create(self, force=False)')

    @property
    @abstractmethod
    def status(self):
        raise NotImplementedError('Need to implement Source.status(self) as property')

    @abstractmethod
    def start(self, quiet=False):
        raise NotImplementedError('Need to implement Source.start(self, quiet=False)')

    @abstractmethod
    def stop(self, quiet=False):
        raise NotImplementedError('Need to implement Source.stop(self, quiet=False)')

    @abstractmethod
    def delete(self, force=False, quiet=False):
        raise NotImplementedError('Need to implement Source.delete(self, force=False, quiet=False)')
