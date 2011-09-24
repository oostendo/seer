from base import *
from Seer.Statistic import Statistic

class Inspection(MappedClass):
    class __mongometa__:
        session = session
        name = 'inspection'

    _id = FieldProperty(schema.ObjectId)    
    title = Field(str)
    test_type = Field(str) 
    roi_code = Field(str)#this might be a relation 
    statistics = RelationProperty('Statistic') 
    data = {}
    samples = []
    unit = "mm"
    showchart = False
    threshold = False
    threshold_event = False

    def __init__(self, roisource, statistics):
	self.roisource = roisource
        self.testsource = testsource
        self.roi_code = compile(roisource, "<string>", "exec")
        self.statistics = statistics

    def addSample(self, img):
	roi_origin, roi_offset = exec(self.roi_code)
        if not roi_offset[0]:
            return
        #calculate where we should be looking in the image, skip if no match

        if type(img) != 'array':
             img = [img]

        for i in img:
            self.samples.append(i.crop(roi_origin[0], roi_origin[1], roi_offset[0], roi_offset[1]))
        #add the images into samples
                         
    def calc(self):
        for s in statistics:
            key, val = s.calc(self.samples)
            self.data[key] = val

    def getData(self):
        return [self.data[k] for k in sorted(self.data.keys())]

    def clear():
        data = {}
        samples = []
        
#    def __json__(self):
