%rename(apply_nod) SoAction::apply(SoNode *root);
%rename(apply_pat) SoAction::apply(SoPath *path);
%rename(apply_act) SoAction::apply(SoAction *beingApplied);

%feature("shadow") SoAction::apply(const SoPathList &pathlist, SbBool obeysrules=FALSE) %{
def apply(*args):
   if len(args) == 2:
      if isinstance(args[1], SoNode):
         return apply(_pivy.SoAction_apply_nod,args)
      elif isinstance(args[1], SoPath):
         return apply(_pivy.SoAction_apply_pat,args)
      elif isinstance(args[1], SoAction):
         return apply(_pivy.SoAction_apply_act,args)
   return apply(_pivy.SoAction_apply,args)
%}

%rename(popCurPath_pc) SoAction::popCurPath(const PathCode prevpathcode);

%feature("shadow") SoAction::popCurPath(void) %{
def popCurPath(*args):
   if len(args) == 2:
      return apply(_pivy.SoAction_popCurPath_pc,args)
   return apply(_pivy.SoAction_popCurPath,args)
%}

%rename(pushCurPath_i_nod) SoAction::pushCurPath(const int childindex, SoNode *node=NULL);

%feature("shadow") SoAction::pushCurPath(void) %{
def popCurPath(*args):
   if len(args) >= 2:
      return apply(_pivy.SoAction_pushCurPath_i_nod,args)
   return apply(_pivy.SoAction_pushCurPath,args)
%}
