%typemap(in) (SbVec2s & size, int & nc) {
  $1 = new SbVec2s();
  $2 = (int *)malloc(sizeof(int));
}

%extend SoSFImage {
  void setValue(const SbVec2s & size, const int nc,
                PyObject * pixels)
  {
    int len = size[0] * size[1] * nc;
    unsigned char * image;

    PyString_AsStringAndSize(pixels, (char **)&image, &len);
    self->setValue(size, nc, image);
  }

  PyObject * getValue() {
    PyObject *result;
    int nc;
    SbVec2s * size = new SbVec2s;
    const unsigned char * image = self->getValue(*size, nc);

    PyString_FromStringAndSize((const char*)image, (*size)[0] * (*size)[1] * nc);
    
    result = PyTuple_New(3);
    PyTuple_SetItem(result, 0, PyString_FromStringAndSize((const char*)image, (*size)[0] * (*size)[1] * nc));
    PyTuple_SetItem(result, 1, SWIG_NewPointerObj((void *)size, SWIGTYPE_p_SbVec2s, 1));
    PyTuple_SetItem(result, 2, PyInt_FromLong(nc));
    Py_INCREF(result);

    return result;
  }
}

/* fake an input argument */
%feature("shadow") SoSFImage::getValue(SbVec2s & size, int & nc) const %{
def getValue(self):
   return apply(_pivy.SoSFImage_getValue,(self,0))
%}

%feature("shadow") SoSFImage::startEditing(SbVec2s & size, int & nc) %{
def startEditing(self):
   return apply(_pivy.SoSFImage_startEditing,(self,0))
%}
