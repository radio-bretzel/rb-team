"""
    rbcore.source.model
    ~~~~~~~~~~~~~~~~~~~

    This module handles every database operation for Radio Bretzel sources.

    More info in documentation at https://docs.radiobretzel.org
"""

from abc import ABCMeta, abstractmethod

from rbcore.database import Model
from rbcore.errors import SourceError, ValidationError, DatabaseError, DatabaseNotFound
from rbcore.source import source as Source
from rbcore.utils import formats
from rbcore.utils.validations import validate

class Sources(Model):
    """ Source's model definition """
    __metaclass__ = ABCMeta

    schema = {
        'name': {
            'required': True,
            'validator': 'slug'
        },
        'channel': {
            'required': True,
            'validator': 'slug'
        },
        'status': {
            'allowed': ['playing', 'stopped', 'non-existent', 'in error']
        },
        'stream_mountpoint': {
            'validator': 'slug'
        }
    }

    @classmethod
    @abstractmethod
    def find(cls, **filters):
        """ Returns multiple matching documents from given filters
        """
        collection = Model.get_collection(cls)
        schema = Sources.schema.copy()
        filters = validate(filters, schema, mandatories=False)
        source_list = []
        try:
            for document in collection.find(filters):
                name = document.pop('name')
                source = Source.init(name, **document)
                source_list.append(source)
        except SourceError:
            raise
        except Exception as err:
            raise DatabaseError(str(err))
        return source_list


    @classmethod
    @abstractmethod
    def find_one(cls, **filters):
        """ Returns the first matching document from given filters
        """
        collection = Model.get_collection(cls)
        schema = Sources.schema.copy()
        filters = validate(filters, schema, mandatories=False)
        if not filters:
            raise ValidationError('You must provide at least one filter')
        documents = []
        try:
            for document in collection.find(filters).limit(1):
                documents.append(document)
        except Exception as err:
            raise DatabaseError(str(err))
        if not documents:
            raise DatabaseNotFound()
        document = documents.pop()
        name = document.pop('name')
        return Source.init(name, **document)


    @classmethod
    @abstractmethod
    def create(cls, **kwargs):
        """ Returns new document from given args
        """
        collection = Model.get_collection(cls)
        schema = Sources.schema.copy()
        values = validate(kwargs, schema)
        name = values.pop('name')
        values['status'] = values.get('status', 'stopped')
        for document in collection.find({'name': name}).limit(1):
            if document:
                raise ValueError("source '" + str(name) + "' already exists.")
        source = Source.init(name, **values)
        source.create()
        try:
            collection.insert_one(source.document)
        except Exception as err:
            DatabaseError(str(err))
        return source

    @classmethod
    @abstractmethod
    def update(cls, source, values):
        """ Update given source with given values. Source.init can be source object or source name
        """
        collection = Model.get_collection(cls)
        if isinstance(source, str):
            source = Sources.find_one(**{'name': source})
        schema = Sources.schema.copy()
        formats.pop_keys(schema, 'name', 'channel', 'status')
        values = validate(values, schema, mandatories=False)
        vars(source).update(values)
        if values:
            try:
                source.reload()
            except:
                pass
        try:
            collection.update_one(
                {'name': source.name},
                {'$set': source.document}
            )
        except Exception as err:
            raise DatabaseError(str(err))
        return source

    @classmethod
    @abstractmethod
    def delete(cls, source, force='False', **opts):
        """ Delete the current document from given collection
        """
        collection = Model.get_collection(cls)
        if isinstance(source, str):
            source = Sources.find_one(**{'name': source})
        schema = {
            'force': {
                'validator': 'boolean',
                'coerce': 'boolean'
            }
        }
        force = validate({'force': force}, schema).pop('force')
        source.delete(force=force)
        try:
            collection.delete_one({'name': source.name})
        except Exception as err:
            raise DatabaseError(str(err))
        return source
