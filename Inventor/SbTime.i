%rename(SbTime_d) SbTime::SbTime(const double sec);
%rename(SbTime_i_l) SbTime::SbTime(const int32_t sec, const long usec);
%rename(SbTime_tv) SbTime::SbTime(const struct timeval * const tv);

%feature("shadow") SbTime::SbTime %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      if type(args[0]) == type(1.0):
         newobj = apply(_pivy.new_SbTime_d,args)
      else:
         newobj = apply(_pivy.new_SbTime_tv,args)
   elif len(args) == 2:
      newobj = apply(_pivy.new_SbTime_i_l,args)
   else:
      newobj = apply(_pivy.new_SbTime,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}

%rename(setValue_i_l) SbTime::setValue(const int32_t sec, const long usec);
%rename(setValue_tv) SbTime::setValue(const struct timeval * const tv);

%feature("shadow") SbTime::setValue(const double sec) %{
def setValue(*args):
   if len(args) == 2:
      if type(args[1]) == type(1.0):
         return apply(_pivy.SbTime_setValue,args)
      elif type(args[1]) == SbTime:
         return _pivy.SbTime_setValue(args[0],args[1].getValue())
      else:
         return apply(_pivy.SbTime_setValue_tv,args)
   elif len(args) == 3:
      return apply(_pivy.SbTime_setValue_i_l,args)   
   return apply(_pivy.SbTime_setValue,args)
%}

/* add operator overloading methods instead of the global functions */
%extend SbTime {
    SbTime __add__(const SbTime &u)
    {
        return *self + u;
    };
    
    SbTime __sub__(const SbTime &u)    
    {
       return *self - u;
    };
    
    SbTime __mul__(const double d)
    {
       return *self * d;
    };
    
    SbTime __rmul__(const double d)
    {
           return *self * d;
    };
    
    SbTime __div__(const double d)
    {
        return *self / d;
    };
}

%ignore SbTime::getValue(time_t & sec, long & usec) const;
%ignore SbTime::getValue(struct timeval * tv) const;
