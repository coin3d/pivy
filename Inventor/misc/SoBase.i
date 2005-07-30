%extend SoBase {
%pythoncode %{
    def __eq__(self,other):
        return self.this == other.this;
    def __ne__(self,other):
        return self.this != other.this;
%}
}
