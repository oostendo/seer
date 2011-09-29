from base import *
from Session import Session

class Result(ming.Document):
    class __mongometa__:
        session = Session().mingsession
        name = 'result'
        
    data = ming.Field(ming.schema.Array(str))
    roi = ming.Field(ming.schema.Array(int))
    capturetime = ming.Field(float)
    camera = ming.Field(str)

    measurement_id = ming.Field(ming.schema.ObjectId)
    inspection_id = ming.Field(ming.schema.ObjectId)
    frame_id = ming.Field(ming.schema.ObjectId)
