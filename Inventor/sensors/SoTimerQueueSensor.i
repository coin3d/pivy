%rename(SoTimerQueueSensor_scb_v) SoTimerQueueSensor::SoTimerQueueSensor(SoSensorCB * func, void * data);

%feature("shadow") SoTimerQueueSensor::SoTimerQueueSensor %{
def __init__(self,*args):
   if len(args) == 2:
      args = (args[0], (args[0], args[1]))
      self.this = apply(_pivy.new_SoTimerQueueSensor_scb_v,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SoTimerQueueSensor,args)
   self.thisown = 1
%}
