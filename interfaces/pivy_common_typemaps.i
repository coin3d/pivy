/**
 * Copyright (C) 2002-2004, Tamer Fahmy <tamer@tammura.at>
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 *   * Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *   * Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in
 *     the documentation and/or other materials provided with the
 *     distribution.
 *   * Neither the name of the copyright holder nor the names of its
 *     contributors may be used to endorse or promote products derived
 *     from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 **/

/* header include needed to let nodekit extensions find the SbTime header */
%{
#include <Inventor/SbTime.h>

/* a casting helper function */
SWIGEXPORT(PyObject *)
cast(PyObject * self, PyObject * args)
{
  swig_type_info * swig_type = 0;
  void * cast_obj = 0;
  size_t type_len;
  char * type, * ptr_type;
  PyObject * obj;

  if (!PyArg_ParseTuple(args,"Os", &obj, &type)) return NULL;
  type_len = strlen(type);

  /*
   * add a pointer sign to the string coming from the interpreter
   * e.g. "SoSeparator" becomes "SoSeparator *" - so that SWIG_TypeQuery()
   * can do its job.
   */
  ptr_type = (char*)malloc(type_len+3);
  if (ptr_type == NULL) return NULL;

  memset(ptr_type, 0, type_len+3);
  strncpy(ptr_type, type, type_len);
  strcat(ptr_type, " *");

  if ((swig_type = SWIG_TypeQuery(ptr_type)) == 0) { free(ptr_type); return NULL; }

  free(ptr_type);

  if ((SWIG_ConvertPtr(obj, (void**)&cast_obj, NULL, 1)) == -1) return NULL;

  return SWIG_NewPointerObj((void*)cast_obj, swig_type, 0);
}

/* an autocasting helper function */
SWIGEXPORT(PyObject *)
autocast_base(SoBase * base)
{
  PyObject * result = NULL;

  /* autocast the result to the corresponding type */
  if (base) {
    const char * name = base->getTypeId().getName().getString();
    size_t name_len = strlen(name);
    char * cast_name = NULL;
    PyObject * result_tuple = NULL;

    /* in case it is a builtin type add an So prefix to the name */
    if (base->isOfType(SoFieldContainer::getClassTypeId()) && 
        ((SoFieldContainer*)base)->getIsBuiltIn()) {
      cast_name = (char*)malloc(name_len + 3);
      memset(cast_name, 0, name_len + 3);
      cast_name[0] = 'S'; cast_name[1] = 'o';
      strncpy(cast_name + 2, name, name_len);
    } else {
      cast_name = (char*)malloc(name_len+1);
      memset(cast_name, 0, name_len+1);
      strncpy(cast_name, name, name_len);
    }

    result_tuple = PyTuple_New(2);
    PyTuple_SetItem(result_tuple, 0, SWIG_NewPointerObj((void*)base, SWIGTYPE_p_SoBase, 1));
    PyTuple_SetItem(result_tuple, 1, PyString_FromString((const char*)cast_name));
    Py_INCREF(result_tuple);

    result = cast(NULL, result_tuple);

    Py_DECREF(result_tuple);
    free(cast_name);
  }

  if (!result) {
    Py_INCREF(Py_None);
    result = Py_None;
  }

  return result;
}

/* an autocasting helper function */
SWIGEXPORT(PyObject *)
autocast_path(SoPath * path)
{
  PyObject * result = NULL;
  
  /* autocast the result to the corresponding type */
  if (path) {
    const char * name = path->getTypeId().getName().getString();
    PyObject * result_tuple = NULL;

    result_tuple = PyTuple_New(2);
    PyTuple_SetItem(result_tuple, 0, SWIG_NewPointerObj((void*)path, SWIGTYPE_p_SoPath, 1));
    PyTuple_SetItem(result_tuple, 1, PyString_FromString((const char*)name));
    Py_INCREF(result_tuple);
    
    result = cast(NULL, result_tuple);

    Py_DECREF(result_tuple);

    if (!result) {
      /* try again by adding an So prefix to the name in case it is a builtin type */
      size_t name_len = strlen(name);
      char * cast_name = (char*)malloc(name_len + 3);

      memset(cast_name, 0, name_len + 3);
      cast_name[0] = 'S'; cast_name[1] = 'o';
      strncpy(cast_name + 2, name, name_len);

      result_tuple = PyTuple_New(2);
      PyTuple_SetItem(result_tuple, 0, SWIG_NewPointerObj((void*)path, SWIGTYPE_p_SoPath, 1));
      PyTuple_SetItem(result_tuple, 1, PyString_FromString((const char*)cast_name));
      Py_INCREF(result_tuple);

      result = cast(NULL, result_tuple);
      Py_DECREF(result_tuple);

      free(cast_name);
      
    }
  }

  if (!result) {
    Py_INCREF(Py_None);
    result = Py_None;
  }

  return result;
}

/* an autocasting helper function */
SWIGEXPORT(PyObject *)
autocast_field(SoField * field)
{
  PyObject * result = NULL;
  
  /* autocast the result to the corresponding type */
  if (field) {
    const char * name = field->getTypeId().getName().getString();
    PyObject * result_tuple = NULL;

    result_tuple = PyTuple_New(2);
    PyTuple_SetItem(result_tuple, 0, SWIG_NewPointerObj((void*)field, SWIGTYPE_p_SoField, 1));
    PyTuple_SetItem(result_tuple, 1, PyString_FromString((const char*)name));
    Py_INCREF(result_tuple);
    
    result = cast(NULL, result_tuple);

    Py_DECREF(result_tuple);

    if (!result) {
      /* try again by adding an So prefix to the name in case it is a builtin type */
      size_t name_len = strlen(name);
      char * cast_name = (char*)malloc(name_len + 3);

      memset(cast_name, 0, name_len + 3);
      cast_name[0] = 'S'; cast_name[1] = 'o';
      strncpy(cast_name + 2, name, name_len);

      result_tuple = PyTuple_New(2);
      PyTuple_SetItem(result_tuple, 0, SWIG_NewPointerObj((void*)field, SWIGTYPE_p_SoField, 1));
      PyTuple_SetItem(result_tuple, 1, PyString_FromString((const char*)cast_name));
      Py_INCREF(result_tuple);

      result = cast(NULL, result_tuple);
      Py_DECREF(result_tuple);

      free(cast_name);
      
    }
  }

  if (!result) {
    Py_INCREF(Py_None);
    result = Py_None;
  }

  return result;
}
%}

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
 *  constructors of any kind. the following %feature
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
%typemap(in) SbName & {
  if (PyString_Check($input)) {
    $1 = new SbName(PyString_AsString($input));
  } else {
    SWIG_ConvertPtr($input, (void**)&$1, SWIGTYPE_p_SbName, 1);
  }
}

%typemap(in) SbString & {
  if (PyString_Check($input)) {
    $1 = new SbString(PyString_AsString($input));
  } else {
    SWIG_ConvertPtr($input, (void**)&$1, SWIGTYPE_p_SbString, 1);
  }
}

%typemap(in) SbTime & {
  if (PyFloat_Check($input)) {
    $1 = new SbTime(PyFloat_AsDouble($input));
  } else {
    SWIG_ConvertPtr($input, (void**)&$1, SWIGTYPE_p_SbTime, 1);
  }
}

%typemap(in) FILE * {
  if (PyFile_Check($input)) {
    $1 = PyFile_AsFile($input);
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a file object.");
  }
}

/* typemaps for autocasting types through the Inventor type system */
%typemap(out) SoBase * {
  return autocast_base($1);
}

%typemap(out) SoNode * {
  return autocast_base($1);
}

%typemap(out) SoPath * {
  return autocast_path($1);
}

%typemap(out) SoEngine * {
  return autocast_base($1);
}

%typemap(out) SoField * {
  return autocast_field($1);
}

%native(cast) PyObject * cast(PyObject * self, PyObject * args);

#ifdef PIVY_WIN32
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
#endif
