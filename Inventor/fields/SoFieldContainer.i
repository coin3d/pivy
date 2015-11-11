%extend SoFieldContainer {
  PyObject * getFieldName(SoField * field) {
    SbName name;
    if (!self->getFieldName(field, name)) {
      Py_INCREF(Py_None);
      return Py_None;
    }
    return Py_BuildValue("s", name.getString());
  }
  
/* add generic interface to access fields as attributes */
%pythoncode %{
  def __getattr__(self, name):
    try:
        return SoBase.__getattribute__(self, name)
    except AttributeError, e:
        field = self.getField(name)
        if field is None:
            raise e
        return field
          
  def __setattr__(self, name, value):
    # I don't understand why we need this, but otherwise it does not work :/
    if name == 'this':
        return SoBase.__setattr__(self, name, value)
    field = self.getField(name)
    if field is None:
        return SoBase.__setattr__(self, name, value)
    field.setValue(value)
    return field
%}
}
