%rename(SoWriteAction_out) SoWriteAction::SoWriteAction(SoOutput * out);

%feature("shadow") SoWriteAction::SoWriteAction %{
def __init__(self,*args):
   if len(args) == 1:
      self.this = apply(_pivy.new_SoWriteAction_out,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SoWriteAction,args)
   self.thisown = 1
%}

%rename(continueToApply_nod) SoWriteAction::continueToApply(SoNode * node);

%feature("shadow") SoWriteAction::continueToApply(SoPath * path) %{
def continueToApply(*args):
   if isinstance(args[1], SoNode):
      return apply(_pivy.SoWriteAction_continueToApply_nod,args)
   return apply(_pivy.SoWriteAction_continueToApply,args)
%}
