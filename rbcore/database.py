"""
    rbcore.database
    ~~~~~~~~~~~~~~~

    This module handles database operations and the core data model.

    More info in documentation at https://docs.radiobretzel.org
"""

import abc

from flask import current_app as app
from flask_pymongo import PyMongo

from rbcore.errors import DatabaseError


def get_database():
    """Returns the current database connection or create it if doesn't exist.
    """
    if not hasattr(app, 'db'):
        mongo_uri = app.config.get('MONGO_URI')
        if not mongo_uri:
            mongo_host = app.config.get('MONGO_HOST', 'localhost')
            mongo_port = app.config.get('MONGO_PORT', 27017)
            mongo_user = app.config.get('MONGO_USER')
            mongo_passwd = app.config.get('MONGO_PASSWD')
            mongo_database = app.config.get('MONGO_DATABASE', 'rbcore')
            mongo_uri = 'mongodb://'
            if mongo_user:
                mongo_uri += mongo_user
                if mongo_passwd:
                    mongo_uri += ':' + mongo_passwd
                mongo_uri += '@'
            mongo_uri += mongo_host + ':' + str(mongo_port)
            mongo_uri += '/' + mongo_database
        else:
            if not mongo_uri.startswith('mongodb://'):
                mongo_uri = 'mongodb://' + mongo_uri
        try:
            mongo = PyMongo(app, uri=mongo_uri)
            app.mongo = mongo.db
            app.mongo.command('ping')
        except Exception as err:
            raise DatabaseError("Couldn't initiate database connection : " + str(err))
    return app.mongo


class Model():
    """Abstract class whose different models will inherit.
    """
    __metaclass__ = abc.ABCMeta

    __MODELS = [
        'channels',
        'sources',
    ]

    @staticmethod
    def get_collection(model):
        """Returns collection object from given model class.
        """
        db = get_database()
        name = model.__name__.lower()
        if name not in Model.__MODELS:
            raise DatabaseError("Couldn't get collection : Unreferenced model ''" + name + "'")
        collection = db[name]
        return collection


    @staticmethod
    def _schema():
        """Returns a tuple of valids and invalids arguments.
        """
        raise NotImplementedError('Need to implement Model._schema()')


    @classmethod
    @abc.abstractmethod
    def find(cls, **filters):
        """Returns multiple matching documents from given filters.
        """
        raise NotImplementedError('Need to implement Model.find()')


    @classmethod
    @abc.abstractmethod
    def find_one(cls, slug, **filters):
        """Returns the first matching document from given filters.
        """
        raise NotImplementedError('Need to implement Model.find_one()')


    @classmethod
    @abc.abstractmethod
    def create(cls, slug, **args):
        """Returns new document from given args.
        """
        raise NotImplementedError('Need to implement Model.create()')


    @classmethod
    @abc.abstractmethod
    def update(cls, slug, values):
        """Returns first matching document with given slug, updated with
        given document.
        """
        raise NotImplementedError('Need to implement Model.update()')


    @classmethod
    @abc.abstractmethod
    def delete(cls, instance):
        """ Delete the current document from given collection
        """
        raise NotImplementedError('Need to implement Model.delete()')
