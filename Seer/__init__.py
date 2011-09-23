from Seer import *

if __name__ == '__main__':
    if (len(sys.argv) > 1):
       config_file = sys.argv[1] 
    else:
       config_file = "seer.cnf"
    Seer(config_file).start()
