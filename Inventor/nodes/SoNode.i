%rename(getByName_nam_pal) SoNode::getByName(const SbName & name, SoNodeList & l);

%feature("shadow") SoNode::getByName(const SbName & name) %{
def getByName(*args):
   if len(args) == 3:
      return apply(_pivy.SoNode_getByName_nam_pal,args)
   return apply(_pivy.SoNode_getByName,args)
%}
