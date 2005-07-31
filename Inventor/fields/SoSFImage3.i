%typemap(in,numinputs=0) (SbVec3s & size, int & nc) (int temp) {
   $1 = new SbVec3s();
   $2 = &temp;
}

%typemap(argout) (SbVec3s & size, int & nc) {
  Py_XDECREF($result);   /* Blow away any previous result */
  $result = PyTuple_New(3);
  PyTuple_SetItem($result, 0, PyString_FromStringAndSize((const char *)result, (*$1)[0] * (*$1)[1] * (*$1)[2] * (*$2)));
  PyTuple_SetItem($result, 1, SWIG_NewPointerObj((void *)$1, SWIGTYPE_p_SbVec3s, 1));
  PyTuple_SetItem($result, 2, PyInt_FromLong(*$2));
  Py_INCREF($result);
}

%extend SoSFImage3 {
  void setValue(const SbVec3s & size, const int nc,
                PyObject * pixels)
  {
    int len = size[0] * size[1] * size[2] * nc;
    unsigned char * image;

    PyString_AsStringAndSize(pixels, (char **)&image, &len);
    self->setValue(size, nc, image);
  }
  void setValue(const SoSFImage3 * other){ *self = *other; }
}
