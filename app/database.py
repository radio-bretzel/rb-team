from flask import current_app as app
from flask_pymongo import PyMongo

from app.errors import DatabaseError

models = [
   'channel',
]

def connect_db(app):
   """ Open a Mongodb connection."""
   client = PyMongo(app)
   return client

def init_db(app):
   """ Initiate DB connection at app startup """
   if not hasattr(app, 'mongo'):
      app.mongo = connect_db(app)
   return app

def get_collection(name):
   try:
      if not hasattr(app, 'mongo'):
         raise DatabaseError("Database unavailable")
      if name in models:
         collection = app.mongo.db[name]
         return collection
      else:
         raise DatabaseError('Database Error - Unreferenced model')
   except:
      raise DatabaseError("Couldn't get collection object")

class Document(object):
   """ Abstract class whose different models will inherit """

   def save(self):
      """ Update or create model's document in database """
      try:
         collection = get_collection(self.model)
         document = self.document()
         existing_document = collection.find_one({'_id': document['_id']})
         if existing_document:
            collection.replace_one(existing_document, document)
         else:
            collection.insert_one(document)
         return True
      except:
         raise SystemError("Couldn't save " + self.model + " in database")

   def delete(self):
      """ Delete the current document from given collection """
      try:
         collection = get_collection(self.model)
         document = self.document()
         if not document.get('_id'):
            raise KeyError('No primary key given for object')
         existing_document = collection.find_one({'_id': document['_id']})
         if not existing_document:
            raise DatabaseError('Document not found')
         collection.remove(existing_document)
         return True
      except:
         raise DatabaseError("Couldn't delete " + self.model + " in database")
