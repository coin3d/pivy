%typemap(in) (const unsigned char * bytes, const SbVec2s & size, const int bytesperpixel) {
  unsigned char * image;
  PyObject * buf = $input;
  PyObject * vec2s = $input;
  PyObject * nc = $input;

  if ((SWIG_ConvertPtr(vec2s,(void **) &$2, SWIGTYPE_p_SbVec2s, SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
  if ($2 == NULL) {
    PyErr_SetString(PyExc_TypeError,"null reference"); SWIG_fail;
  }
  $3 = PyInt_AsLong(nc);
  if (PyString_Check(buf)) {
    int len = (*$2)[0] * (*$2)[1] * $3;
    PyString_AsStringAndSize(buf, (char **)&image, &len);
    $1 = image;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence."); SWIG_fail;
  }
}

%typemap(in) (const unsigned char * bytes, const SbVec3s & size, const int bytesperpixel) {
  unsigned char * image;
  PyObject * buf = $input;
  PyObject * vec3s = $input;
  PyObject * nc = $input;

  if ((SWIG_ConvertPtr(vec3s,(void **) &$2, SWIGTYPE_p_SbVec3s, SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
  if ($2 == NULL) {
    PyErr_SetString(PyExc_TypeError,"null reference"); SWIG_fail;
  }
  $3 = PyInt_AsLong(nc);
  if (PyString_Check(buf)) {
    int len = (*$2)[0] * (*$2)[1] * (*$2)[2] * $3;
    PyString_AsStringAndSize(buf, (char **)&image, &len);
    $1 = image;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence."); SWIG_fail;
  }
}

%typemap(in) (const SbVec2s & size, const int bytesperpixel, const unsigned char * bytes) {
  unsigned char * image;
  PyObject * vec2s = $input;
  PyObject * nc = $input;
  PyObject * buf = $input;

  if ((SWIG_ConvertPtr(vec2s,(void **) &$1, SWIGTYPE_p_SbVec2s, SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
  if ($1 == NULL) {
    PyErr_SetString(PyExc_TypeError,"null reference"); SWIG_fail;
  }
  $2 = PyInt_AsLong(nc);
  if (PyString_Check(buf)) {
    int len = (*$1)[0] * (*$1)[1] * $2;
    PyString_AsStringAndSize(buf, (char **)&image, &len);
    $3 = image;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence."); SWIG_fail;
  }
}

%typemap(in) (const SbVec3s & size, const int bytesperpixel, const unsigned char * bytes) {
  unsigned char * image;
  PyObject * vec3s = $input;
  PyObject * nc = $input;
  PyObject * buf = $input;

  if ((SWIG_ConvertPtr(vec3s,(void **) &$1, SWIGTYPE_p_SbVec3s, SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
  if ($1 == NULL) {
    PyErr_SetString(PyExc_TypeError,"null reference"); SWIG_fail;
  }
  $2 = PyInt_AsLong(nc);
  if (PyString_Check(buf)) {
    int len = (*$1)[0] * (*$1)[1] * $2;
    PyString_AsStringAndSize(buf, (char **)&image, &len);
    $3 = image;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence."); SWIG_fail;
  }
}

%rename(SbImage_vec2s) SbImage::SbImage(const unsigned char * bytes,
                                        const SbVec2s & size, const int bytesperpixel);
%rename(SbImage_vec3s) SbImage::SbImage(const unsigned char * bytes,
                                        const SbVec3s & size, const int bytesperpixel);
 
%feature("shadow") SbImage::SbImage %{
def __init__(self,*args):
  newobj = None
  if len(args) == 3:
     if isinstance(args[1], SbVec2s):
        newobj = apply(_pivy.new_SbImage_vec2s,args)
     elif isinstance(args[1], SbVec3s):
        newobj = apply(_pivy.new_SbImage_vec3s,args)
  else:
     newobj = apply(_pivy.new_SbImage,args)
  if newobj:
     self.this = newobj.this
     self.thisown = 1
%}


%rename(setValue_vec2s) SbImage::setValue(const SbVec2s & size, const int bytesperpixel,
                                          const unsigned char * bytes);

%feature("shadow") SbImage::setValue(const SbVec3s & size, const int bytesperpixel,
                                     const unsigned char * bytes) %{
def setValue(*args):
  if isinstance(args[1], SbVec2s):
      return apply(_pivy.SbImage_setValue_vec2s,args)
  return apply(_pivy.SbImage_setValue_vec2s,args)
%}

%extend SbImage {
  PyObject * getValue() {
    PyObject *result;
    SbVec3s size;
    int nc;

    const unsigned char * image = self->getValue(size, nc);
    
    result = PyTuple_New(3);
    
    /* check for 3D image */
    if (size[2] == 0) {
      SbVec2s * vec2s = new SbVec2s(size[0], size[1]);
      PyTuple_SetItem(result, 0, PyString_FromStringAndSize((const char*)image,
                                                            (*vec2s)[0] * (*vec2s)[1] * nc));
      PyTuple_SetItem(result, 1, SWIG_NewPointerObj((void *)vec2s, SWIGTYPE_p_SbVec2s, 1));
    } else {
      SbVec3s * vec3s = new SbVec3s(size[0], size[1], size[2]);
      PyTuple_SetItem(result, 0, PyString_FromStringAndSize((const char*)image,
                                                            (*vec3s)[0] * (*vec3s)[1] * (*vec3s)[2] * nc));
      PyTuple_SetItem(result, 1, SWIG_NewPointerObj((void *)vec3s, SWIGTYPE_p_SbVec3s, 1));
    }
      
    PyTuple_SetItem(result, 2, PyInt_FromLong(nc));
    Py_INCREF(result);

    return result;
  }
}
