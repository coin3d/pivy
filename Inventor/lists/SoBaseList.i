// add a method for wrapping c++ operator[] access
%extend SoBaseList {
  PyObject * get(int index) {
    return autocast_base((SoBase*)self->get(index));
  }

  PyObject * __getitem__(int i) {
    return SoBaseList_get(self, i);
  }
}
