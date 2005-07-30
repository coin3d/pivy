%extend SoMField {
/* shadow __iter__ to return a new iterator object */
%pythoncode %{
   def __iter__(self):
      i = 0
      while i < self.getNum():
         yield self[i]
         i += 1
%}
// TODO: write a get1 method that returns a string as a result
}
