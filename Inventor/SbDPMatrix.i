%{
static void
convert_SbDPMat_array(PyObject *input, SbDPMat temp)
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

%typemap(in) SbDPMat * (SbDPMat temp) {
  convert_SbDPMat_array($input, temp);
  $1 = &temp;
}

%typemap(out) SbDPMat & {
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

%rename(SbDPMatrix_mul) operator *(const SbDPMatrix & m1, const SbDPMatrix & m2);
%rename(SbDPMatrix_eq) operator ==(const SbDPMatrix & m1, const SbDPMatrix & m2);
%rename(SbDPMatrix_neq) operator !=(const SbDPMatrix & m1, const SbDPMatrix & m2);

%ignore SbDPMatrix::SbDPMatrix(const SbDPMat & matrix);

/**
 * workaround for swig generating an unnecessary cast
 * -> (SbDPMat const &)*arg);
 **/
%extend SbDPMatrix {
  void setValue(const SbDPMat * m) {
    self->setValue(*m);
  }
}

%ignore SbDPMatrix::setValue(const SbDPMat & m);
