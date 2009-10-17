/*
 * Copyright (c) 2002-2007 Systems in Motion
 *
 * Permission to use, copy, modify, and distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */

/* header include needed to let nodekit extensions find the SbTime header */
%{
#include <Inventor/SbTime.h>

#if (PY_VERSION_HEX < 0x02050000)
/* Py_ssize_t needed for Python 2.5 compatibility, but isn't defined
 * in earlier Python versions. */
typedef int Py_ssize_t;
#endif

/* a casting helper function */
SWIGEXPORT PyObject *
cast(PyObject * self, PyObject * args)
{
  swig_type_info * swig_type = 0;
  void * cast_obj = 0;
  char * type_name, * ptr_type;
  int type_len;
  PyObject * obj = 0;

  if (!PyArg_ParseTuple(args, "Os#:cast", &obj, &type_name, &type_len)) {
    SWIG_fail;
  }

  /*
   * add a pointer sign to the string coming from the interpreter
   * e.g. "SoSeparator" becomes "SoSeparator *" - so that SWIG_TypeQuery()
   * can do its job.
   */
  if (!(ptr_type = (char*)malloc(type_len+3))) { SWIG_fail; }

  memset(ptr_type, 0, type_len+3);
  strncpy(ptr_type, type_name, type_len);
  strcat(ptr_type, " *");

  if (!(swig_type = SWIG_TypeQuery(ptr_type))) {
    /* the britney maneuver: "baby one more time" by prefixing 'So' */
    char * cast_name = (char*)malloc(type_len + 5);
    memset(cast_name, 0, type_len + 5);
    cast_name[0] = 'S'; cast_name[1] = 'o';
    strncpy(cast_name+2, ptr_type, type_len+2);

    if (!(swig_type = SWIG_TypeQuery(cast_name))) {
      free(cast_name); free(ptr_type);
      SWIG_fail;
    }

    free(cast_name);
  }

  free(ptr_type);

  SWIG_ConvertPtr(obj, (void**)&cast_obj, NULL, SWIG_POINTER_EXCEPTION | 0);
  if (SWIG_arg_fail(1)) { SWIG_fail; }

  return SWIG_NewPointerObj((void*)cast_obj, swig_type, 0);
  fail:
  return NULL;
}

/* autocasting helper function for SoBase */
SWIGEXPORT PyObject *
autocast_base(SoBase * base)
{
  PyObject * result = NULL;

  /* autocast the result to the corresponding type */
  if (base && base->isOfType(SoFieldContainer::getClassTypeId())) {
    PyObject * cast_args = NULL;
    PyObject * obj = NULL;
    SoType type = base->getTypeId();

    /* in case of a non built-in type get the closest built-in parent */
    while (!(type.isBad() || result)) {
      obj = SWIG_NewPointerObj((void*)base, SWIGTYPE_p_SoBase, 0);
      cast_args = Py_BuildValue("(Os)", obj, type.getName().getString());
      
      result = cast(NULL, cast_args);

      Py_DECREF(cast_args);
      Py_DECREF(obj);

      if (!result) { type = type.getParent(); }
    }
  }      

  if (!result) {
    Py_INCREF(Py_None);
    result = Py_None;
  }

  return result;
}

/* autocasting helper function for SoPath */
SWIGEXPORT PyObject *
autocast_path(SoPath * path)
{
  PyObject * result = NULL;
  
  /* autocast the result to the corresponding type */
  if (path) {
    PyObject * cast_args = NULL;
    PyObject * obj = NULL;
    SoType type = path->getTypeId();

    /* in case of a non built-in type get the closest built-in parent */
    while (!(type.isBad() || result)) {
      obj = SWIG_NewPointerObj((void*)path, SWIGTYPE_p_SoPath, 0);
      cast_args = Py_BuildValue("(Os)", obj, type.getName().getString());
      
      result = cast(NULL, cast_args);

      Py_DECREF(cast_args);
      Py_DECREF(obj);

      if (!result) { type = type.getParent(); }
    }
  }

  if (!result) {
    Py_INCREF(Py_None);
    result = Py_None;
  }

  return result;
}

/* autocasting helper function for SoField */
SWIGEXPORT PyObject *
autocast_field(SoField * field)
{
  PyObject * result = NULL;

  /* autocast the result to the corresponding type */
  if (field) {
    PyObject * cast_args = NULL;
    PyObject * obj = NULL;
    SoType type = field->getTypeId();

    /* in case of a non built-in type get the closest built-in parent */
    while (!(type.isBad() || result)) {
      obj = SWIG_NewPointerObj((void*)field, SWIGTYPE_p_SoField, 0);
      cast_args = Py_BuildValue("(Os)", obj, type.getName().getString());
      
      result = cast(NULL, cast_args);

      Py_DECREF(cast_args);
      Py_DECREF(obj);
      
      if (!result) { type = type.getParent(); }
    }
  }

  if (!result) {
    Py_INCREF(Py_None);
    result = Py_None;
  }

  return result;
}

/* autocasting helper function for SoEvent */
SWIGEXPORT PyObject *
autocast_event(SoEvent * event)
{
  PyObject * result = NULL;
  
  /* autocast the result to the corresponding type */
  if (event) {
    PyObject * cast_args = NULL;
    PyObject * obj = NULL;
    SoType type = event->getTypeId();

    /* in case of a non built-in type get the closest built-in parent */
    while (!(type.isBad() || result)) {
      obj = SWIG_NewPointerObj((void*)event, SWIGTYPE_p_SoEvent, 0);
      cast_args = Py_BuildValue("(Os)", obj, type.getName().getString());
      
      result = cast(NULL, cast_args);

      Py_DECREF(cast_args);
      Py_DECREF(obj);

      if (!result) { type = type.getParent(); }
    }
  }

  if (!result) {
    Py_INCREF(Py_None);
    result = Py_None;
  }

  return result;
}
%}

/* typemaps for autocasting types through the Inventor type system */
%typemap(out) SoBase * {
  $result = autocast_base($1);
}

%typemap(out) SoFieldContainer * {
  $result = autocast_base($1);
}

%typemap(out) SoNode * {
  $result = autocast_base($1);
}

%typemap(out) SoPath * {
  $result = autocast_path($1);
}

%typemap(out) SoEngine * {
  $result = autocast_base($1);
}

%typemap(out) SoField * {
  $result = autocast_field($1);
}

%typemap(out) SoEvent * {
  $result = autocast_event($1);
}

%native(cast) PyObject * cast(PyObject * self, PyObject * args);

/**
 * SWIG - interface includes and general typemap definitions
 **/

%include "typemaps.i"
%include "cpointer.i"

%pointer_class(char, charp);
%pointer_class(int, intp);
%pointer_class(long, longp);
%pointer_class(float, floatp);
%pointer_class(double, doublep);

/* if SWIG determines the class abstract it doesn't generate
 * constructors of any kind. the following %feature
 * declarations take care about this for the classes we still
 * want a constructor for.
 */
%feature("notabstract") SoBoolOperation;
%feature("notabstract") SoComposeRotation;
%feature("notabstract") SoComposeVec3f;
%feature("notabstract") SoDecomposeVec3f;

%rename(output) print(FILE * fp) const;
%rename(output) print(FILE * const fp) const;
%rename(output) print(FILE * const file = stdout) const;
%rename(srcFrom) from;
%rename(destTo) to;

/* generic typemaps to allow using python types instead of instances
 * within the python interpreter
 */
%typemap(in) int32_t = int;
%typemap(out) int32_t = int;
%typemap(typecheck) int32_t = int;

%typemap(in) uint32_t = unsigned int;
%typemap(out) uint32_t = unsigned int;
%typemap(typecheck) uint32_t = unsigned int;

%typemap(typecheck) SbName & {
  void *ptr = NULL;
  $1 = 1;
  if (!PyString_Check($input) && (SWIG_ConvertPtr($input, (void**)(&ptr), SWIGTYPE_p_SbName, 0) == -1)) {
    $1 = 0;
  }
}

%typemap(in) SbName & {
  if (PyString_Check($input)) {
    $1 = new SbName(PyString_AsString($input));
  } else {
    SbName * tmp = NULL;
    $1 = new SbName;
    SWIG_ConvertPtr($input, (void**)&tmp, SWIGTYPE_p_SbName, 1);
    *$1 = *tmp;
  }
}

%typemap(freearg) SbName & {
  if ($1) { delete $1; }
}

%typemap(typecheck) SbName {
  void *ptr = NULL;
  $1 = 1;
  if (!PyString_Check($input) && (SWIG_ConvertPtr($input, (void**)(&ptr), SWIGTYPE_p_SbName, 0) == -1)) {
    $1 = 0;
  }
}

%typemap(in) SbName {
  if (PyString_Check($input)) {
    $1 = SbName(PyString_AsString($input));
  } else {
    SbName * namePtr;
    SWIG_ConvertPtr($input, (void**)&namePtr, SWIGTYPE_p_SbName, 1);
    $1 = *namePtr;
  }
}

%typemap(typecheck) SbString & {
  void *ptr = NULL;
  $1 = 1;
  if (!PyString_Check($input) && (SWIG_ConvertPtr($input, (void**)(&ptr), SWIGTYPE_p_SbString, 0) == -1)) {
    $1 = 0;
  }
}

%typemap(in) SbString & {
  if (PyString_Check($input)) {
    $1 = new SbString(PyString_AsString($input));
  } else {
    SbString * tmp = NULL;
    $1 = new SbString;
    SWIG_ConvertPtr($input, (void**)&tmp, SWIGTYPE_p_SbString, 1);
    *$1 = *tmp;
  }
}

%typemap(freearg) SbString & {
  if ($1) { delete $1; }
}

%typemap(typecheck) SbTime & {
  void *ptr = NULL;
  $1 = 1;
  if (!PyFloat_Check($input) && (SWIG_ConvertPtr($input, (void**)(&ptr), SWIGTYPE_p_SbTime, 0) == -1)) {
    $1 = 0;
  }
}

%typemap(in) SbTime & {
  if (PyFloat_Check($input)) {
    $1 = new SbTime(PyFloat_AsDouble($input));
  } else {
    SbTime * tmp = NULL;
    $1 = new SbTime;
    SWIG_ConvertPtr($input, (void**)&tmp, SWIGTYPE_p_SbTime, 1);
    *$1 = *tmp;
  }
}

%typemap(freearg) SbTime & {
  if ($1) { delete $1; }
}

%typemap(in) FILE * {
  if (PyFile_Check($input)) {
    $1 = PyFile_AsFile($input);
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a file object.");
  }
}

%include Inventor/events/SoEvent.h
%include Inventor/fields/SoField.h
%include Inventor/SbString.h

/* some ignores for missing COIN_DLL_API specifications */
%ignore cc_rbptree_init;
%ignore cc_rbptree_clean;
%ignore cc_rbptree_insert;
%ignore cc_rbptree_remove;
%ignore cc_rbptree_size;
%ignore cc_rbptree_traverse;
%ignore cc_rbptree_debug;
%ignore so_plane_data::so_plane_data;
%ignore SoGLRenderCache::SoGLRenderCache;
%ignore SoGLRenderCache::open;
%ignore SoGLRenderCache::close;
%ignore SoGLRenderCache::call;
%ignore SoGLRenderCache::getCacheContext;
%ignore SoGLRenderCache::getPreLazyState;
%ignore SoGLRenderCache::getPostLazyState;
%ignore SoGLCacheList::SoGLCacheList;
%ignore SoGLCacheList::~SoGLCacheList;
%ignore SoGLCacheList::call;
%ignore SoGLCacheList::open;
%ignore SoGLCacheList::close;
%ignore SoGLCacheList::invalidateAll;
%ignore SoNormalBundle::SoNormalBundle;
%ignore SoNormalBundle::~SoNormalBundle;
%ignore SoNormalBundle::shouldGenerate;
%ignore SoNormalBundle::initGenerator;
%ignore SoNormalBundle::beginPolygon;
%ignore SoNormalBundle::polygonVertex;
%ignore SoNormalBundle::endPolygon;
%ignore SoNormalBundle::triangle;
%ignore SoNormalBundle::generate;
%ignore SoNormalBundle::getGeneratedNormals;
%ignore SoNormalBundle::getNumGeneratedNormals;
%ignore SoNormalBundle::set;
%ignore SoNormalBundle::get;
%ignore SoNormalBundle::send;

%ignore SoMultiTextureCoordinateElement::setFunction;
%ignore SoGLMultiTextureCoordinateElement::setTexGen;
