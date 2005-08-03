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
%module(package="pivy") coin

%{
#if defined(_WIN32) || defined(__WIN32__)
#include <windows.h>
#undef max
#undef ERROR
#undef DELETE
#endif

#undef ANY

#include "coin_header_includes.h"

/* make GLState in SoGLLazyElement known to SWIG */
typedef SoGLLazyElement::GLState GLState;
%}

/* probably a correct way to get ref counting into the wrapper taken
   from the swig mailing list. */
%define RefCount(...)
  %typemap(newfree) __VA_ARGS__ * { $1->ref(); }
  %extend __VA_ARGS__ { ~__VA_ARGS__() { self->unref(); } }
  %ignore __VA_ARGS__::~__VA_ARGS__();
%enddef

/* has to be declared for all classes it should apply to :/. In our
   case all classes derived from and including SoBase ... */
RefCount(SoNode)
RefCount(SoBase)
RefCount(SoProtoInstance)
RefCount(SoProto)
RefCount(SoLabel)
RefCount(SoNonIndexedShape)
RefCount(SoScale)
RefCount(SoCylinder)
RefCount(SoDirectionalLight)
RefCount(SoTranslation)
RefCount(SoIndexedTriangleStripSet)
RefCount(SoRotor)
RefCount(SoTriangleStripSet)
RefCount(SoLight)
RefCount(SoLightModel)
RefCount(SoShape)
RefCount(SoRotationXYZ)
RefCount(SoPointLight)
RefCount(SoTextureCoordinateBinding)
RefCount(SoBumpMapTransform)
RefCount(SoPackedColor)
RefCount(SoDrawStyle)
RefCount(SoFaceSet)
RefCount(SoNurbsSurface)
RefCount(SoMaterial)
RefCount(SoLinearProfile)
RefCount(SoIndexedNurbsSurface)
RefCount(SoSurroundScale)
RefCount(SoNurbsProfile)
RefCount(SoText2)
RefCount(SoText3)
RefCount(SoCone)
RefCount(SoVertexProperty)
RefCount(SoCube)
RefCount(SoAnnotation)
RefCount(SoFile)
RefCount(SoSceneTexture2)
RefCount(SoTransformation)
RefCount(SoFont)
RefCount(SoInfo)
RefCount(SoTextureScalePolicy)
RefCount(SoTransformSeparator)
RefCount(SoFontStyle)
RefCount(SoOrthographicCamera)
RefCount(SoComplexity)
RefCount(SoSeparator)
RefCount(SoWWWInline)
RefCount(SoPickStyle)
RefCount(SoBaseColor)
RefCount(SoMaterialBinding)
RefCount(SoBumpMapCoordinate)
RefCount(SoTextureCoordinateEnvironment)
RefCount(SoBlinker)
RefCount(SoSelection)
RefCount(SoPendulum)
RefCount(SoTextureCoordinateFunction)
RefCount(SoNormal)
RefCount(SoUnits)
RefCount(SoNormalBinding)
RefCount(SoNurbsCurve)
RefCount(SoWWWAnchor)
RefCount(SoBumpMap)
RefCount(SoGroup)
RefCount(SoPolygonOffset)
RefCount(SoMarkerSet)
RefCount(SoTextureUnit)
RefCount(SoSpotLight)
RefCount(SoSphere)
RefCount(SoPointSet)
RefCount(SoPathSwitch)
RefCount(SoMatrixTransform)
RefCount(SoCallback)
RefCount(SoVertexShape)
RefCount(SoQuadMesh)
RefCount(SoAsciiText)
RefCount(SoProfileCoordinate2)
RefCount(SoProfileCoordinate3)
RefCount(SoSwitch)
RefCount(SoExtSelection)
RefCount(SoClipPlane)
RefCount(SoArray)
RefCount(SoEnvironment)
RefCount(SoLOD)
RefCount(SoShuttle)
RefCount(SoIndexedLineSet)
RefCount(SoTextureCoordinateDefault)
RefCount(SoTexture2Transform)
RefCount(SoImage)
RefCount(SoMultipleCopy)
RefCount(SoCoordinate3)
RefCount(SoCoordinate4)
RefCount(SoCamera)
RefCount(SoTransform)
RefCount(SoLocateHighlight)
RefCount(SoTexture3Transform)
RefCount(SoEventCallback)
RefCount(SoIndexedShape)
RefCount(SoLevelOfDetail)
RefCount(SoTextureCoordinatePlane)
RefCount(SoAntiSquish)
RefCount(SoTexture2)
RefCount(SoTexture3)
RefCount(SoListener)
RefCount(SoRotation)
RefCount(SoIndexedFaceSet)
RefCount(SoShapeHints)
RefCount(SoTextureCoordinate2)
RefCount(SoTextureCoordinate3)
RefCount(SoLineSet)
RefCount(SoIndexedNurbsCurve)
RefCount(SoResetTransform)
RefCount(SoColorIndex)
RefCount(SoTransparencyType)
RefCount(SoPerspectiveCamera)
RefCount(SoProfile)
RefCount(SoVRMLCone)
RefCount(SoVRMLVertexPoint)
RefCount(SoVRMLCoordinate)
RefCount(SoVRMLTouchSensor)
RefCount(SoVRMLAnchor)
RefCount(SoVRMLCylinderSensor)
RefCount(SoVRMLSpotLight)
RefCount(SoVRMLPlaneSensor)
RefCount(SoVRMLIndexedShape)
RefCount(SoVRMLNormal)
RefCount(SoVRMLSphereSensor)
RefCount(SoVRMLElevationGrid)
RefCount(SoVRMLProximitySensor)
RefCount(SoVRMLTimeSensor)
RefCount(SoVRMLColor)
RefCount(SoVRMLText)
RefCount(SoVRMLSphere)
RefCount(SoVRMLNavigationInfo)
RefCount(SoVRMLSwitch)
RefCount(SoVRMLTexture)
RefCount(SoVRMLPointSet)
RefCount(SoVRMLVertexShape)
RefCount(SoVRMLInterpolator)
RefCount(SoVRMLTransform)
RefCount(SoVRMLMovieTexture)
RefCount(SoVRMLScalarInterpolator)
RefCount(SoVRMLColorInterpolator)
RefCount(SoVRMLParent)
RefCount(SoVRMLLight)
RefCount(SoVRMLShape)
RefCount(SoVRMLPointLight)
RefCount(SoVRMLScript)
RefCount(SoVRMLSound)
RefCount(SoVRMLVertexLine)
RefCount(SoVRMLDragSensor)
RefCount(SoVRMLVisibilitySensor)
RefCount(SoVRMLBillboard)
RefCount(SoVRMLAppearance)
RefCount(SoVRMLImageTexture)
RefCount(SoVRMLTextureTransform)
RefCount(SoVRMLGeometry)
RefCount(SoVRMLBackground)
RefCount(SoVRMLPositionInterpolator)
RefCount(SoVRMLBox)
RefCount(SoVRMLFog)
RefCount(SoVRMLLOD)
RefCount(SoVRMLSensor)
RefCount(SoVRMLWorldInfo)
RefCount(SoVRMLIndexedLineSet)
RefCount(SoVRMLNormalInterpolator)
RefCount(SoVRMLExtrusion)
RefCount(SoVRMLOrientationInterpolator)
RefCount(SoVRMLDirectionalLight)
RefCount(SoVRMLIndexedLine)
RefCount(SoVRMLCylinder)
RefCount(SoVRMLTextureCoordinate)
RefCount(SoVRMLGroup)
RefCount(SoVRMLAudioClip)
RefCount(SoVRMLCollision)
RefCount(SoVRMLCoordinateInterpolator)
RefCount(SoVRMLPixelTexture)
RefCount(SoVRMLInline)
RefCount(SoVRMLMaterial)
RefCount(SoVRMLViewpoint)
RefCount(SoVRMLFontStyle)
RefCount(SoVRMLIndexedFaceSet)
RefCount(SoInterpolate)
RefCount(SoComposeMatrix)
RefCount(SoConcatenate)
RefCount(SoOneShot)
RefCount(SoComposeRotation)
RefCount(SoInterpolateFloat)
RefCount(SoInterpolateRotation)
RefCount(SoTimeCounter)
RefCount(SoGate)
RefCount(SoComposeVec2f)
RefCount(SoComposeVec3f)
RefCount(SoComposeVec4f)
RefCount(SoComposeRotationFromTo)
RefCount(SoDecomposeMatrix)
RefCount(SoInterpolateVec2f)
RefCount(SoInterpolateVec3f)
RefCount(SoInterpolateVec4f)
RefCount(SoSelectOne)
RefCount(SoDecomposeRotation)
RefCount(SoTransformVec3f)
RefCount(SoTriggerAny)
RefCount(SoCalculator)
RefCount(SoOnOff)
RefCount(SoCounter)
RefCount(SoFieldConverter)
RefCount(SoNodeEngine)
RefCount(SoElapsedTime)
RefCount(SoBoolOperation)
RefCount(SoComputeBoundingBox)
RefCount(SoEngine)
RefCount(SoDecomposeVec2f)
RefCount(SoDecomposeVec3f)
RefCount(SoDecomposeVec4f)
RefCount(SoHandleBoxDragger)
RefCount(SoDragger)
RefCount(SoScaleUniformDragger)
RefCount(SoDirectionalLightDragger)
RefCount(SoSpotLightDragger)
RefCount(SoTrackballDragger)
RefCount(SoPointLightDragger)
RefCount(SoTabBoxDragger)
RefCount(SoRotateSphericalDragger)
RefCount(SoTranslate1Dragger)
RefCount(SoTransformerDragger)
RefCount(SoJackDragger)
RefCount(SoTransformBoxDragger)
RefCount(SoTranslate2Dragger)
RefCount(SoScale2UniformDragger)
RefCount(SoScale1Dragger)
RefCount(SoCenterballDragger)
RefCount(SoDragPointDragger)
RefCount(SoRotateCylindricalDragger)
RefCount(SoRotateDiscDragger)
RefCount(SoTabPlaneDragger)
RefCount(SoScale2Dragger)
RefCount(SoJackManip)
RefCount(SoTabBoxManip)
RefCount(SoTransformManip)
RefCount(SoClipPlaneManip)
RefCount(SoTrackballManip)
RefCount(SoTransformBoxManip)
RefCount(SoPointLightManip)
RefCount(SoSpotLightManip)
RefCount(SoDirectionalLightManip)
RefCount(SoTransformerManip)
RefCount(SoHandleBoxManip)
RefCount(SoCenterballManip)
RefCount(SoLightKit)
RefCount(SoBaseKit)
RefCount(SoCameraKit)
RefCount(SoAppearanceKit)
RefCount(SoNodeKitListPart)
RefCount(SoWrapperKit)
RefCount(SoShapeKit)
RefCount(SoSeparatorKit)
RefCount(SoInteractionKit)
RefCount(SoSceneKit)

/* include the typemaps common to all pivy modules */
%include pivy_common_typemaps.i

%include coin_header_includes.h

/* removes all the properties for fields in classes derived from
   SoFieldContainer. this makes way for the dynamic access to fields
   as attributes.

   Note: this has to be the last code in the pivy file, therefore it
   is after all other SWIG declarations!
*/
%pythoncode %{        
for x in locals().values():
  if isinstance(x, type) and issubclass(x, SoFieldContainer):
    for name, thing in x.__dict__.items():
      if isinstance(thing, property):
        delattr(x, name)
%}
