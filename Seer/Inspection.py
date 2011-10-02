from base import *
from Session import *
from Measurement import Measurement

class Inspection(MappedClass):
    """
    An Inspection determines what part of an image to look at from a given camera
    and what Measurement objects get taken.  It has a single handler, the roi_method,
    which determines ROI for the measurements.
    
    The roi_method determines if measurements are or are not taken.  A completely
    passive roi_method would return the entire image space (taking measurements
    on every frame), and an "enabled = 0" equivalent would be roi_method always
    returning None.
    
    The roi_method can return several samples, pieces of the evaluated frame,
    and these get passed in turn to each Measurement.
    
    The results from these measurements are aggregated and returned from the
    Inspection.execute() function, which gives all samples to each measurement.
    
    insp = Inspection(
        name = "Blob Measurement 1",
        test_type = "Measurement",
        enabled = 1,
        roi_method = "fixed_window",
        camera = "0",
        roi_parameters = ["100", "100", "400", "300"]) #x,y,w,h
    
    Measurement(..., inspection_id = ins._id )
    
    results = insp.execute()
    
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
        """
        The exeecute method takes in a frame object, executes the roi_method
        and sends the samples to each measurement object.  The results are returned
        as a multidimensional array [ samples ][ measurements ] = result
        """

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

    #below are "core" inspection functions

    def fixed_window(self, frame):        
        params = tuple([int(p) for p in self.roi_parameters])
        return (frame.image.crop(*params), params)
#    def __json__(self):
 
ming.orm.Mapper.compile_all()   
for mapper in ming.orm.Mapper.all_mappers():
    Session().mingsession.ensure_indexes(mapper.collection)
