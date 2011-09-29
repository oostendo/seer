from base import *

class Session():
    __shared_state = { }
    
    def __init__(self, json_config = ''):
        self.__dict__ = self.__shared_state
        
        if not json_config:
            return
        
        self.__dict__.clear()  
        config = json.load(open(json_config))
        for k in config.keys():
            self.__dict__[k] = config[k]
        
        self.bind = DataStore(self.mongo, database = self.database)
        self.mingsession = ming.Session(self.bind)

        
    def __getattr__(self, attr):
        return ''  #return false on any non-present properties
    
    def __str__(self):
        return "Seer Session Object"