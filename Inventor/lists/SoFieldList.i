// add a method for wrapping c++ operator[] access
%extend SoFieldList {
  PyObject * get(int index) {
    return autocast_field((SoField*)self->get(index));
  }
}
