%rename(getPosition_vpr) SoEvent::getPosition(const SbViewportRegion & vpRgn) const;

%feature("shadow") SoEvent::getPosition(void) %{
def getPosition(*args):
   if len(args) == 2:
      return apply(_pivy.SoEvent_getPosition_vpr,args)
   return apply(_pivy.SoEvent_getPosition,args)
%}
