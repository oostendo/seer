from base import *
from Session import Session

class Watcher(MappedClass):
    """
    The Watcher reviews results in Seer, and has two handler patterns:
      - self.conditions takes any parameters in the Parameters object
        and returns a Statistic object.  Multiple conditions can be added and
        are considered implicitly ANDed.  It must refer to a class method.
      - self.handlers are function references that are fired if all conditions return statistic objects,
        and must be a class method.  They are sent the statistics as their parameter.
    
    A typical watcher will have a sample size, and wil look in the Seer() to see
    the most recently recorded measurements.  It can check state on the entire system,
    and may potentially reference the Web, Control, and Display interfaces.  They
    also are responsible for recording any Results and Statistics.    
    
    w = Watcher(
        name = "blob is big enough",
        enabled = 1,
        parameters = { "threshold_greater": {
            "threshold": 5000,
            "samples": 5,
            "measurement_name": "Largest Blob",
            "label": "area" })
    
        conditions = ["threshold_greater"],
        handlers = ["log_statistics"])
    w.check()
    """
    class __mongometa__:
        session = Session().mingsession()
        name = 'watcher'
        
    _id = ming.Field(ming.schema.ObjectId)    
    name = ming.Field(str)
    conditions = ming.Field(ming.schema.Array(str))
    handlers = ming.Field(ming.schema.Array(str))#this might be a relation 
    enabled = ming.Field(int)
    parameters = ming.Field(ming.schema.Object)
    
    def check(self):
        """
        When the wather runs check, each of its conditions are checked.  If
        all conditions return Statistic objects, they are sent to each
        handler.
        """
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
