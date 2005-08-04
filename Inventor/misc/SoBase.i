%extend SoBase {
%pythoncode %{
    def __eq__(self,other):
      return other and (self.this == other.this) or False
    def __ne__(self,other):
      return other and (self.this != other.this) or True
%}
}
