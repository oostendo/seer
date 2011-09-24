from base import *

class Frame(Document):
   class __mongometa:
       session = Seer().session
       name = 'frame'

   id = Field(schema.ObjectId)
   capturetime = Field(str)
   size = Field(tuple)
   camera = Field(str)
   image = Field(str)
