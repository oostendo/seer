from base import *

class Seer(Threading.thread):
    __shared_state = {} 
    cameras = []
    shell_thread = ''
    display = ''
    camera_on = 0
    lastframes = []

    def __init__(self, config):
        self.__dict__ = self.__shared_state
	#ActiveState "Borg" Singleton replacement design

 	#read config file
        self.cameras = []
        for id in camera_ids:
            self.cameras.append(Camera(id))

        shell_thread = Shell()
        shell_thread.setDaemon(True)
        shell_thread.start()

	self.display = Display()
        self.lastframes = []

    def run(self):
        while True:
            count = 0
            for c in self.cameras:
                self.lastframes[count] = c.getImage()
                count = count + 1

            self.display.send(self.lastframes[self.camera_on])
