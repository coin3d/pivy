%rename(SoFieldSensor_scb_v) SoFieldSensor::SoFieldSensor(SoSensorCB * func, void * data);

%feature("shadow") SoFieldSensor::SoFieldSensor %{
def __init__(self,*args):
   if len(args) == 2:
      args = (args[0], (args[0], args[1]))
      self.this = apply(_pivy.new_SoFieldSensor_scb_v,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SoFieldSensor,args)
   self.thisown = 1
%}
