// add a method for wrapping c++ operator[] access
%extend SoNodeList {
  PyObject * get(int index) {
    return autocast((SoNode*)self->get(index));
  }

  PyObject * __getitem__(int i) {
    return SoNodeList_get(self, i);
  }

}
