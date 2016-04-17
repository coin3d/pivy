%ignore SoField::get(SbString & valuestring);

%extend SoField {
  SbString get() {
    SbString valuestring;
    self->get(valuestring);
    return valuestring;
  }

%pythoncode %{
  @property
  def values(self):
    def _values(obj):
      for value in obj:
        if hasattr(value, "__iter__"):
          yield list(_values(value))
        else:
          yield value
    out = _values(self)
    return list(out)

  @values.setter
  def values(self, arr):
    self.deleteValues(0)
    self.setValues(0, len(arr), arr)

%}
}
