%rename(SbName_char) SbName::SbName(const char * nameString);
%rename(SbName_str) SbName::SbName(const SbString & str);
%rename(SbName_name) SbName::SbName(const SbName & name);

%feature("shadow") SbName::SbName %{
def __init__(self,*args):
   if len(args) == 1:
      if isinstance(args[0], SbName):
         self.this = apply(_pivy.new_SbName_str,args)
         self.thisown = 1
         return
      elif isinstance(args[0], SbName):
         self.this = apply(_pivy.new_SbName_name,args)
         self.thisown = 1
         return
      else:
         self.this = apply(_pivy.new_SbName_char,args)
         self.thisown = 1
         return
   self.this = apply(_pivy.new_SbName,args)
   self.thisown = 1
%}
