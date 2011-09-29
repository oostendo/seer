import sys, time, os
import threading
import json
from multiprocessing import Process, Queue, Pipe
import threading

import cherrypy
try:
  import Image as pil
except(ImportError):
  import PIL.Image as pil

import cv
import IPython.Shell
import pyfirmata
import bson
import ming
import ming.orm
from ming.datastore import DataStore
from ming.orm.declarative import MappedClass


import SimpleCV
#from SimpleCV.Shell import *
from SimpleCV import Image, JpegStreamer, Camera
#from SimpleCV.Display import Display
