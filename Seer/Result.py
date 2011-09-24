from base import *

class Result(MappedClass):
   class __mongometa__:
       session = session
       name = 'result'

   _id = FieldProperty(schema.ObjectId)
   time = Field(str)
   data = Field(dict)
