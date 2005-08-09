%typemap(in,numinputs=0) (SbVec2s & size, int & nc) (int temp) {
   $1 = new SbVec2s();
   $2 = &temp;
}

%typemap(argout) (SbVec2s & size, int & nc) {
  Py_XDECREF($result); /* free up any previous result */
  $result = PyTuple_New(3);
  PyTuple_SetItem($result, 0, PyString_FromStringAndSize((const char *)result, (*$1)[0] * (*$1)[1] * (*$2)));
  PyTuple_SetItem($result, 1, SWIG_NewPointerObj((void *)$1, SWIGTYPE_p_SbVec2s, 1));
  PyTuple_SetItem($result, 2, PyInt_FromLong(*$2));
  Py_INCREF($result);
}

%extend SoSFImage {
  void setValue(const SbVec2s & size, const int nc, PyObject * pixels)
  {
    int len = size[0] * size[1] * nc;
    unsigned char * image;

    PyString_AsStringAndSize(pixels, (char **)&image, &len);
    self->setValue(size, nc, image);
  }

  void setValue(const SoSFImage * other) { *self = *other; }
}
