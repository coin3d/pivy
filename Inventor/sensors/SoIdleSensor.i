%rename(SoIdleSensor_scb_v) SoIdleSensor::SoIdleSensor(SoSensorCB * func, void * data);

%feature("shadow") SoIdleSensor::SoIdleSensor %{
def __init__(self,*args):
   if len(args) == 2:
      args = (args[0], (args[0], args[1]))
      self.this = apply(_pivy.new_SoIdleSensor_scb_v,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SoIdleSensor,args)
   self.thisown = 1
%}
