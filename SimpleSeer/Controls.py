from base import *

class ControlObject:
    """
	An abstract class for all objects -- controls Arduino pin assignment 
	and previous state

	This needs to be fleshed out

    """
   pin = '' 
   state = 0
   statechange = False 
   handlers = set() 

   def __init__(self, board, config):
       board.digital[pin_added].enable_reporting()
       self.pin = board.get_pin('d:%d:i' % config['pin'])
       handers = set() 
       for handler in config['handlers'] {
           handlers.add(getattr(self, handler))
       }

   def read(self): 
         newstate = self.pin.read()
         if newstate != self.state: #need to add some "smoothing" here probably
             self.state = newstate
             self.fire(newstate) 

   def fire(self, *args, **kargs):
       for function_ref in handlers:
          function_ref(self, *args, **kargs)   
           
class Button(ControlObject):
     pass

class Knob(ControlObject):
     pass

class Controls():
    iterator = ''
    board = ''

    buttons = []
    knobs = []
    lights = [] 
    pins = {} 

    def __init__(self, config):
       buttons = []
       knobs = []
       lights = []
       pins = {} 

       #
       board = Arduino(config['board'])
       it = util.Iterator(board)
       it.start()
       config['board']

       for control in sorted(config.keys()):
           pin_added = ''
           if control.find('button'):
               buttons.append(Button(config[control])) 
               pin_added = config['control'][pin] 
           elif control.find('knob'):
               knobs.append(Knob(config[control]))
               pin_added = config['control'][pin] 
               board.analog[pin_added].enable_reporting()
           elif control.find('light'):
               lights.append(Light(config[control]))     
               pin_added = config['control'][pin] 
                

