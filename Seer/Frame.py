from base import *
from Session import Session

"""
    f = Frame({ 
      capturetime = time.time(),
      camera = "0" })
      
    f.image(Seer().cameras[0].


"""
class Frame(ming.Document):
    class __mongometa__:
        session = Session().mingsession
        name = 'frame'

    _id = ming.Field(ming.schema.ObjectId)
    capturetime = ming.Field(float)
    camera = ming.Field(str)
    _height = ming.Field(int, if_missing = 0)
    _width = ming.Field(int, if_missing = 0)
    _image = ming.Field(ming.schema.Binary) #a base64 encoded image

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
       
