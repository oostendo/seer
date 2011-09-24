from base import *

class Seer(Threading.thread):
    __shared_state = {} 
#    cameras = []
#    shell_thread = ''
#    display = ''
#    camera_on = 0
#    lastframes = []
#    config = {}
#    framecount = {}

    def __init__(self, config):
        self.__dict__ = self.__shared_state
	#ActiveState "Borg" Singleton replacement design
        if not self.config:
            return

 	#read config file
	self.configure(config)

        self.cameras = []
        for camera in self.config[cameras]:
            id = camera[id]
            del camera[id]
            self.cameras.append(Camera(id, camera))
        #log initialized camera X

	self.display = Display(self.config.display)
        self.lastframes = []
        #log display started

        self.web = Web()

        self.bind = DataStore(self.config.mongo, self.config.database)
        self.session = Session(self.bind) 

        self.controls = Controls(self.config.arduino)
        
        shell_thread = Shell()
        shell_thread.setDaemon(True)
        shell_thread.start()

    def configure(self, config):
        json_config = ''
        json_config = open(config)
        self.config = json.load(json_config)     
        #log event, config reloaded

    def capture(self)
        for c in self.cameras:
           img = c.getImage()
           frame = Frame(time: time.time(), 
               size: img.size(),
               image: img.getBitmap().tostring(),
               camera: c.getId())

           self.lastframes.append(frame) 	   
           if self.config.has_key(record_all) and self.config['record_all']:
               frame.save()
	   
           self.framecount = self.framecount + 1

    def run(self):
        while True:
	    self.capture() 
            foreach  
            self.display.send(self.lastframes)
