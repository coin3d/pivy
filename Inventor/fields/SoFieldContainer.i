%extend SoFieldContainer {
  PyObject * getFieldName(SoField * field) {
    SbName * name = new SbName;
    PyObject * result;

    SbBool tf = self->getFieldName(field, *name);

    result = PyTuple_New(2);
    PyTuple_SetItem(result, 0, PyInt_FromLong(tf));
    PyTuple_SetItem(result, 1,
                    SWIG_NewPointerObj((void *) name, SWIGTYPE_p_SbName, 1));
    Py_INCREF(result);

    return result;
  }
  
/* add generic interface to access fields as attributes */
%pythoncode %{
    def __getattr__(self,name):
        try:
            return SoBase.__getattribute__(self, name)
        except AttributeError, e:
            field = self.getField(SbName(name))
            if field is None:
                raise e
            return field
            
    def __setattr__(self,name,value):
        # I don't understand why we need this, but otherwise it does not work :/
        if name == 'this':
            return SoBase.__setattr__(self, name, value)
        field = self.getField(SbName(name))
        if field is None:
            return SoBase.__setattr__(self, name, value)
        field.setValue(value)
        return field
%}
}
