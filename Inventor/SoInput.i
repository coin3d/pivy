%typemap(in) (void * bufpointer, size_t bufsize) {
#ifdef PY_2
  if (!PyString_Check($input))
#else
  if (!PyBytes_Check($input))
#endif
  {
    PyErr_SetString(PyExc_ValueError, "Expecting a string");
    return NULL;
  }
#ifdef PY_2
  $1 = (void *) PyString_AsString($input);
  $2 = PyString_Size($input);
#else
  $1 = (void *) PyBytes_AsString($input);
  $2 = PyBytes_Size($input);
#endif
}
