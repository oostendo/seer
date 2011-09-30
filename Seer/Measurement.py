from base import *
from Session import Session
from Result import Result

"""


    Measurement( 
        name =  "largestblob",
        label = "Largest Blob",
        test_method = "largest_blob",
        required_parameters = [],
        optional_parameters = ['threshval', 'minsize', 'maxsize', 'threshblocksize', 'threshconstant'],
        result_labels = ["area","centroid"],
        units =  "px",
        inspection_id = i._id)


"""
class Measurement(MappedClass):
    class __mongometa__:
        session = Session().getORMSession()
        name = 'statistic'
        
    _id = ming.orm.FieldProperty(ming.schema.ObjectId)  
    name = ming.orm.FieldProperty(str)
    label = ming.orm.FieldProperty(str)
    test_method = ming.orm.FieldProperty(str)
    required_parameters = ming.orm.FieldProperty(ming.schema.Array(str))
    optional_parameters = ming.orm.FieldProperty(ming.schema.Array(str))
    result_labels = ming.orm.FieldProperty(ming.schema.Array(str))
    units = ming.orm.FieldProperty(str)
    
    inspection = ming.orm.RelationProperty('Inspection')
    inspection_id = ming.orm.ForeignIdProperty('Inspection')

    def calculate(self, parameters, sample):
        
        #basic validation, make sure all parameters are here -- but optional ones can be passed
        for param in self.required_parameters:
            if not parameters[param]:
                raise "Parameter " + param + " is required for Statistic " + self.name
        
        function_ref = getattr(self, test_method)
        data = []
        
        result = function_ref(sample, parameters)
           
        data.append(Result({
            "measurement_id": self._id,
            "data": result
        }))
        
        return data
        
    def mean_color(self, img, parameters):
        return [str(c) for c in img.meanColor()]

    def largest_blob_area(self, img, parameters):
        blobs = [str(n) for n in img.findBlobs(**parameters)]
        
        if blobs:
            return [str(blobs[-1].area())]
        
        return ''
    
