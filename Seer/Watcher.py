from base import *
from Session import Session

class Watcher(MappedClass):
    """
    w = Watcher(
        name = "blob is big enough",
        conditions = ["threshold_greater"],
        handlers = ["log_statistics"],
        enabled = 1,
        parameters = { "threshold_greater": {
            "threshold": 5000,
            "samples": 5,
            "measurement_name": "Largest Blob",
            "label": "area" })
    
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
    
    
    def threshold_greater(self, threshold, measurement_name, label, samples = 1):
        resultset = Seer().results[-samples:]
        measurement = Measurement.query.get( name = measurement_name )
        if not measurement:
            return False
        
        result_index = measurement.result_labels.index(label)
        if result_index == None:
            return False
        
        result_set = [ r for r in list if r.measurement_id == measurement._id ]
        
        stat = Statistic( {
            name: "Average of " + measurement_name,
            capturetime: time.time()
        })
        #MOVE THE ABOVE STUFF TO A DECORATOR
        
        stat.calculate(result_set, 'mean', np.mean)
        if stat.data[measurement._id][result_index] > threshold:
            return stat
        return False
    
    def log_statistics(self, statistics):
        for stat in statistics:
            stat.saveResults()
            stat.m.save()
    
    
ming.orm.Mapper.compile_all()   
