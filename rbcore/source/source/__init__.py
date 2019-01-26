from flask import current_app as app
from rbcore.source.source.docker import DockerSource

def init(name, type=None, **kwargs):
    """ Factory function called for source creation """
    if not type:
        type = app.config.get('SOURCE_TYPE', 'docker')
    if type == 'docker':
        return DockerSource(name, **kwargs)
    raise ValueError('unsupported source type ' + str(source_type))
