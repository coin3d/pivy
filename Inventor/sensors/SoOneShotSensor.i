%rename(SoOneShotSensor_scb_v) SoOneShotSensor::SoOneShotSensor(SoSensorCB * func, void * data);

%feature("shadow") SoOneShotSensor::SoOneShotSensor %{
def __init__(self,*args):
   newobj = None
   if len(args) == 2:
      args = (args[0], (args[0], args[1]))
      newobj = apply(_pivy.new_SoOneShotSensor_scb_v,args)
   else:
      newobj = apply(_pivy.new_SoOneShotSensor,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
%}
