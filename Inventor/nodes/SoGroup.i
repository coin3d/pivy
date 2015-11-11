%extend SoGroup {
/* extend __iter__ to return a new iterator object */
%pythoncode %{
   def __iter__(self):
      i = 0
      while i < self.getNumChildren():
         yield self.getChild(i)
         i += 1
%}

  /* methods to emulate Python Container object */
  int __len__(void) { return self->getNumChildren(); }
  int __contains__(const SoNode * node ) { return (self->findChild(node) != -1); }
  SoNode * __getitem__(int index) { return self->getChild(index); }
}
