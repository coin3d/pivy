%{
static void
convert_SbMat_array(PyObject *input, SbMat temp)
{
  if (PySequence_Check(input) && (PySequence_Size(input) == 4) &&
      (PySequence_Size(PySequence_GetItem(input, 0)) == 4) &&
      (PySequence_Size(PySequence_GetItem(input, 1)) == 4) &&
      (PySequence_Size(PySequence_GetItem(input, 2)) == 4) &&
      (PySequence_Size(PySequence_GetItem(input, 3)) == 4)) {
    int i,j;
    for (i=0; i < 4; i++) {
      for (j=0; j < 4; j++) {
        PyObject *oij = PySequence_GetItem(PySequence_GetItem(input, i), j);
        if (!PyNumber_Check(oij)) {
          PyErr_SetString(PyExc_TypeError,
                          "sequence must contain 4 sequences where every sequence contains 4 floats");
          PyErr_Print();
          return;
        }
        temp[i][j] = PyFloat_AsDouble(oij);
      }
    }
  } else {
    PyErr_SetString(PyExc_TypeError,
                    "sequence must contain 4 sequences where every sequence contains 4 floats");
    PyErr_Print();
  }
}
%}

%typemap(in) SbMat * (SbMat temp) {
  convert_SbMat_array($input, temp);
  $1 = &temp;
}

%typemap(out) SbMat & {
  int i,j;
  $result = PyTuple_New(4);
  
  for (i=0; i<4; i++) {
    PyObject *oi = PyList_New(4);
    for (j=0; j<4; j++) {
      PyObject *oj = PyFloat_FromDouble((double)(*$1)[i][j]);
      PyList_SetItem(oi, j, oj);
    }
    PyTuple_SetItem($result, i, oi);	
  }
}

%rename(SbMatrix_f16) SbMatrix::SbMatrix(const float a11, const float a12, const float a13, const float a14,
                                         const float a21, const float a22, const float a23, const float a24,
                                         const float a31, const float a32, const float a33, const float a34,
                                         const float a41, const float a42, const float a43, const float a44);
%rename(SbMatrix_SbMat) SbMatrix::SbMatrix(const SbMat * matrix);

%feature("shadow") SbMatrix::SbMatrix %{
def __init__(self,*args):
   if len(args) == 1:
      self.this = apply(_pivy.new_SbMatrix_SbMat,args)
      self.thisown = 1
      return
   elif len(args) == 16:
      self.this = apply(_pivy.new_SbMatrix_f16,args)
      self.thisown = 1
      return
   self.this = apply(_pivy.new_SbMatrix,args)
   self.thisown = 1
%}

%rename(det3_i6) SbMatrix::det3(int r1, int r2, int r3,
								int c1, int c2, int c3) const;

%feature("shadow") SbMatrix::setScale(const float s) %{
def det3(*args):
   if len(args) == 7:
      return apply(_pivy.SbMatrix_det3_i6,args)
   return apply(_pivy.SbMatrix_det3,args)
%}

%rename(setScale_vec3) SbMatrix::setScale(const SbVec3f & s);

%feature("shadow") SbMatrix::setScale(const float s) %{
def setScale(args):
  if type(args[1]) == type(0.0):
	return apply(_pivy.SbMatrix_setScale,args)
  return apply(_pivy.SbMatrix_setScale_vec3,args)
%}

%rename(setTransform_vec3_rot_vec3_rot) SbMatrix::setTransform(const SbVec3f & t, const SbRotation & r, const SbVec3f & s,
															   const SbRotation & so);
%rename(setTransform_vec3_rot_vec3_rot_vec3) SbMatrix::setTransform(const SbVec3f & translation,
																	const SbRotation & rotation, const SbVec3f & scaleFactor,
																	const SbRotation & scaleOrientation, const SbVec3f & center);

%feature("shadow") SbMatrix::setTransform(const SbVec3f & t, const SbRotation & r, const SbVec3f & s) %{
def setTransform(*args):
   if len(args) == 5:
      return apply(_pivy.SbMatrix_setTransform_vec3_rot_vec3_rot,args)
   elif len(args) == 6:
      return apply(_pivy.SbMatrix_setTransform_vec3_rot_vec3_rot_vec3,args)
   return apply(_pivy.SbMatrix_setTransform,args)
%}

%ignore SbMatrix::getTransform(SbVec3f & translation, SbRotation & rotation,
												  SbVec3f & scaleFactor, SbRotation & scaleOrientation,
												  const SbVec3f & center) const;

%ignore SbMatrix::getTransform(SbVec3f & t, SbRotation & r, SbVec3f & s, SbRotation & so);

%rename(multVecMatrix_vec4) SbMatrix::multVecMatrix(const SbVec4f & src, SbVec4f & dst) const;

%feature("shadow") SbMatrix::multVecMatrix(const SbVec3f & src, SbVec3f & dst) %{
def multVecMatrix(*args):
   if isinstance(args[1], SbVec4f):
      return apply(_pivy.SbMatrix_multVecMatrix_vec4,args)
   return apply(_pivy.SbMatrix_multVecMatrix,args)
%}

/* the next 2 typemaps handle the return value for e.g. multMatrixVec() */
%typemap(argout) SbVec3f & dst, SbVec4f & dst {
  $result = SWIG_NewPointerObj((void *) $1, $1_descriptor, 1);
}
%typemap(in,numinputs=0) SbVec3f & dst, SbVec4f & dst {
    $1 = new $1_basetype();
}

%ignore SbMatrix::SbMatrix(const SbMat & matrix);
%ignore SbMatrix::setValue(const SbMat & m);

/**
 * workaround for swig generating an unnecessary cast
 * -> (SbMat const &)*arg);
 **/
%extend SbMatrix {
  void setValue(const SbMat * m) {
    self->setValue(*m);
  }

  // add a method for wrapping c++ operator[] access
  const float *__getitem__(int i) {
    return (self->getValue())[i];
  }

  PyObject * getTransform() {
    SbVec3f * t = new SbVec3f;
    SbVec3f * s = new SbVec3f;
    SbRotation * r = new SbRotation;
    SbRotation * so = new SbRotation;
    PyObject * result;

    self->getTransform(*t, *r, *s, *so);
        
    result = PyTuple_New(4);
    PyTuple_SetItem(result, 0,
                    SWIG_NewPointerObj((void *) t, SWIGTYPE_p_SbVec3f, 1));
    PyTuple_SetItem(result, 1,
                    SWIG_NewPointerObj((void *) r, SWIGTYPE_p_SbRotation, 1));
    PyTuple_SetItem(result, 2,
                    SWIG_NewPointerObj((void *) s, SWIGTYPE_p_SbVec3f, 1));
    PyTuple_SetItem(result, 3,
                    SWIG_NewPointerObj((void *) so, SWIGTYPE_p_SbRotation, 1));
    Py_INCREF(result);

    return result;
  }

  PyObject * getTransform(SbVec3f & center) {
    SbVec3f * t = new SbVec3f;
    SbVec3f * s = new SbVec3f;
    SbRotation * r = new SbRotation;
    SbRotation * so = new SbRotation;
    PyObject * result;

    self->getTransform(*t, *r, *s, *so, center);
        
    result = PyTuple_New(4);
    PyTuple_SetItem(result, 0,
                    SWIG_NewPointerObj((void *) t, SWIGTYPE_p_SbVec3f, 1));
    PyTuple_SetItem(result, 1,
                    SWIG_NewPointerObj((void *) r, SWIGTYPE_p_SbRotation, 1));
    PyTuple_SetItem(result, 2,
                    SWIG_NewPointerObj((void *) s, SWIGTYPE_p_SbVec3f, 1));
    PyTuple_SetItem(result, 3,
                    SWIG_NewPointerObj((void *) so, SWIGTYPE_p_SbRotation, 1));
    Py_INCREF(result);

    return result;
  }
}
