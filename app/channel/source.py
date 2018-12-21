from flask import current_app as app

from app.docker import get_source_network

class Source(object):
   """ Abstract class whose Channels will inherit """
   def get_container_name(self):
      return app.config['OBJECTS_NAME_PREFIX'] + 'source_' + self._id

   def create_source(self):
      """ Create a source container from given args """
      source_container_config = app.config.get_namespace('SOURCE_CONTAINER_')
      stream_config = app.config.get_namespace('STREAM_')
      container_args = {
         'name': self.get_container_name(),
         'detach': True,
         'read_only': True,
         #'auto_remove': True,
         'environment': {
            'STREAM_MOUNTPOINT': self._id,
            'STREAM_HOST': stream_config['host'],
            'STREAM_SOURCE_PASSWD': stream_config['source_passwd']
         },
      }
      source_container_config.update(container_args)

      source = app.docker.containers.run(image=app.config['SOURCE_IMAGE'], **source_container_config)
      if not source:
         return False
      source_network = get_source_network()
      if not source_network:
         raise SystemError('Couldn\'t get nor create Source network')
         return False
      source_network.connect(source)
      return source

   def get_source(self):
      """ Return source container object or false if doesn't exist """
      try:
         source = app.docker.containers.get(self.get_container_name())
         if not source:
            return False
         return source
      except:
         return False

   def get_or_create_source(self):
      """ Return source container object, and create it if doesn't exist """
      source = self.get_source()
      if not source:
         source = self.create_source()
      if not source:
         return False
      else:
         self.source = source
         return source

   def reload_source(self):
      return True

   def delete_source(self):
      return app.docker.containers.remove(self.get_container_name())
