from base import *
from Seer import Seer

class Frame(Document):
    class __mongometa__:
        session = Seer().session
        name = 'frame'

    _id = Field(schema.ObjectId)
    capturetime = Field(float)
    camera = Field(str)
    _height = Field(int, if_missing = 0)
    _width = Field(int, if_missing = 0)
    _image = Field(schema.Binary) #a base64 encoded image

    @apply
    def image():
       def fget(self):
          bitmap = cv.CreateImageHeader((self._width, self._height), cv.IPL_DEPTH_8U, 3)
          cv.SetData(bitmap, self._image)
          #need to find some way to cache this
          
          return Image(bitmap)
          
       def fset(self, img):
          self._width, self._height = img.size()
          self._image = bson.Binary(img.getBitmap().tostring())
          
       return property(fget, fset)
       
