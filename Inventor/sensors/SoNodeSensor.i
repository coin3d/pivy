%rename(SoNodeSensor_scb_v) SoNodeSensor::SoNodeSensor(SoSensorCB * func, void * data);

%feature("shadow") SoNodeSensor::SoNodeSensor %{
def __init__(self,*args):
   if len(args) == 2:
      args = (args[0], (args[0], args[1]))
      self.this = apply(_pivy.new_SoNodeSensor_scb_v,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SoNodeSensor,args)
   self.thisown = 1
%}
