%typemap(in) (const unsigned char * bytes, const SbVec2s & size, const int bytesperpixel) {
  unsigned char * result = NULL;
  PyObject * arr_obj;
  arr_obj = $input;
  if (PySequence_Check(arr_obj)) {
    int i, len = PySequence_Size(arr_obj);
    result = (unsigned char *)malloc(len);
    for (i=0; i < len; i++) {
      PyArg_ParseTuple(PySequence_GetItem(arr_obj, i), "B", result[len]);
    }
    $1 = result;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence.");
    SWIG_fail;
  }
  if ((SWIG_ConvertPtr($input,(void **) &$1, SWIGTYPE_p_SbVec2s, SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
  if ($2 == NULL) {
    PyErr_SetString(PyExc_TypeError,"null reference"); SWIG_fail;
  }
  $3 = PyInt_AsLong($input);
}

%typemap(in) (const unsigned char * bytes, const SbVec3s & size, const int bytesperpixel) {
  unsigned char * result = NULL;
  PyObject * arr_obj;
  arr_obj = $input;
  if (PySequence_Check(arr_obj)) {
    int i, len = PySequence_Size(arr_obj);
    result = (unsigned char *)malloc(len);
    for (i=0; i < len; i++) {
      PyArg_ParseTuple(PySequence_GetItem(arr_obj, i), "B", result[len]);
    }
    $1 = result;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence.");
    SWIG_fail;
  }
  if ((SWIG_ConvertPtr($input,(void **) &$1, SWIGTYPE_p_SbVec3s, SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
  if ($2 == NULL) {
    PyErr_SetString(PyExc_TypeError,"null reference"); SWIG_fail;
  }
  $3 = PyInt_AsLong($input);
}

%typemap(in) (const SbVec2s & size, const int bytesperpixel, const unsigned char * bytes) {
  unsigned char * result = NULL;
  PyObject * arr_obj;
  if ((SWIG_ConvertPtr($input,(void **) &$1, SWIGTYPE_p_SbVec2s, SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
  if ($1 == NULL) {
    PyErr_SetString(PyExc_TypeError,"null reference"); SWIG_fail;
  }
  $2 = PyInt_AsLong($input);
  arr_obj = $input;
  if (PySequence_Check(arr_obj)) {
    int i, len = PySequence_Size(arr_obj);
    result = (unsigned char *)malloc(len);
    for (i=0; i < len; i++) {
      PyArg_ParseTuple(PySequence_GetItem(arr_obj, i), "B", result[len]);
    }
    $3 = result;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence.");
    SWIG_fail;
  }
}

%typemap(in) (const SbVec3s & size, const int bytesperpixel, const unsigned char * bytes) {
  unsigned char * result = NULL;
  PyObject * arr_obj;
  if ((SWIG_ConvertPtr($input,(void **) &$1, SWIGTYPE_p_SbVec3s, SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
  if ($1 == NULL) {
    PyErr_SetString(PyExc_TypeError,"null reference"); SWIG_fail;
  }
  $2 = PyInt_AsLong($input);
  arr_obj = $input;
  if (PySequence_Check(arr_obj)) {
    int i, len = PySequence_Size(arr_obj);
    result = (unsigned char *)malloc(len);
    for (i=0; i < len; i++) {
      PyArg_ParseTuple(PySequence_GetItem(arr_obj, i), "B", result[len]);
    }
    $3 = result;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence.");
    SWIG_fail;
  }
}

%rename(SbImage_vec2s) SbImage::SbImage(const unsigned char * bytes,
                                        const SbVec2s & size, const int bytesperpixel);
%rename(SbImage_vec3s) SbImage::SbImage(const unsigned char * bytes,
                                        const SbVec3s & size, const int bytesperpixel);
 
%feature("shadow") SbImage::SbImage %{
def __init__(self,*args):
  if len(args) == 3:
      if isinstance(args[1], SbVec2s):
          self.this = apply(_pivy.new_SbImage_vec2s,args)
          self.thisown = 1
          return
      elif isinstance(args[1], SbVec3s):
          self.this = apply(_pivy.new_SbImage_vec3s,args)
          self.thisown = 1
          return
  self.this = apply(_pivy.new_SbImage,args)
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
