"""
    rbteam.source.view
    ~~~~~~~~~~~~~~~~~~~

    This module handles views for Source objects in rbteam application

    More info in documentation at https://docs.radiobretzel.org
"""

from flask import jsonify

def infos(source):
    """Returns source object information as json.
    """
    return {
        'name': source.name,
        'channel': source.channel,
        'status': source.status
    }

# Views

def many(*sources):
    """Returns a json HTTP response for multiple source information.
    """
    infos_ = []
    for source in sources:
        infos_.append(infos(source))
    return jsonify(infos_)

def one(source):
    """Returns a json HTTP response for a single source information.
    """
    return jsonify(infos(source))
