%rename(SoQtCursor_sha) SoQtCursor::SoQtCursor(const Shape shape);
%rename(SoQtCursor_cc) SoQtCursor::SoQtCursor(const SoQtCursor::CustomCursor * cc);

%feature("shadow") SoQtCursor::SoQtCursor %{
def __init__(self,*args):
   if len(args) == 1:
      if isinstance(args[0], CustomCursor):
         self.this = apply(_pivy.new_SoQtCursor_cc,args)
         self.thisown = 1
         return
      else:
         self.this = apply(_pivy.new_SoQtCursor_sha,args)
         self.thisown = 1
         return
   self.this = apply(_pivy.new_SoQtCursor,args)
   self.thisown = 1
%}
