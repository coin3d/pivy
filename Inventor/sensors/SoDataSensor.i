%rename(SoDataSensor_scb_v) SoDataSensor::SoDataSensor(SoSensorCB * func, void * data);

%feature("shadow") SoDataSensor::SoDataSensor %{
def __init__(self,*args):
   if len(args) == 2:
      args = (args[0], (args[0], args[1]))
      self.this = apply(_pivy.new_SoDataSensor_scb_v,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SoDataSensor,args)
   self.thisown = 1
%}
