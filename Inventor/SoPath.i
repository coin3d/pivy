%rename(SoPath_nod) SoPath::SoPath(SoNode * const head);
%rename(SoPath_pat) SoPath::SoPath(const SoPath & rhs);

%feature("shadow") SoPath::SoPath %{
def __init__(self,*args):
   if isinstance(args[0], SoNode):
      self.this = apply(_pivy.new_SoPath_nod,args)
      self.thisown = 1
      return
   elif isinstance(args[0], SoPath):
      self.this = apply(_pivy.new_SoPath_pat,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SoPath,args)
   self.thisown = 1
%}

%rename(append_nod) SoPath::append(SoNode * const node);
%rename(append_pat) SoPath::append(const SoPath * const frompath);

%feature("shadow") SoPath::append(const int childindex) %{
def append(*args):
   if isinstance(args[1], SoNode):
      return apply(_pivy.SoPath_append_nod,args)
   elif isinstance(args[1], SoPath):
      return apply(_pivy.SoPath_append_pat,args)
   return apply(_pivy.SoPath_append,args)
%}

%rename(getByName_nam_pal) SoPath::getByName(const SbName name, SoPathList & l);

%feature("shadow") SoPath::getByName(const SbName name) %{
def getByName(*args):
   if len(args) == 3:
      return apply(_pivy.SoPath_getByName_nam_pal,args)
   return apply(_pivy.SoPath_getByName,args)
%}

%rename(SoPath_eq) operator==(const SoPath & lhs, const SoPath & rhs);
%rename(SoPath_neq) operator!=(const SoPath & lhs, const SoPath & rhs);
