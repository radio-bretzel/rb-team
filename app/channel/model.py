from flask import current_app as app

from app.database import Document
from app.utils import formats, validations
from app.channel.source import Source

class Channel(Source, Document):
   model = 'channel'

   def __init__(self,
                  _id,
                  name=None):
      self._id = _id
      self.name = formats.name(self._id, name)

   def document(self):
      document = {
         '_id': self._id,
         'name': self.name,
      }
      return document

def validate(**data):
   """ Validate Channel arguments """
   for field in data:
      if field == '_id':
         try:
            if not data['_id'] or not validations.slug(data['_id']):
               raise ValueError('"name" argument don\'t fit the requirements.')
         except:
            return False
   return True
