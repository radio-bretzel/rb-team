"""
    rbcore.channel
    ~~~~~~~~~~~~~~

    This module handles channel routes and public interface for Flask.
    Channels represents rooms where users can listen to music and chat.

    More info in documentation at https://docs.radiobretzel.org
"""

from flask import request, abort

from rbcore.channel.model import Channel, Channels
from rbcore.channel import view
from rbcore.errors import DatabaseError, ValidationError
from rbcore.source import view as source_view
from rbcore.utils import formats, validations


def routes(app):
    """All routes for channel resources

    This function initialize all routes for the given app
    """
    # pylint: disable=unused-variable
    @app.route('/channel/', methods=['GET'])
    def get_channels():
        # pylint: enable=unused-variable
        values = request.args.to_dict()
        channels = Channels.find(**values)
        return view.many(*channels)

    # pylint: disable=unused-variable
    @app.route('/channel/<string:slug>', methods=['GET'])
    def get_channel(slug):
        # pylint: enable=unused-variable
        values = request.args.to_dict()
        values.update({'slug': slug})
        channel = Channels.find_one(**values)
        return view.one(channel)

    # pylint: disable=unused-variable
    @app.route('/channel/<string:slug>', methods=['POST'])
    def create_channel(slug):
        # pylint: enable=unused-variable
        values = request.form.to_dict()
        values.update({'slug': slug})
        channel = Channels.create(**values)
        return view.one(channel)

    # pylint: disable=unused-variable
    @app.route('/channel/<string:slug>', methods=['PUT', 'UPDATE'])
    def update_channel(slug):
        # pylint: enable=unused-variable
        values = request.form.to_dict()
        updated_channel = Channels.update(slug, values)
        return view.one(update_channel)

    # pylint: disable=unused-variable
    @app.route('/channel/<string:slug>', methods=['DELETE'])
    def delete_channel(slug):
        # pylint: enable=unused-variable
        values = request.form.to_dict()
        deleted_channel = Channels.delete(slug, **values)
        return view.one(deleted_channel)

    # pylint: disable=unused-variable
    @app.route('/channel/<string:slug>/source', methods=['GET'])
    def get_channel_source(slug):
        # pylint: enable=unused-variable
        values = request.form.to_dict()
        values.update({'slug': slug})
        channel = Channels.find_one(**values)
        return source_view.one(channel.source)

    # pylint: disable=unused-variable
    @app.route('/channel/<string:slug>/source/start')
    def start_channel_source(slug):
        # pylint: enable=unused-variable
        values = request.form.to_dict()
        values.update({'slug': slug})
        channel = Channels.find_one(**values)
        channel.source.start()
        return source_view.one(channel.source)

    # pylint: disable=unused-variable
    @app.route('/channel/<string:slug>/source/stop')
    def stop_channel_source(slug):
        # pylint: enable=unused-variable
        values = request.form.to_dict()
        values.update({'slug': slug})
        channel = Channels.find_one(**values)
        channel.source.stop()
        return source_view.one(channel.source)
