typedef int uint32_t;

%rename(SoDelayQueueSensor_scb_v) SoDelayQueueSensor::SoDelayQueueSensor(SoSensorCB * func, void * data);

%feature("shadow") SoDelayQueueSensor::SoDelayQueueSensor %{
def __init__(self,*args):
   if len(args) == 2:
      args = (args[0], (args[0], args[1]))
      self.this = apply(_pivy.new_SoDelayQueueSensor_scb_v,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SoDelayQueueSensor,args)
   self.thisown = 1
%}
