
import sys, time
from multiprocessing import Process, Queue, Pipe

import cherrypy
import Image as pil
import cv
import IPython.Shell

import SimpleCV
from SimpleCV.Shell import *
from SimpleCV import Image, JpegStreamer, Camera
from SimpleCV.Display import Display
