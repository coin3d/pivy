/* add generic interface to access parts as attributes */
%extend SoBaseKit {
%pythoncode %{
    def __getattr__(self,name):
        try:
            return SoNode.__getattr__(self, name)
        except AttributeError, e:
            c = _coin.SoBaseKit_getNodekitCatalog(self)
            if c.getPartNumber(name) >= 0:
                part = self.getPart(name,1)
                return part
            raise e

    def __setattr__(self,name,value):
       if name == 'this':
          return SoNode.__setattr__(self,name,value)
       c = _coin.SoBaseKit_getNodekitCatalog(self)
       if c.getPartNumber(name) >= 0:
          return self.setPart(name, value)
       return SoNode.__setattr__(self,name,value)       
%}
}
