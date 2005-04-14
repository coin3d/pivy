/* generator for iterating MFields */
%pythoncode %{        
def MFieldGenerator(field):
   for i in range(field.getNum()):
      yield field[i]
%}

%extend SoMField {
/* shadow __iter__ to return a new iterator object */
%pythoncode %{
   def __iter__(self):
      iter = MFieldGenerator(self)
      return iter
%}
}
