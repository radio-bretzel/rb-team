"""
    rbcore.channel.model
    ~~~~~~~~~~~~~~~~~~~~

    This module describes the database representation and operations of the
    Channel object.

    More info in documentation at https://docs.radiobretzel.org
"""

from abc import ABCMeta, abstractmethod

from rbcore.database import Model
from rbcore.errors import DatabaseError, DatabaseNotFound, SourceError
from rbcore.source.model import Sources
from rbcore.source import source as Source
from rbcore.utils import formats
from rbcore.utils.validations import validate

class Channels(Model):
    """ Channel's model definition """
    __metaclass__ = ABCMeta

    schema = {
        'slug': {
            'required': True,
            'validator': 'slug',
        },
        'name': {
            'type': 'string',
            'coerce': 'text'
        },
        'active': {
            'validator': 'boolean',
            'coerce': 'boolean',
            'default': True
        },
        'deleted': {
            'validator': 'boolean',
            'coerce': 'boolean',
            'default': False
        },
        'description': {
            'type': 'string',
            'coerce': 'text'
        },
        'source': {
            'oneof': [
                {
                    'validator': 'slug',
                    'nullable': True
                },
                {
                    'type': 'dict',
                    'schema': Sources.schema
                }
            ]
        }
    }

    @classmethod
    @abstractmethod
    def find(cls, **filters):
        """ Returns all matching channels from given filters
        """
        collection = Model.get_collection(cls)
        schema = Channels.schema.copy()
        filters = validate(filters, schema, mandatories=False)
        if not filters.pop('active'):
            filters['active'] = True
        if not filters.pop('deleted'):
            filters['deleted'] = False
        channel_list = []
        pipeline = [
            {
                '$match': filters
            },
            {
                '$lookup': {
                    'from': 'sources',
                    'localField': 'source',
                    'foreignField': 'channel',
                    'as': 'source'
                }
            },
            {
                '$unwind': {
                    'path': '$source'
                }
            }
        ]
        try:
            for document in collection.aggregate(pipeline):
                channel = Channel(**document)
                channel_list.append(channel)
        except SourceError:
            raise
        except Exception as err:
            raise DatabaseError(str(err))
        return channel_list

    @classmethod
    @abstractmethod
    def find_one(cls, **filters):
        """ Returns the first matching channel from given name
        """
        collection = Model.get_collection(cls)
        schema = Channels.schema.copy()
        filters = validate(filters, schema, mandatories=False)
        if not filters.pop('active'):
            filters['active'] = True
        if not filters.pop('deleted'):
            filters['deleted'] = False
        pipeline = [
            {
                '$match': filters
            },
            {
                '$limit': 1
            },
            {
                '$lookup': {
                    'from': 'sources',
                    'localField': 'source',
                    'foreignField': 'channel',
                    'as': 'source'
                }
            },
            {
                '$unwind': {
                    'path': '$source'
                }
            },

        ]
        documents = []
        try:
            for document in collection.aggregate(pipeline):
                documents.append(document)
        except SourceError:
            raise
        except Exception as err:
            raise DatabaseError(str(err))
        try:
            document = documents.pop()
        except:
            raise DatabaseNotFound()
        return Channel(**document)

    @classmethod
    @abstractmethod
    def create(cls, **values):
        """ Returns the created channel from given arguments
        """
        collection = Model.get_collection(cls)
        schema = Channels.schema.copy()
        values = validate(values, schema)
        slug = values.get('slug')
        for document in collection.find({'slug': slug}).limit(1):
            if document:
                raise ValueError("channel " + str(channel) + " already exists.")
        source_args = values.pop('source', {})
        if not source_args.get('name'):
            source_args['name'] = slug
        source_args['channel'] = slug
        if not source_args.get('status'):
            values['source'] = Sources.create(**source_args)
        channel = Channel(**values)
        try:
            collection.insert_one(channel.document)
        except Exception as err:
            DatabaseError(str(err))
        return channel

    @classmethod
    @abstractmethod
    def update(cls, channel, values):
        """ Returns the first matching channel with given slug , updated with
        given arguments
        """
        collection = Model.get_collection(cls)
        if isinstance(channel, str):
            channel = Channels.find_one(**{'slug': channel})
        schema = Channels.schema.copy()
        formats.pop_keys(schema, 'source')
        values = validate(values, schema, mandatories=False)
        vars(channel).update(values)
        if values:
            try:
                source.reload()
            except:
                pass
        try:
            collection.update_one(
                {'slug': channel.slug},
                {'$set': channel.document}
            )
        except Exception as err:
            raise DatabaseError(str(err))
        return channel

    @classmethod
    @abstractmethod
    def delete(cls, channel, **opts):
        collection = Model.get_collection(cls)
        source_collection = Model.get_collection(Sources)
        schema = {
            'hard_delete': {
                'validator': 'boolean',
                'coerce': 'boolean',
                'default': False
            }
        }
        hard_delete = validate(opts, schema).pop('hard_delete')
        if isinstance(channel, str):
            channel = Channels.find_one(**{'slug': channel, 'deleted': hard_delete})
        if channel.source:
            channel.source.delete(force=True, quiet=True)
        if hard_delete:
            try:
                source_collection.delete_one({'name': channel.source.name})
                collection.delete_one({'slug': channel.slug})
            except Exception as err:
                raise DatabaseError(str(err))
        else:
            channel.deleted = True
            try:
                collection.update_one(
                    {'slug': channel.slug},
                    {'$set': channel.document}
                )
            except Exception as err:
                raise DatabaseError(str(err))
        return channel


class Channel():
    """ Channel object.
    """
    def __init__(self, **kwargs):
        self.slug = kwargs.pop('slug')
        self.active = kwargs.pop('active', True)
        self.deleted = kwargs.pop('deleted', False)
        self.name = kwargs.pop('name', formats.id_to_name(self.slug))
        self.description = kwargs.pop(
            'description',
            "Welcome to " + self.name + " Radio Bretzel Channel"
        )
        source = kwargs.pop('source', None)
        if isinstance(source, dict):
            self.source = Source.init(**source)
        else:
            self.source = source

    @property
    def document(self):
        """ Channel model database schema """
        document = vars(self).copy()
        document['source'] = getattr(self.source, 'name', None)
        return document
