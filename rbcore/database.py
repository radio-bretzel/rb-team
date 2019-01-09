import abc
from flask import current_app as app
from flask_pymongo import PyMongo
from rbcore.errors import DatabaseError


_models = [
    'channels',
    'sources',
]


def get_database():
    if not hasattr(app, 'db'):
        try:
            mongo = PyMongo(app)
            app.db = mongo.db
            app.db.command('ping')
        except Exception as e:
            raise DatabaseError("Couldn't initiate database connection : " + str(e))
    return app.db


class Model(object):
    """ Abstract class whose different models will inherit """
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def get_collection(model):
        """ Returns collection object from given model class"""
        db = get_database()
        name = model.__name__.lower()
        if name in _models:
            collection = db[name]
            return collection
        else:
            raise DatabaseError("Couldn't get collection : Unreferenced model ''" + name + "'")


    @staticmethod
    def _schema():
        """ Returns a tuple of valids and invalids arguments
        """
        raise NotImplementedError('Need to implement Model._schema()')


    @classmethod
    @abc.abstractmethod
    def find(cls, **filters):
        """ Returns multiple matching documents from given filters
        """
        raise NotImplementedError('Need to implement Model.find()')


    @classmethod
    @abc.abstractmethod
    def find_one(cls, slug, **filters):
        """ Returns the first matching document from given filters
        """
        raise NotImplementedError('Need to implement Model.find_one()')


    @classmethod
    @abc.abstractmethod
    def create(cls, slug, **args):
        """ Returns new document from given args
        """
        raise NotImplementedError('Need to implement Model.create()')


    @classmethod
    @abc.abstractmethod
    def update(cls, slug, values):
        """ Returns first matching document with given slug, updated with
        given document
        """
        raise NotImplementedError('Need to implement Model.update()')


    @classmethod
    @abc.abstractmethod
    def delete(cls, instance):
        """ Delete the current document from given collection
        """
        raise NotImplementedError('Need to implement Model.delete()')
