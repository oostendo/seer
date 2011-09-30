from base import *
from Session import Session

class Watcher(MappedClass):
    """
    w = Watcher(
        name = "blob is big enough",
        conditions = ["threshold_greater"],
        handlers = ["log_statistics"],
        enabled = 1,
        parameters = { "threshold_greater": { "threshold": 5000, "samples: 5", "measurement": "Largest Blob", "label": "area" })
    
    w.check()
    """
    class __mongometa__:
        session = Session().getORMSession()
        name = 'watcher'
        
    _id = ming.orm.FieldProperty(ming.schema.ObjectId)    
    name = ming.orm.FieldProperty(str)
    conditions = ming.orm.FieldProperty(ming.schema.Array(str))
    handlers = ming.orm.FieldProperty(ming.schema.Array(str))#this might be a relation 
    enabled = ming.orm.FieldProperty(int)
    parameters = ming.orm.FieldProperty(ming.schema.Object)
    
    def check(self):
        statistics = []
        for condition in self.conditions:
            function_ref = getattr(self, condition)
            stat = function_ref(**self.parameters[condition])
            
            if not stat:
                return False
                
            statistics.append(stat)
    
        for handler in handlers:
            function_ref = getattr(self, condition)
            function_ref(statistics)
        
        return True
    
    
    def threshold_greater(self, threshold, samples, measurement, label):
        
    
    
    def log_statistics(self, statistics):
        for stat in statistics:
            stat.saveResults()
            stat.m.save()
    
    
ming.orm.Mapper.compile_all()   
