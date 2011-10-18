from base import *

def displayManagerProcess(master_pipe, resolution = (800, 600), host = ""):
    d = Display(resolution = resolution)

    js = ''
    if host:
    	js = JpegStreamer(host + ":8081")

    count = 0
    while True:
        size, buff = master_pipe.recv()
	#print "received image %d" % count 
 	bitmap = cv.CreateImageHeader(size, cv.IPL_DEPTH_8U, 3)
	cv.SetData(bitmap, buff)
	i = Image(bitmap)
	if i == "quit" or d.isDone():
	     break
    	i.save(d)
  	if js: 
            i.save(js)
	count = count + 1

    master_pipe.send("quit")
    master_pipe.close()
     
class DisplayManager:
    c = ""
    lastframe = ""
    display_pipe = ''
    display_process = ""

    def __init__(self, resolution = (800,600), host = ""):
        self.display_pipe,master_pipe = Pipe() 
        self.display_process = Process(target=displayManagerProcess, args=(master_pipe,resolution, host,))
        self.display_process.daemon = True
        self.display_process.start()

    def send(image):
	self.lastframe = image 
        self.imagecount = self.imagecount + 1
	display_pipe.send((self.lastframe.size(), self.lastframe.getBitmap().tostring()))
	time.sleep(0.04)

