from flask import request, abort

from rbcore.source import view
from rbcore.source.model import Sources
from rbcore.config import get_config
from rbcore.errors import DatabaseError, ValidationError, DatabaseNotFound

def routes(app):
    """ All routes for source resources"""

    @app.route('/source', methods=['GET'])
    def get_sources():
        """
        Returns all matching sources from given filters
        """
        values = request.args.to_dict()
        sources = Sources.find(**values)
        return view.many(*sources)

    @app.route('/source/<string:name>', methods=['GET'])
    def get_source(name):
        values = request.args.to_dict()
        values.update({'name': name})
        source = Sources.find_one(**values)
        return view.one(source)

    @app.route('/source', methods=['POST'])
    @app.route('/source/<string:name>', methods=['POST'])
    def create_source(name=None):
        values = request.form.to_dict()
        if name:
            values.update({'name': name})
        source = Sources.create(**values)
        return view.one(source)

    @app.route('/source/<string:name>', methods=['PUT', 'UPDATE'])
    def update_source(name):
        values = request.form.to_dict()
        source = Sources.update(name, **values)
        return view.one(source)

    @app.route('/source/<string:name>', methods=['DELETE'])
    def delete_source(name):
        values = request.form.to_dict()
        source = Sources.delete(name, **values)
        return view.one(source)

    @app.route('/source/<string:name>/start')
    def start_source(name):
        source = Sources.find_one(**{'name': name})
        source.start()
        return view.one(source)

    @app.route('/source/<string:name>/stop')
    def stop_source(name):
        source = Sources.find_one(**{'name': name})
        source.stop()
        return view.one(source)
