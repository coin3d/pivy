%rename(SoGroup_i) SoGroup::SoGroup(int nchildren);

%feature("shadow") SoGroup::SoGroup %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      newobj = apply(_coin.new_SoGroup_i,args)
   else:
      newobj = apply(_coin.new_SoGroup,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}
