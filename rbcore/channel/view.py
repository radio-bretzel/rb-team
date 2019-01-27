"""
    rbcore.channel.view
    ~~~~~~~~~~~~~~~~~~~

    This module handles views for Channel objects in rbcore application

    More info in documentation at https://docs.radiobretzel.org
"""

from flask import jsonify

def infos(channel):
    """Returns given channel informations as json.
    """
    info = channel._document
    info['source'] = {
        'name': channel.source.name,
        'status': channel.source.status
    }
    info.pop('deleted')
    return info

# Views
def many(*channels):
    """Returns a view of informations of the given channels.
    """
    list_ = []
    for channel in channels:
        list_.append(infos(channel))
    return jsonify(list_)

def one(channel):
    """Returns the inofrmations for the given channel.
    """
    return jsonify(infos(channel))
