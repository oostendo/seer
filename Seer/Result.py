from base import *
from Session import Session

class Result(ming.Document):
    """
    Result( {
       "data": ["1","2","3"]
    
    """
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
    
    @property
    def float_data(self):
        if not self.is_numeric:
            return None
        np.cast[float](self.data)
        
    @property
    def int_data(self):
        if not self.is_numeric:
            return None
        np.cast[int](self.data)
        
    def save(self):
        self.m.save()
        
