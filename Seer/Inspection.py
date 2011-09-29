from base import *
from Session import *
from Measurement import Measurement

class Inspection(MappedClass):
    """
    
    Inspection(
        title = "Blob Measurement 1",
        test_type = "Measurement",
        enabled = 1,
        roi_method = "fixed_window",
        roi_parameters = ["100", "100", "400", "300"]) #x,y,w,h
    
    """
    class __mongometa__:
        session = Session().getORMSession()
        name = 'inspection'
        
    _id = ming.orm.FieldProperty(ming.schema.ObjectId)    
    title = ming.orm.FieldProperty(str)
    test_type = ming.orm.FieldProperty(str) 
    roi_method = ming.orm.FieldProperty(str)#this might be a relation 
    enabled = ming.orm.FieldProperty(int)
    roi_parameters = ming.orm.FieldProperty(ming.schema.Array(str))
    measurements = ming.orm.RelationProperty('Measurement')
                         
    def execute(self, frames):
        if not isinstance(frames, (list, tuple)):
            frames = [frames]
        
        roi_function_ref = getattr(self, self.roi_method)
        #get the ROI function that we want
            
        for frame in frames:
            samples, roi = roi_function_ref(frame, self.roi_parameters)
            
            
            for sample in samples:
            
                for m in measurements:
                    results = m.calculate(self.samples)
                    count = 0
                     
                    for r in results:
                        r.roi = roi
                        r.capturetime = frame.capturetime
                        r.camera = frame.camera
                        r.frame_id = frame._id
                        r.inspection_id = self._id
                        r.measurement_id = m._id
                        self.results.append[r]
                        #probably need to add unit conversion here
                        
    def record(self):
        for r in results:
            r.m.save()
            
    def getResults(self):
        return [r.data for r in self.results]

    def clear():
        self.data = {}
        self.samples = []
        self.results = []
        
    def fixed_window(self, frame, parameters):        
        params = tuple(parameters)
        return ( frame.image.crop(*parameters),
            ( parameters ) )
#    def __json__(self):
 
ming.orm.Mapper.compile_all()   
for mapper in ming.orm.Mapper.all_mappers():
    Session().mingsession.ensure_indexes(mapper.collection)
