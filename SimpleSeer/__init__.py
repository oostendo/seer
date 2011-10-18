from base import *
from Session import Session

if __name__ == '__main__':
    if (len(sys.argv) > 1):
       config_file = sys.argv[1] 
    else:
       config_file = "../default.cfg"

    Session(config_file)

from SimpleSeer import SimpleSeer 
from Inspection import Inspection
from Measurement import Measurement
from Result import Result

if __name__ == '__main__':
    SimpleSeer()
    

