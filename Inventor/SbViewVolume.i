%typemap(in) (const SbVec2f& pt, SbVec3f& line0, SbVec3f& line1) {
  if ((SWIG_ConvertPtr(obj1,(void **) &arg2, SWIGTYPE_p_SbVec2f,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
  if (arg2 == NULL) {
    PyErr_SetString(PyExc_TypeError,"null reference"); SWIG_fail; 
  }
  $2 = new SbVec3f();
  $3 = new SbVec3f();
}

%typemap(argout) (SbVec3f& line0, SbVec3f& line1) {
  $result = Py_BuildValue("(OO)", 
                          SWIG_NewPointerObj((void *) $1, $1_descriptor, 1),
                          SWIG_NewPointerObj((void *) $2, $2_descriptor, 1));
}

%typemap(in) (const SbVec3f& src, SbVec3f& dst) {
  if ((SWIG_ConvertPtr(obj1,(void **) &arg2, SWIGTYPE_p_SbVec3f,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
  if (arg2 == NULL) {
    PyErr_SetString(PyExc_TypeError,"null reference"); SWIG_fail; 
  }
  $2 = new SbVec3f();
}

%typemap(argout) (const SbVec3f& src, SbVec3f& dst) {
  $result = SWIG_NewPointerObj((void *) $1, $1_descriptor, 1);
}

%ignore SbViewVolume::projectPointToLine(const SbVec2f& pt, SbLine& line) const;
