%rename(SbTime_d) SbTime::SbTime(const double sec);
%rename(SbTime_i_l) SbTime::SbTime(const int32_t sec, const long usec);
%rename(SbTime_tv) SbTime::SbTime(const struct timeval * const tv);

%feature("shadow") SbTime::SbTime %{
def __init__(self,*args):
   if len(args) == 1:
      if type(args[0]) == type(1.0):
         self.this = apply(_pivy.new_SbTime_d,args)
         self.thisown = 1
         return
      else:
         self.this = apply(_pivy.new_SbTime_tv,args)
         self.thisown = 1
         return      
   elif len(args) == 2:
      self.this = apply(_pivy.new_SbTime_i_l,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SbTime,args)
   self.thisown = 1
%}

%rename(setValue_d) SbTime::setValue(const double sec);
%rename(setValue_i_l) SbTime::setValue(const int32_t sec, const long usec);
%rename(setValue_tv) SbTime::setValue(const struct timeval * const tv);

%feature("shadow") SbTime::setValue(const float vec[2]) %{
def setValue(*args):
   if len(args) == 2:
      if type(args[0]) == type(1.0):
         return apply(_pivy.SbTime_setValue_d,args)
      else:
         return apply(_pivy.SbTime_setValue_tv,args)
   elif len(args) == 2:
      return apply(_pivy.SbTime_setValue_i_l,args)   
   return apply(_pivy.SbTime_setValue,args)
%}

%rename(SbTime_add) operator+(const SbTime & t0, const SbTime & t1);
%rename(SbTime_sub) operator-(const SbTime & t0, const SbTime & t1);
%rename(SbTime_d_mul) operator *(const double s, const SbTime & tm);
%rename(SbTime_mul) operator *(const SbTime & tm, const double s);
%rename(SbTime_div) operator /(const SbTime & tm, const double s);

%ignore SbTime::getValue(time_t & sec, long & usec) const;
%ignore SbTime::getValue(struct timeval * tv) const;
