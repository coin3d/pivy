%rename(set_str_in) SoFieldContainer::set(const char * fielddata, SoInput * in);

%feature("shadow") SoFieldContainer::set(const char * const fielddata) %{
def set(*args):
   if len(args) == 3:
      return apply(_pivy.SoFieldContainer_set_str_in,args)
   return apply(_pivy.SoFieldContainer_set,args)
%}

%rename(get_str_out) SoFieldContainer::get(SbString & fielddata, SoOutput * out);

%feature("shadow") SoFieldContainer::get(SbString & fielddata) %{
def get(*args):
   if len(args) == 3:
      return apply(_pivy.SoFieldContainer_get_str_out,args)
   return apply(_pivy.SoFieldContainer_get,args)
%}

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
}
