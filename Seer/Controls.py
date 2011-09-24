from base import *

class Widget:
   pin_id = -1
   state = 0

   def read(self, value): 
         self.value = value
         self.state = value
   
class Button(Widget):
     pass

class Knob(Widget):
     pass

class Controls():
    iterator = ''
    board = ''

    buttons = []
    knobs = []
    lights = [] 

    def __init__(self, config):
       buttons = []
       knobs = []
       lights = []

       for control in sorted(config.keys()):
           if control.find('button'):
               buttons.append(Button(config[control])) 
           elif control.find('knob'):
               knobs.append(Knob(config[knob]))
           elif control.find('light'):
               lights.append(Light())     

