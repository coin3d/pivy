%rename(SoOneShotSensor_scb_v) SoOneShotSensor::SoOneShotSensor(SoSensorCB * func, void * data);

%feature("shadow") SoOneShotSensor::SoOneShotSensor %{
def __init__(self,*args):
   if len(args) == 2:
      args = (args[0], (args[0], args[1]))
      self.this = apply(_pivy.new_SoOneShotSensor_scb_v,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SoOneShotSensor,args)
   self.thisown = 1
%}
