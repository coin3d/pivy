%rename(SbViewportRegion_ss) SbViewportRegion::SbViewportRegion(short width, short height);
%rename(SbViewportRegion_vec) SbViewportRegion::SbViewportRegion(SbVec2s winSize);
%rename(SbViewportRegion_vr) SbViewportRegion::SbViewportRegion(const SbViewportRegion & vpReg);

%feature("shadow") SbViewportRegion::SbViewportRegion %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      if isinstance(args[0], SbVec2s):
         newobj = apply(_pivy.new_SbViewportRegion_vec,args)
      else:
         newobj = apply(_pivy.new_SbViewportRegion_vr,args)
   elif len(args) == 2:
      newobj = apply(_pivy.new_SbViewportRegion_ss,args)
   else:   
      newobj = apply(_pivy.new_SbViewportRegion,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}

%rename(setWindowSize_ss) SbViewportRegion::setWindowSize(short width, short height);

%feature("shadow") SbViewportRegion::setWindowSize(SbVec2s winSize) %{
def setWindowSize(*args):
   if len(args) == 3:
      return apply(_pivy.SbViewportRegion_setWindowSize_ss,args)
   return apply(_pivy.SbViewportRegion_setWindowSize,args)
%}

%rename(setViewport_ffff) SbViewportRegion::setViewport(float left, float bottom, float width, float height);

%feature("shadow") SbViewportRegion::setViewport(SbVec2f origin, SbVec2f size) %{
def setViewport(*args):
   if len(args) == 5:
      return apply(_pivy.SbViewportRegion_setViewport_ffff,args)
   return apply(_pivy.SbViewportRegion_setViewport,args)
%}

%rename(setViewportPixels_ssss) SbViewportRegion::setViewportPixels(short left, short bottom, short width, short height);

%feature("shadow") SbViewportRegion::setViewportPixels(SbVec2s origin, SbVec2s size) %{
def setViewportPixels(*args):
   if len(args) == 5:
      return apply(_pivy.SbViewportRegion_setViewportPixels_ssss,args)
   return apply(_pivy.SbViewportRegion_setViewportPixels,args)
%}

/* add operator overloading methods instead of the global functions */
%extend SbViewportRegion {    
    int __eq__( const SbViewportRegion &u )
    {
        return *self == u;
    };
    
    int __ne__( const SbViewportRegion &u )
    {
        return !(*self == u );
    };
}
