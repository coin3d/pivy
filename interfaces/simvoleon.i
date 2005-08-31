/*
 * Copyright (c) 2002-2005 Tamer Fahmy <tamer@tammura.at>
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
%module(package="pivy") simvoleon

%{
#if defined(_WIN32) || defined(__WIN32__)
#include <windows.h>
#undef max
#undef ERROR
#undef DELETE
#undef ANY
#endif

#include <VolumeViz/C/basic.h>
#include <VolumeViz/details/SoVolumeRenderDetail.h>
#include <VolumeViz/details/SoOrthoSliceDetail.h>
#include <VolumeViz/details/SoObliqueSliceDetail.h>
#include <VolumeViz/details/SoVolumeDetail.h>
#include <VolumeViz/details/SoVolumeSkinDetail.h>
#include <VolumeViz/readers/SoVRVolFileReader.h>
#include <VolumeViz/readers/SoVolumeReader.h>
#include <VolumeViz/nodes/SoTransferFunction.h>
#include <VolumeViz/nodes/SoOrthoSlice.h>
#include <VolumeViz/nodes/SoVolumeRender.h>
#include <VolumeViz/nodes/SoVolumeRendering.h>
#include <VolumeViz/nodes/SoObliqueSlice.h>
#include <VolumeViz/nodes/SoVolumeIndexedFaceSet.h>
#include <VolumeViz/nodes/SoVolumeFaceSet.h>
#include <VolumeViz/nodes/SoVolumeData.h>
#include <VolumeViz/nodes/SoVolumeIndexedTriangleStripSet.h>
#include <VolumeViz/nodes/SoVolumeSkin.h>
#include <VolumeViz/nodes/SoVolumeTriangleStripSet.h>

#include "coin_header_includes.h"
%}

/* define needed for ref counting */
%define RefCount(...)
  %typemap(newfree) __VA_ARGS__ * { $1->ref(); }
  %extend __VA_ARGS__ { ~__VA_ARGS__() { self->unref(); } }
  %ignore __VA_ARGS__::~__VA_ARGS__();
%enddef

/* RefCount has to be declared for all classes it should apply to. In
   our case all classes derived from SoBase */
RefCount(SoObliqueSlice)
RefCount(SoOrthoSlice)
RefCount(SoVolumeFaceSet)
RefCount(SoVolumeIndexedFaceSet)
RefCount(SoVolumeIndexedTriangleStripSet)
RefCount(SoVolumeRender)
RefCount(SoVolumeRendering)
RefCount(SoTransferFunction)
RefCount(SoVolumeData)
RefCount(SoVolumeSkin)
RefCount(SoVolumeTriangleStripSet)

/* include the typemaps common to all pivy modules */
%include pivy_common_typemaps.i

/* import the pivy main interface file */
%import coin.i

%typemap(in) void * = char *;
%typemap(out) void * = char *;
%typemap(typecheck) void * = char *;

%include VolumeViz/details/SoVolumeRenderDetail.h
%include VolumeViz/details/SoOrthoSliceDetail.h
%include VolumeViz/details/SoObliqueSliceDetail.h
%include VolumeViz/details/SoVolumeDetail.h
%include VolumeViz/details/SoVolumeSkinDetail.h
%include VolumeViz/readers/SoVRVolFileReader.h
%include VolumeViz/readers/SoVolumeReader.h
%include VolumeViz/nodes/SoTransferFunction.h
%include VolumeViz/nodes/SoOrthoSlice.h
%include VolumeViz/nodes/SoVolumeRender.h
%include VolumeViz/nodes/SoVolumeRendering.h
%include VolumeViz/nodes/SoObliqueSlice.h
%include VolumeViz/nodes/SoVolumeIndexedFaceSet.h
%include VolumeViz/nodes/SoVolumeFaceSet.h
%include VolumeViz/nodes/SoVolumeData.h
%include VolumeViz/nodes/SoVolumeIndexedTriangleStripSet.h
%include VolumeViz/nodes/SoVolumeSkin.h
%include VolumeViz/nodes/SoVolumeTriangleStripSet.h
