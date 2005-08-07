%rename(SoPath_nod) SoPath::SoPath(SoNode * const head);
%rename(SoPath_pat) SoPath::SoPath(const SoPath & rhs);

%feature("shadow") SoPath::SoPath %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      if isinstance(args[0], SoNode):
         newobj = apply(_coin.new_SoPath_nod,args)
      elif isinstance(args[0], SoPath):
         newobj = apply(_coin.new_SoPath_pat,args)
   else:
      newobj = apply(_coin.new_SoPath,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}

/* add operator overloading methods instead of the global functions */
%extend SoPath {      
  int __eq__(const SoPath &u) { return *self == u; }
  int __nq__(const SoPath &u) { return *self != u; }
}
