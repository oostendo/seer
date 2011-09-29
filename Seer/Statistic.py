from base import *

class Statistic(ming.MappedClass):
    name = Field(str)
    label = Field(str)
    test_method = Field(str)
    required_parameters = Field(schema.Array)
    optional_parameters = Field(schema.Array)
    result_labels = Field(schema.Array)
    units = Field(str)

    def calculate(self, parameters, samples):
        
        #basic validation, make sure all parameters are here -- but optional ones can be passed
        for param in self.required_parameters:
            if not parameters[param]:
                raise "Parameter " + param + " is required for Statistic " + self.name
        
        function_ref = getattr(self, test_method)
        data = []
        for s in samples:
            result = function_ref(s, parameters)
            
            data.append(StatResult({
                "statistic": self,
                "data": list(result)
            }))
        
        return data
        
    def mean_color(self, img, parameters):
        return img.meanColor()

    def largest_blob_area(self, img, parameters):
        blobs = img.findBlobs(**parameters)
        
        if blobs:
            return blobs[-1].area()
        
        return None
    
    
#   def __json__(self):   
