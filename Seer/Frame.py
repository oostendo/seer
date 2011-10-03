from base import *
from Session import Session

"""
    Frame Objects are a mongo-friendly wrapper for SimpleCV image objects,
    containing additional properties for the originating camera and time of capture.
    
    Note that Frame.image property must be used as a getter-setter.

    >>> f = Seer.capture()[0]  #get a frame from the Seer module
    >>> f.image.dl().line((0,0),(100,100))
    >>> f.save()
    >>> 
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
    _image = ming.Field(ming.schema.Binary) #binary image data
    _layer = ming.Field(ming.schema.Binary, if_missing = None) #layer data
    _imgcache = ming.Field(str, if_missing = '')

    @apply
    def image():
        def fget(self):
            if self._imgcache != '':
                return self._imgcache
            
            bitmap = cv.CreateImageHeader((self._width, self._height), cv.IPL_DEPTH_8U, 3)
            cv.SetData(bitmap, self._image)
            
            self._imgcache = Image(bitmap)
            if self._layer:
                self._imgcache.dl()._mSurface = pygame.image.fromstring(self._layer, self._imgcache.size(), "RGBA")
            
            return self._imgcache
            
          
        def fset(self, img):
            self._width, self._height = img.size()
            self._image = bson.Binary(img.getBitmap().tostring())
          
            if len(img._mLayers):
                if len(img._mLayers) > 1:
                    mergedlayer = DrawingLayer(img.size())
                    for layer in img._mLayers[::-1]:
                        layer.renderToOtherLayer(mergedlayer)
                else:
                    mergedlayer = img.dl()
                self._layer = bson.Binary(pygame.image.tostring(mergedlayer._mSurface, "RGBA"))
          
            self._imgcache = img
            
        return property(fget, fset)
       
    def __repr__(self):
       return "<Seer Frame Object %d,%d captured with '%s' at %f>" % (
            self._width, self._height, self.camera, self.capturetime) 
        
    def save(self):
        if self._imgcache != '':
            self.image = self._imgcache #encode any layer changes made before save
            self._imgcache = ''
        
        self.m.save()
       
