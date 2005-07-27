%rename(SoWriteAction_out) SoWriteAction::SoWriteAction(SoOutput * out);

%feature("shadow") SoWriteAction::SoWriteAction %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      newobj = apply(_coin.new_SoWriteAction_out,args)
   else:
      newobj = apply(_coin.new_SoWriteAction,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}

%rename(continueToApply_nod) SoWriteAction::continueToApply(SoNode * node);

%feature("shadow") SoWriteAction::continueToApply(SoPath * path) %{
def continueToApply(*args):
   if isinstance(args[1], SoNode):
      return apply(_coin.SoWriteAction_continueToApply_nod,args)
   return apply(_coin.SoWriteAction_continueToApply,args)
%}
