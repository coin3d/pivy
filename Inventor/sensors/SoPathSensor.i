%rename(SoPathSensor_scb_v) SoPathSensor::SoPathSensor(SoSensorCB * func, void * data);

%feature("shadow") SoPathSensor::SoPathSensor %{
def __init__(self,*args):
   if len(args) == 2:
      args = (args[0], (args[0], args[1]))
      self.this = apply(_pivy.new_SoPathSensor_scb_v,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SoPathSensor,args)
   self.thisown = 1
%}
