/* add generic interface to access parts as attributes */
%extend SoBaseKit {
%pythoncode %{
   def __getattr__(self,name):
      if name == 'this' or name == 'thisown':
         return object.__getattr__(self,name)
      c = _pivy.SoBaseKit_getNodekitCatalog(self)
      if c.getPartNumber(name) >= 0:
         part = self.getPart(name,1)
         return part
      raise AttributeError()

   def __setattr__(self,name,value):
      if name == 'this' or name == 'thisown':
         return object.__setattr__(self,name,value)
      c = _pivy.SoBaseKit_getNodekitCatalog(self)
      if c.getPartNumber(name) >= 0:
         return self.setPart(name, value)
      return object.__setattr__(self,name,value)
%}
}
