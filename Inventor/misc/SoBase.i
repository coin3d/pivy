%extend SoBase {
  /* add a public destructor - otherwise refcount of new SoBase
   * derived instances, raised by the autoref feature, never gets
   * decreased */
  ~SoBase() { self->unref(); }

%pythoncode %{
    def __eq__(self,other):
      return other and (self.this == other.this) or False
    def __ne__(self,other):
      return other and (self.this != other.this) or True
    def __nonzero__(self):
      return True
%}
}
