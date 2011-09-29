from base import *
from Session import *
from Statistic import Statistic

class Inspection(ming.MappedClass):
    class __mongometa__:
        session = Session().mingsession
        name = 'inspection'

    _id = FieldProperty(schema.ObjectId)    
    title = Field(str)
    test_type = Field(str) 
    roi_method = Field(str)#this might be a relation 
    roi_parameters = Field(ming.schema.Array)
    statistics = RelationProperty('Statistic')

    results = []
    samples = []
    showchart = False
    threshold = False
    threshold_event = False

    def __init__(self, roisource, statistics):
        self.roisource = roisource
        self.testsource = testsource
        self.roi_code = compile(roisource, "<string>", "exec")
                         
    def execute(self, frames):
        if not isinstance(frames, (list, tuple)):
            frames = [frames]
        
        roi_function_ref = getattr(self, roi_method)
            
        for frame in frames:
            samples, roi = roi_function_ref(*self.roi_parameters)
            
            for sample in samples:
            
                for s in statistics:
                    results = s.calculate(self.samples)
            
                    count = 0 
                    for r in results:
                        result.inspection = self
                        result.frame = frame
                        result.roi = roi
                        self.results.append[results]
                        #probably need to add unit conversion here
    def record(self)
        for r in results:
            results.m.save()
            
    def getResults(self):
        return [r.data for r in self.results]

    def clear():
        data = {}
        samples = []
        results = []
        
#    def __json__(self):
