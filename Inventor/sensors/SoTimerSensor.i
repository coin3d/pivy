%rename(SoTimerSensor_scb_v) SoTimerSensor::SoTimerSensor(SoSensorCB * func, void * data);

%feature("shadow") SoTimerSensor::SoTimerSensor %{
def __init__(self,*args):
   if len(args) == 2:
      args = (args[0], (args[0], args[1]))
      self.this = apply(_pivy.new_SoTimerSensor_scb_v,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SoTimerSensor,args)
   self.thisown = 1
%}
