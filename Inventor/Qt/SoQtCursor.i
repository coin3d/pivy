%rename(SoQtCursor_sha) SoQtCursor::SoQtCursor(const Shape shape);
%rename(SoQtCursor_cc) SoQtCursor::SoQtCursor(const SoQtCursor::CustomCursor * cc);

%feature("shadow") SoQtCursor::SoQtCursor %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      if isinstance(args[0], CustomCursor):
         newobj = apply(_pivy.new_SoQtCursor_cc,args)
      else:
         newobj = apply(_pivy.new_SoQtCursor_sha,args)
   else:
      newobj = apply(_pivy.new_SoQtCursor,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}
