/**
 * Copyright (C) 2002-2005, Tamer Fahmy <tamer@tammura.at>
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
