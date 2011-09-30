from base import *
from Session import *
from Measurement import Measurement

class Inspection(MappedClass):
    """
    
    Inspection(
        name = "Blob Measurement 1",
        test_type = "Measurement",
        enabled = 1,
        roi_method = "fixed_window",
        camera = "0",
        roi_parameters = ["100", "100", "400", "300"]) #x,y,w,h
    
    """
    class __mongometa__:
        session = Session().getORMSession()
        name = 'inspection'
        
    _id = ming.orm.FieldProperty(ming.schema.ObjectId)    
    name = ming.orm.FieldProperty(str)
    test_type = ming.orm.FieldProperty(str) 
    roi_method = ming.orm.FieldProperty(str)#this might be a relation 
    enabled = ming.orm.FieldProperty(int)
    camera = ming.orm.FieldProperty(str)
    roi_parameters = ming.orm.FieldProperty(ming.schema.Array(str))
    measurements = ming.orm.RelationProperty('Measurement')
                         
    def execute(self, frame):

        roi_function_ref = getattr(self, self.roi_method)
        #get the ROI function that we want
        #note that we should validate/roi method

                
        samples, roi = roi_function_ref(frame)
            
        if not isinstance(samples, list):
            samples = [samples]
        
        results = []
        for sample in samples:
            
            for m in self.measurements:
                r = m.calculate(sample)
                     
                r.roi = roi
                r.capturetime = frame.capturetime
                r.camera = frame.camera
                r.frame_id = frame._id
                r.inspection_id = self._id
                r.measurement_id = m._id
                    
                results.append[r]
                #probably need to add unit conversion here
                        

        return results

    def fixed_window(self, frame):        
        params = tuple([int(p) for p in self.roi_parameters])
        return (frame.image.crop(*params), params)
#    def __json__(self):
 
ming.orm.Mapper.compile_all()   
for mapper in ming.orm.Mapper.all_mappers():
    Session().mingsession.ensure_indexes(mapper.collection)
