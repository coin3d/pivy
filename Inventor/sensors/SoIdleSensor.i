%rename(SoIdleSensor_scb_v) SoIdleSensor::SoIdleSensor(SoSensorCB * func, void * data);

%feature("shadow") SoIdleSensor::SoIdleSensor %{
def __init__(self,*args):
   newobj = None
   if len(args) == 2:
      args = (args[0], (args[0], args[1]))
      newobj = apply(_pivy.new_SoIdleSensor_scb_v,args)
   else:
      newobj = apply(_pivy.new_SoIdleSensor,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}
