%{
static void
SoSensorPythonCB(void * data, SoSensor * sensor)
{
  PyObject *func, *arglist;
  PyObject *result, *sensCB;

  sensCB = SWIG_NewPointerObj((void *) sensor, SWIGTYPE_p_SoSensor, 1);

  /* the first item in the data sequence is the python callback
   * function; the second is the supplied data python object */
  func = PyTuple_GetItem((PyObject *)data, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)data, 1), sensCB);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
    PyErr_Print();
  }

  Py_DECREF(arglist);
  Py_XDECREF(result);

  return /*void*/;
}
%}

%rename(SoSensor_scb_v) SoSensor::SoSensor(SoSensorCB * func, void * data);

%feature("shadow") SoSensor::SoSensor %{
def __init__(self,*args):
   newobj = None
   if len(args) == 2:
      args = (args[0], (args[0], args[1]))
      newobj = apply(_pivy.new_SoSensor_scb_v,args)
   else:
      newobj = apply(_pivy.new_SoSensor,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
%}

%typemap(in) SoSensorCB * func %{
  if (!PyCallable_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "need a callable object!");
    return NULL;
  }
  $1 = SoSensorPythonCB;
%}

%typemap(in) void * data %{
  if (!PyTuple_Check($input)) {
    PyErr_SetString(PyExc_TypeError, "tuple expected!");
    return NULL;
  }

  Py_INCREF($input);
  $1 = (void *)$input;
%}
