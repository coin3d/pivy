%extend SoGroup {
/* extend __iter__ to return a new iterator object */
%pythoncode %{
   def __iter__(self):
      i = 0
      while i < self.getNumChildren():
         yield self.getChild(i)
         i += 1
%}
   /* FIXME: write a get1 method that returns a string as a
      result. 20050731 gerhard. */
  int __len__(void) { return self->getNumChildren(); }
}
