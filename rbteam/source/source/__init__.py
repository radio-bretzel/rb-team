"""
    rbteam.source.source
    ~~~~~~~~~~~~~~~~~~~~

    This module hosts every radio bretzel source type. All its modules can
    create, delete, start, stop and manage audio sources for Radio Bretzel.

    More info in documentation at https://docs.radiobretzel.org
"""

from flask import current_app as app

from rbteam.source.source.docker import DockerSource


def init(name, type=None, **kwargs):
    """Factory function called for source creation.
    """
    if not type:
        type = app.config.get('SOURCE_TYPE', 'docker')
    if type == 'docker':
        return DockerSource(name, **kwargs)
    raise ValueError('unsupported source type ' + str(source_type))
