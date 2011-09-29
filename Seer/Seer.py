from base import *
from Session import Session
#import Shell

class Seer(threading.Thread):
    __shared_state = { "initialized": False } 
#    cameras = []
#    shell_thread = ''
#    display = ''
#    camera_on = 0
#    lastframes = []
#    config = {}
#    framecount = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        #ActiveState "Borg" Singleton replacement design
        if self.initialized:
            return  #successive calls to Seer simply return the borg'd object

        #read config file
        self.config = Session()

        self.cameras = []
        for camera in self.config.cameras:
            id = camera['id']
            del camera['id']
            self.cameras.append(Camera(id, camera))
        #log initialized camera X

        self.inspections = []
        #self.inspections = Inspection.m.find( { "enabled": 1 }).all()
         
        self.conditions = []
        #self.conditions = Events.m.find( { "enabled": 1 }).all()

        #self.display = Display()
        self.lastframes = []
        self.framecount = 0
        #log display started

        #self.web = Web(self.config['web'])

        #self.controls = Controls(self.config['arduino'])
        
        if self.config.start_shell:
            self.shell_thread = Shell.Shell()
            self.shell_thread.setDaemon(True)
            self.shell_thread.start()
        
        self.initialized = True
        super(Seer, self).__init__()

    def capture(self):
        count = 0
        currentframes = []
        for c in self.cameras:
            img = c.getImage()
            frame = Frame.make({"capturetime": time.time(), 
                "camera": self.config.cameras[count]['name']})
            frame.image = img
            
            if self.config.record_all:
                frame.save()
            
            currentframes.append(frame)
            self.lastframes.append(frame)
            
            while len(self.lastframes) > self.config.max_frames:
                self.lastframes.popleft()
                            
            self.framecount = self.framecount + 1
            count = count + 1

    def run(self):
        while True:
            timer_start = time.time()
            frames = self.capture()
            
            for inspection in self.inspections:
                data = inspection.execute(frames)
                for event in self.conditions:
                    if event.test(data):
                        event.execute()
            
            self.display.send(frames)
            
            timeleft = poll_interval - (time.time() - timerstart)
            if timeleft > 0:
                time.sleep(timeleft)
            else:
                time.sleep(0)
            
from Frame import Frame        