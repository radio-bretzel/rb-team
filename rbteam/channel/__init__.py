"""
    rbteam.channel
    ~~~~~~~~~~~~~~

    This module handles channel routes and public interface for Flask.
    Channels represents rooms where users can listen to music and chat.

    More info in documentation at https://docs.radiobretzel.org
"""

from flask import request, abort

from rbteam.channel.model import Channel, Channels
from rbteam.channel import view
from rbteam.errors import DatabaseError, ValidationError
from rbteam.source import view as source_view
from rbteam.utils import formats, validations


def routes(app):
    """All routes for channel resources

    This function initialize all routes for the given app
    """

    @app.route('/channel/', methods=['GET'])
    def get_channels(): # pylint: disable=unused-variable
        values = request.args.to_dict()
        channels = Channels.find(**values)
        return view.many(*channels)

    @app.route('/channel/<string:slug>', methods=['GET'])
    def get_channel(slug):  # pylint: disable=unused-variable
        values = request.args.to_dict()
        values.update({'slug': slug})
        channel = Channels.find_one(**values)
        return view.one(channel)

    @app.route('/channel/<string:slug>', methods=['POST'])
    def create_channel(slug):   # pylint: disable=unused-variable
        values = request.form.to_dict()
        values.update({'slug': slug})
        channel = Channels.create(**values)
        return view.one(channel)

    @app.route('/channel/<string:slug>', methods=['PUT', 'UPDATE'])
    def update_channel(slug):   # pylint: disable=unused-variable
        values = request.form.to_dict()
        updated_channel = Channels.update(slug, values)
        return view.one(updated_channel)

    @app.route('/channel/<string:slug>', methods=['DELETE'])
    def delete_channel(slug):   # pylint: disable=unused-variable
        values = request.form.to_dict()
        deleted_channel = Channels.delete(slug, **values)
        return view.one(deleted_channel)

    @app.route('/channel/<string:slug>/source', methods=['GET'])
    def get_channel_source(slug):   # pylint: disable=unused-variable
        values = request.form.to_dict()
        values.update({'slug': slug})
        channel = Channels.find_one(**values)
        return source_view.one(channel.source)

    @app.route('/channel/<string:slug>/source/start')
    def start_channel_source(slug): # pylint: disable=unused-variable
        values = request.form.to_dict()
        values.update({'slug': slug})
        channel = Channels.find_one(**values)
        channel.source.start()
        return source_view.one(channel.source)

    @app.route('/channel/<string:slug>/source/stop')
    def stop_channel_source(slug):  # pylint: disable=unused-variable
        values = request.form.to_dict()
        values.update({'slug': slug})
        channel = Channels.find_one(**values)
        channel.source.stop()
        return source_view.one(channel.source)
