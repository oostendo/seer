from base import *
from Session import Session


class Statistic(ming.Document):
    """
    
    s = Statistic( {
       "name": "average of frame" + Seer().framecount,
       "capturetime": time.time() }) #we may want to put another ID field on here
       
    s.processColumns(results, "average", np.mean)
    s.m.save()
    
    
    """
    class __mongometa__:
        session = Session().mingsession
        name = 'statistic'
    
    _id = ming.orm.FieldProperty(ming.schema.ObjectId)    
    
    data = ming.Field(ming.schema.Object)
    name = ming.Field(str)
    capturetime = ming.Field(float)
    results = ming.Field(ming.schema.Array(ming.schema.ObjectID))

    def saveResults(self):
        for r in self.unsavedresults:
            r.save()
            self.results.append(r)

        del self.__dict__['unsavedresults']

    def calculate(self, results, name, column_function):
        measurement_group = {}
        
        self.unsavedresults = []
        
        for r in results:
            if not measurement_sort.has_key(r.measurement_id):
                measurement_sort[r.measurement_id] = []
                
            measurement_group[r.measurement_id].append(r.float_data)
            if r._id:
                self.results.append(r)
            else:
                self.unsavedresults.append(r)
                
        
        for m_id in measurement_group.keys():
            measurement = Measurement.query.get( _id = m_id )
            if not measurement.is_numeric:
                continue
            
            data_table = np.array(measurement_group[m_id])
            
            count = 0
            for label in measurement.result_labels:
                self.data[m._id][label] = column_function(data_table[:,count])
                count = count + 1
                
    def save(self):
        if len(self.unsavedresults):
            self.saveResults()
            self.m.save()
