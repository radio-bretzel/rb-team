
def name(_id, name=None):
   if not name:
      name = _id.replace('-', ' ')
   return name.title()
