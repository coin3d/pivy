%rename(SoWinCursor_sha) SoWinCursor::SoWinCursor(const Shape shape);
%rename(SoWinCursor_cc) SoWinCursor::SoWinCursor(const SoWinCursor::CustomCursor * cc);

%feature("shadow") SoWinCursor::SoWinCursor %{
def __init__(self,*args):
   newobj = None
   if len(args) == 1:
      if isinstance(args[0], CustomCursor):
         newobj = apply(_sowin.new_SoWinCursor_cc,args)
      else:
         newobj = apply(_sowin.new_SoWinCursor_sha,args)
   else:
      newobj = apply(_sowin.new_SoWinCursor,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}
