from base import *
from Session import Session
from Result import Result

"""
    The measurement object takes any regions of interest in an Inspection and
    returns a Result object with the appropriate measurement.
    
    The handler 
    
    Note that measurements are each linked to a single Inspection object.

    Measurement( 
        name =  "largestblob",
        label = "Largest Blob",
        test_method = "largest_blob",
        parameters = {'threshval': 127 },
        result_labels = ["area","centroid"],
        is_numeric = 1,
        units =  "px",
        inspection_id = i._id)


"""
class Measurement(MappedClass):
    class __mongometa__:
        session = Session().mingsession()
        name = 'statistic'
        
    _id = ming.Field(ming.schema.ObjectId)  
    name = ming.Field(str)
    #VALIDATION NEEDED: this should be a unique name
    label = ming.Field(str)
    test_method = ming.Field(str)
    parameters = ming.Field(ming.schema.Array(str))
    result_labels = ming.Field(ming.schema.Array(str))
    
    is_numeric = ming.Field(int)
    #VALIDATION NEEDED, data should be castable 
    units = ming.Field(str)
    
    inspection = ming.orm.RelationProperty('Inspection')
    inspection_id = ming.orm.ForeignIdProperty('Inspection')

    def calculate(self, sample):
        
        function_ref = getattr(self, test_method)
        
        result = function_ref(sample, self.parameters)
           
        return Result({
            "measurement_id": self._id,
            "data": result,
            "is_numeric": self.is_numeric
        }))
        
        return data
        
    def mean_color(self, img, parameters):
        return [str(c) for c in img.meanColor()]

    def largest_blob_area(self, img, parameters):
        blobs = [str(n) for n in img.findBlobs(**parameters)]
        
        if blobs:
            return [str(blobs[-1].area())]
        
        return ''
    
