from rbcore.config import get_config
from rbcore.source.source.docker import DockerSource

def init(name, type=None, **kwargs):
    """ Factory function called for source creation """
    config = get_config()
    if not type:
        type = config.get('SOURCE_TYPE', 'docker')
    if type == 'docker':
        return DockerSource(name, **kwargs)
    raise ValueError('unsupported source type ' + str(source_type))
