%{
/* sip specific stuff that allows to bridge to PyQt */
/**
 * as this solution might appeal to the devil himself - here an attempt
 * of clarification:
 *
 * You: but tamer this is a really really ugly hack! shame on you!
 *  Me: guilty! *blush* ey, but what else can I do, huh?
 *      so would you plz. just join my prayers that the sip structures are 
 *      not going to change any time soon as otherwise we are going to burn
 *      in _HELL_ and won't see any angels any time soon!
 */

/*
 * A Python method's component parts.  This allows us to re-create the method
 * without changing the reference counts of the components.
 */

typedef struct {
	PyObject *mfunc;		/* The function. */
	PyObject *mself;		/* Self if it is a bound method. */
	PyObject *mclass;		/* The class. */
} sipPyMethod;

/*
 * Extra type specific information.
 */
typedef struct {
	const void *(*castfunc)(const void *,PyObject *);	/* Cast function. */
	void *proxyfunc;		/* Create proxy function. */
	struct _sipQtSignal *emitTable;	/* Emit table for Qt sigs (complex). */
} sipExtraType;

/*
 * A slot.
 */

typedef struct {
	char *name;			/* Name if a Qt or Python signal. */
	PyObject *pyobj;		/* Signal or Qt slot object. */
	sipPyMethod meth;		/* Python slot method, pyobj is NULL. */
	PyObject *weakSlot;		/* A weak reference to the slot. */
} sipSlot;

/*
 * A receiver of a Python signal.
 */

typedef struct _sipPySigRx {
	sipSlot rx;			/* The receiver. */
	struct _sipPySigRx *next;	/* Next in the list. */
} sipPySigRx;

/*
 * A Python signal.
 */

typedef struct _sipPySig {
	char *name;			/* The name of the signal. */
	sipPySigRx *rxlist;		/* The list of receivers. */
	struct _sipPySig *next;		/* Next in the list. */
} sipPySig;

/*
 * A C/C++ object wrapped as a Python object.
 */

typedef struct _sipThisType {
	PyObject_HEAD
	union {
		const void *cppPtr;	/* C/C++ object pointer. */
		const void *(*afPtr)();	/* Access function. */
	} u;
	int flags;			/* Object flags. */
	PyObject *sipSelf;		/* The Python class instance. */
	sipPySig *pySigList;		/* Python signal list (complex). */
	sipExtraType *xType;		/* Extra type information. */
} sipThisType;

/*
 * Maps the name of a Qt signal to a wrapper function to emit it.
 */

typedef struct _sipQtSignal {
	char *st_name;
	int (*st_emitfunc)(sipThisType *,PyObject *);
} sipQtSignal;


static SbBool
SoQtRenderAreaEventPythonCB(void * closure, QEvent * event)
{
  PyObject *func, *arglist;
  PyObject *result, *qev;
  sipThisType *sipThis;
  int ires = 0;

  /** 
   * the next stunt here deserves documentation as otherwise i would not
   * know what is going on here by tomorrow morning!
   *
   * What are we doing here? hacking in extremo! i had to find a way to pass
   * the QEvent instance we get to PyQt!
   *
   * the approach i chose is to create a QEvent instance in Python from PyQt
   * (obviously to let this work the user had to import PyQt beforehand. he
   * has to anyways as otherwise there is no good reason to create this
   * callback).
   * this gives us a fully and properly instantiated structure, as PyQt 
   * expects it, without digging into sip or depending on the sip library.
   * We do this in the switch statement and figure out which type we deal with
   * so that we can instantiate the correct type and cast the C++ object to
   * the right class at the same time as there is no way to achieve this with
   * PyQt from within Python.
   *
   * then i pass the instantiated structure over here and grab the sipThis
   * entry from the instance which holds a u.cppPtr which turns
   * out to be the real Qt Object in memory. *har, we are in business now*
   *
   * now i delete the current pointer and let u.cppPtr point to our very own
   * QEvent Object. amazingly enough this really works...
   *
   *                                ~~~o~~~
   *
   * In case anybody wonders! yes, i know that one can achieve all of this
   * in a very simple and elegant fashion by just using the sip library, 
   * like e.g. adding the following instead of the structure declarations
   * and our stunt:
   * #define ANY_TEMP ANY
   * #undef ANY
   * #include <sip.h>
   * #undef ANY
   * #define ANY ANY_TEMP
   *
   *   extern PyObject *sipClass_QEvent;
   *   qev = sipNewCppToSelfSubClass(event, sipClass_QEvent, SIP_SIMPLE | SIP_PY_OWNED);
   *
   * this works perfectly and is such a lovely solution that i really wanted
   * to keep it. BUT libsip gets installed into the python site-packages
   * directory and not only would we need to link against libsip but also
   * against the libqtcmodule for the sipClass_Qevent object. this SUCKS,
   * adds new library dependencies, which i simply don't want to cope with
   * and makes the platform independent goal harder to achieve.
   *
   * so in the hack we trust!
   */
  
  /* type casting business */
  switch (event->type()) {
     case QEvent::Timer:
        PyRun_SimpleString("qev = QTimerEvent(0)");
        event = (QTimerEvent *)event;
		break;

     case QEvent::MouseButtonPress:
     case QEvent::MouseButtonRelease:
     case QEvent::MouseButtonDblClick:
     case QEvent::MouseMove:
        PyRun_SimpleString("qev = QMouseEvent(QEvent.MouseMove, QPoint(), QPoint(), Qt.NoButton, Qt.NoButton)");
        event = (QMouseEvent *)event;
		break;

     case QEvent::KeyPress:
     case QEvent::KeyRelease:
        PyRun_SimpleString("qev = QKeyEvent(QEvent.KeyPress, 0, 0, 0)");
        event = (QKeyEvent *)event;
		break;

     case QEvent::FocusIn:
     case QEvent::FocusOut:
        PyRun_SimpleString("qev = QFocusEvent(QEvent.FocusIn)");
        event = (QFocusEvent *)event;
		break;

     case QEvent::Paint:
        PyRun_SimpleString("qev = QPaintEvent(QRegion())");
        event = (QPaintEvent *)event;
		break;

     case QEvent::Move:
        PyRun_SimpleString("qev = QMoveEvent(QPoint(), QPoint())");
        event = (QMoveEvent *)event;
		break;

     case QEvent::Resize:
        PyRun_SimpleString("qev = QResizeEvent(QSize(), QSize())");
        event = (QResizeEvent *)event;
		break;

     case QEvent::Close:
        PyRun_SimpleString("qev = QCloseEvent()");
        event = (QCloseEvent *)event;
		break;

     case QEvent::Show:
        PyRun_SimpleString("qev = QShowEvent()");
        event = (QShowEvent *)event;
		break;

     case QEvent::Hide:
        PyRun_SimpleString("qev = QHideEvent()");
        event = (QHideEvent *)event;
		break;

     case QEvent::DragMove:
        PyRun_SimpleString("qev = QDragMoveEvent(QPoint())");
        event = (QDragMoveEvent *)event;
		break;

     case QEvent::DragEnter:
        PyRun_SimpleString("qev = QDragEnterEvent(QPoint())");
        event = (QDragEnterEvent *)event;
		break;

     case QEvent::DragLeave:
        PyRun_SimpleString("qev = QDragLeaveEvent()");
        event = (QDragLeaveEvent *)event;
		break;

     case QEvent::Drop:
        PyRun_SimpleString("qev = QDropEvent(QPoint())");
        event = (QDropEvent *)event;
		break;

     case QEvent::ChildInserted:
     case QEvent::ChildRemoved:
        PyRun_SimpleString("qev = QChildEvent(QEvent.ChildInserted, QObject())");
        event = (QChildEvent *)event;
        break;

     default:
        PyRun_SimpleString("qev = QEvent(QEvent.None)");
  }

  PyObject *d = PyModule_GetDict(PyImport_AddModule("__main__"));
  qev = PyRun_String("qev", Py_eval_input, d, d);
  
  sipThis = (sipThisType *)PyDict_GetItem(((PyInstanceObject *)qev)->in_dict,
                                          PyString_FromString("sipThis"));
  delete (QEvent *)sipThis->u.cppPtr;
  sipThis->u.cppPtr = event;

  /* the first item in the closure sequence is the python callback
   * function; the second is the supplied closure python object */
  func = PyTuple_GetItem((PyObject *)closure, 0);
  arglist = Py_BuildValue("OO", PyTuple_GetItem((PyObject *)closure, 1), qev);

  if ((result = PyEval_CallObject(func, arglist)) == NULL) {
	printf("SoQtRenderAreaEventPythonCB(void * closure, QEvent * event) failed!\n");
  }
  else {
	ires = PyInt_AsLong(result);
  }

  Py_DECREF(arglist);
  Py_XDECREF(result);

  return ires;
}
%}

%typemap(in) PyObject *pyfunc %{
  if (!PyCallable_Check($input)) {
	PyErr_SetString(PyExc_TypeError, "need a callable object!");
	return NULL;
  }
  $1 = $input;
%}

/* add python specific callback functions */
%extend SoQtRenderArea {
  void setEventCallback(PyObject *pyfunc, PyObject *user = NULL) {
    if (user == NULL) {
      Py_INCREF(Py_None);
      user = Py_None;
    }
	  
    PyObject *t = PyTuple_New(2);
    PyTuple_SetItem(t, 0, pyfunc);
    PyTuple_SetItem(t, 1, user);
    Py_INCREF(pyfunc);
    Py_INCREF(user);

    self->setEventCallback(SoQtRenderAreaEventPythonCB, (void *) t);
  }
}
