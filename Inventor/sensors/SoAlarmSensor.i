%rename(SoAlarmSensor_scb_v) SoAlarmSensor::SoAlarmSensor(SoSensorCB * func, void * data);

%feature("shadow") SoAlarmSensor::SoAlarmSensor %{
def __init__(self,*args):
   if len(args) == 2:
      args = (args[0], (args[0], args[1]))
      self.this = apply(_pivy.new_SoAlarmSensor_scb_v,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SoAlarmSensor,args)
   self.thisown = 1
%}
