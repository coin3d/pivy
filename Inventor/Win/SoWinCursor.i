%rename(SoWinCursor_sha) SoWinCursor::SoWinCursor(const Shape shape);
%rename(SoWinCursor_cc) SoWinCursor::SoWinCursor(const SoWinCursor::CustomCursor * cc);

%feature("shadow") SoWinCursor::SoWinCursor %{
def __init__(self,*args):
   if len(args) == 1:
      if isinstance(args[0], CustomCursor):
         self.this = apply(_pivy.new_SoWinCursor_cc,args)
         self.thisown = 1
         return
      else:
         self.this = apply(_pivy.new_SoWinCursor_sha,args)
         self.thisown = 1
         return
   self.this = apply(_pivy.new_SoWinCursor,args)
   self.thisown = 1
%}
