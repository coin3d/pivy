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

%typemap(typecheck) SbMat * {
  $1 = PySequence_Check($input) ? 1 : 0;
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

%ignore SbMatrix::getTransform(SbVec3f & translation, SbRotation & rotation,
                               SbVec3f & scaleFactor, SbRotation & scaleOrientation,
                               const SbVec3f & center) const;

%ignore SbMatrix::getTransform(SbVec3f & t, SbRotation & r, SbVec3f & s, SbRotation & so);

/* the next 2 typemaps handle the return value for e.g. multMatrixVec() */
%typemap(argout) SbVec3f & dst, SbVec4f & dst {
  $result = SWIG_NewPointerObj((void *) $1, $1_descriptor, 1);
}
%typemap(in,numinputs=0) SbVec3f & dst, SbVec4f & dst {
  $1 = new $1_basetype();
}

%extend SbMatrix {
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

  /* add operator overloading methods instead of the global functions */
  SbMatrix __mul__(const SbMatrix & u) { return *self * u; }
  SbVec3f __mul__(const SbVec3f & u) { SbVec3f res; self->multMatrixVec(u, res); return res; }
  SbVec3f __rmul__(const SbVec3f & u) { SbVec3f res; self->multVecMatrix(u, res); return res; }
  int __eq__(const SbMatrix & u) { return *self == u; }
  int __ne__(const SbMatrix & u) { return *self != u; }
  const float *__getitem__(int i) { return (self->getValue())[i]; }
}
