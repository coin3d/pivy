/**
 * Copyright (c) 2002, Tamer Fahmy <tamer@tammura.at>
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
%module pivy

%{

#undef ANY

#include <Inventor/SbBasic.h>
#include <Inventor/SbPList.h>
#include <Inventor/So.h>
#include <Inventor/SoDB.h>
#include <Inventor/SoFullPath.h>
#include <Inventor/SoNodeKitPath.h>
#include <Inventor/SoInput.h>
#include <Inventor/SoInteraction.h>
#include <Inventor/SoOffscreenRenderer.h>
#include <Inventor/SoOutput.h>
#include <Inventor/SoPath.h>
#include <Inventor/SoPickedPoint.h>
#include <Inventor/SoPrimitiveVertex.h>
#include <Inventor/SoSceneManager.h>
#include <Inventor/SoType.h>
#include <Inventor/Sb.h>
#include <Inventor/SbBox.h>
#include <Inventor/SbBSPTree.h>
#include <Inventor/SbLinear.h>
#include <Inventor/SoLists.h>
#include <Inventor/SbBox2f.h>
#include <Inventor/SbBox2s.h>
#include <Inventor/SbBox3f.h>
#include <Inventor/SbColor.h>
#include <Inventor/SbColor4f.h>
#include <Inventor/SbCylinder.h>
#include <Inventor/SbDict.h>
#include <Inventor/SbHeap.h>
#include <Inventor/SbImage.h>
#include <Inventor/SbLine.h>
#include <Inventor/SbMatrix.h>
#include <Inventor/SbName.h>
#include <Inventor/SbOctTree.h>
#include <Inventor/SbPlane.h>
#include <Inventor/SbRotation.h>
#include <Inventor/SbSphere.h>
#include <Inventor/SbString.h>
#include <Inventor/SbTesselator.h>
#include <Inventor/SbTime.h>
#include <Inventor/SbVec2f.h>
#include <Inventor/SbVec2s.h>
#include <Inventor/SbVec3f.h>
#include <Inventor/SbVec4f.h>
#include <Inventor/SbViewVolume.h>
#include <Inventor/SbViewportRegion.h>
#include <Inventor/SbXfBox3f.h>

#include <Inventor/lock/SoLockMgr.h>

#include <Inventor/system/inttypes.h>

#include <Inventor/VRMLnodes/SoVRMLInterpOutput.h>
#include <Inventor/VRMLnodes/SoVRMLInterpolator.h>

#include <Inventor/actions/SoSubAction.h>
#include <Inventor/actions/SoActions.h>
#include <Inventor/actions/SoAction.h>
#include <Inventor/actions/SoBoxHighlightRenderAction.h>
#include <Inventor/actions/SoCallbackAction.h>
#include <Inventor/actions/SoGLRenderAction.h>
#include <Inventor/actions/SoGetBoundingBoxAction.h>
#include <Inventor/actions/SoGetMatrixAction.h>
#include <Inventor/actions/SoGetPrimitiveCountAction.h>
#include <Inventor/actions/SoHandleEventAction.h>
#include <Inventor/actions/SoLineHighlightRenderAction.h>
#include <Inventor/actions/SoPickAction.h>
#include <Inventor/actions/SoRayPickAction.h>
#include <Inventor/actions/SoSearchAction.h>
#include <Inventor/actions/SoWriteAction.h>

/* #include <Inventor/bundles/SoBundle.h> */
/* #include <Inventor/bundles/SoMaterialBundle.h> */
/* #include <Inventor/bundles/SoTextureCoordinateBundle.h> */

/* #include <Inventor/caches/SoBoundingBoxCache.h> */
/* #include <Inventor/caches/SoCache.h> */
/* #include <Inventor/caches/SoConvexDataCache.h> */
/* #include <Inventor/caches/SoGLCacheList.h> */
/* #include <Inventor/caches/SoGLRenderCache.h> */
/* #include <Inventor/caches/SoNormalCache.h> */
/* #include <Inventor/caches/SoTextureCoordinateCache.h> */

#include <Inventor/details/SoSubDetail.h>
#include <Inventor/details/SoDetail.h>
#include <Inventor/details/SoDetails.h>
#include <Inventor/details/SoConeDetail.h>
#include <Inventor/details/SoCubeDetail.h>
#include <Inventor/details/SoCylinderDetail.h>
#include <Inventor/details/SoFaceDetail.h>
#include <Inventor/details/SoLineDetail.h>
#include <Inventor/details/SoNodeKitDetail.h>
#include <Inventor/details/SoPointDetail.h>
#include <Inventor/details/SoTextDetail.h>

#include <Inventor/draggers/SoDragger.h>
#include <Inventor/draggers/SoCenterballDragger.h>
#include <Inventor/draggers/SoDirectionalLightDragger.h>
#include <Inventor/draggers/SoDragPointDragger.h>
#include <Inventor/draggers/SoHandleBoxDragger.h>
#include <Inventor/draggers/SoJackDragger.h>
#include <Inventor/draggers/SoPointLightDragger.h>
#include <Inventor/draggers/SoRotateCylindricalDragger.h>
#include <Inventor/draggers/SoRotateDiscDragger.h>
#include <Inventor/draggers/SoRotateSphericalDragger.h>
#include <Inventor/draggers/SoScale1Dragger.h>
#include <Inventor/draggers/SoScale2Dragger.h>
#include <Inventor/draggers/SoScale2UniformDragger.h>
#include <Inventor/draggers/SoScaleUniformDragger.h>
#include <Inventor/draggers/SoSpotLightDragger.h>
#include <Inventor/draggers/SoTabBoxDragger.h>
#include <Inventor/draggers/SoTabPlaneDragger.h>
#include <Inventor/draggers/SoTrackballDragger.h>
#include <Inventor/draggers/SoTransformBoxDragger.h>
#include <Inventor/draggers/SoTransformerDragger.h>
#include <Inventor/draggers/SoTranslate1Dragger.h>
#include <Inventor/draggers/SoTranslate2Dragger.h>

/* #include <Inventor/elements/SoSubElement.h> */
/* #include <Inventor/elements/SoElements.h> */
/* #include <Inventor/elements/SoAccumulatedElement.h> */
/* #include <Inventor/elements/SoAmbientColorElement.h> */
/* #include <Inventor/elements/SoAnnoText3CharOrientElement.h> */
/* #include <Inventor/elements/SoAnnoText3FontSizeHintElement.h> */
/* #include <Inventor/elements/SoAnnoText3RenderPrintElement.h> */
/* #include <Inventor/elements/SoBBoxModelMatrixElement.h> */
/* #include <Inventor/elements/SoCacheElement.h> */
/* #include <Inventor/elements/SoClipPlaneElement.h> */
/* #include <Inventor/elements/SoComplexityElement.h> */
/* #include <Inventor/elements/SoComplexityTypeElement.h> */
/* #include <Inventor/elements/SoCoordinateElement.h> */
/* #include <Inventor/elements/SoCreaseAngleElement.h> */
/* #include <Inventor/elements/SoCullElement.h> */
/* #include <Inventor/elements/SoGLColorIndexElement.h> */
/* #include <Inventor/elements/SoDecimationPercentageElement.h> */
/* #include <Inventor/elements/SoDecimationTypeElement.h> */
/* #include <Inventor/elements/SoDiffuseColorElement.h> */
/* #include <Inventor/elements/SoDrawStyleElement.h> */
/* #include <Inventor/elements/SoElement.h> */
/* #include <Inventor/elements/SoEmissiveColorElement.h> */
/* #include <Inventor/elements/SoEnvironmentElement.h> */
/* #include <Inventor/elements/SoFloatElement.h> */
/* #include <Inventor/elements/SoFocalDistanceElement.h> */
/* #include <Inventor/elements/SoFontNameElement.h> */
/* #include <Inventor/elements/SoFontSizeElement.h> */
/* #include <Inventor/elements/SoGLAmbientColorElement.h> */
/* #include <Inventor/elements/SoGLCacheContextElement.h> */
/* #include <Inventor/elements/SoGLClipPlaneElement.h> */
/* #include <Inventor/elements/SoGLCoordinateElement.h> */
/* #include <Inventor/elements/SoGLDiffuseColorElement.h> */
/* #include <Inventor/elements/SoGLDrawStyleElement.h> */
/* #include <Inventor/elements/SoGLEmissiveColorElement.h> */
/* #include <Inventor/elements/SoGLEnvironmentElement.h> */
/* #include <Inventor/elements/SoGLLazyElement.h> */
/* #include <Inventor/elements/SoGLLightIdElement.h> */
/* #include <Inventor/elements/SoGLLightModelElement.h> */
/* #include <Inventor/elements/SoGLLinePatternElement.h> */
/* #include <Inventor/elements/SoGLLineWidthElement.h> */
/* #include <Inventor/elements/SoGLModelMatrixElement.h> */
/* #include <Inventor/elements/SoGLNormalElement.h> */
/* #include <Inventor/elements/SoGLNormalizeElement.h> */
/* #include <Inventor/elements/SoGLPointSizeElement.h> */
/* #include <Inventor/elements/SoGLPolygonOffsetElement.h> */
/* #include <Inventor/elements/SoGLPolygonStippleElement.h> */
/* #include <Inventor/elements/SoGLProjectionMatrixElement.h> */
/* #include <Inventor/elements/SoGLRenderPassElement.h> */
/* #include <Inventor/elements/SoGLShadeModelElement.h> */
/* #include <Inventor/elements/SoGLShapeHintsElement.h> */
/* #include <Inventor/elements/SoGLShininessElement.h> */
/* #include <Inventor/elements/SoGLSpecularColorElement.h> */
/* #include <Inventor/elements/SoGLTextureCoordinateElement.h> */
/* #include <Inventor/elements/SoGLTextureEnabledElement.h> */
/* #include <Inventor/elements/SoGLTextureImageElement.h> */
/* #include <Inventor/elements/SoGLTextureMatrixElement.h> */
/* #include <Inventor/elements/SoGLUpdateAreaElement.h> */
/* #include <Inventor/elements/SoGLViewingMatrixElement.h> */
/* #include <Inventor/elements/SoGLViewportRegionElement.h> */
/* #include <Inventor/elements/SoInt32Element.h> */
/* #include <Inventor/elements/SoLazyElement.h> */
/* #include <Inventor/elements/SoLightAttenuationElement.h> */
/* #include <Inventor/elements/SoLightElement.h> */
/* #include <Inventor/elements/SoLightModelElement.h> */
/* #include <Inventor/elements/SoLinePatternElement.h> */
/* #include <Inventor/elements/SoLineWidthElement.h> */
/* #include <Inventor/elements/SoLocalBBoxMatrixElement.h> */
/* #include <Inventor/elements/SoMaterialBindingElement.h> */
/* #include <Inventor/elements/SoModelMatrixElement.h> */
/* #include <Inventor/elements/SoNormalBindingElement.h> */
/* #include <Inventor/elements/SoNormalElement.h> */
/* #include <Inventor/elements/SoOverrideElement.h> */
/* #include <Inventor/elements/SoPickRayElement.h> */
/* #include <Inventor/elements/SoPickStyleElement.h> */
/* #include <Inventor/elements/SoPointSizeElement.h> */
/* #include <Inventor/elements/SoPolygonOffsetElement.h> */
/* #include <Inventor/elements/SoProfileCoordinateElement.h> */
/* #include <Inventor/elements/SoProfileElement.h> */
/* #include <Inventor/elements/SoProjectionMatrixElement.h> */
/* #include <Inventor/elements/SoReplacedElement.h> */
/* #include <Inventor/elements/SoShapeHintsElement.h> */
/* #include <Inventor/elements/SoShapeStyleElement.h> */
/* #include <Inventor/elements/SoShininessElement.h> */
/* #include <Inventor/elements/SoSpecularColorElement.h> */
/* #include <Inventor/elements/SoSwitchElement.h> */
/* #include <Inventor/elements/SoTextOutlineEnabledElement.h> */
/* #include <Inventor/elements/SoTextureCoordinateBindingElement.h> */
/* #include <Inventor/elements/SoTextureCoordinateElement.h> */
/* #include <Inventor/elements/SoTextureImageElement.h> */
/* #include <Inventor/elements/SoTextureMatrixElement.h> */
/* #include <Inventor/elements/SoTextureOverrideElement.h> */
/* #include <Inventor/elements/SoTextureQualityElement.h> */
/* #include <Inventor/elements/SoTransparencyElement.h> */
/* #include <Inventor/elements/SoUnitsElement.h> */
/* #include <Inventor/elements/SoViewVolumeElement.h> */
/* #include <Inventor/elements/SoViewingMatrixElement.h> */
/* #include <Inventor/elements/SoViewportRegionElement.h> */
/* #include <Inventor/elements/SoWindowElement.h> */

#include <Inventor/engines/SoSubEngine.h>
#include <Inventor/engines/SoEngines.h>
#include <Inventor/engines/SoBoolOperation.h>
#include <Inventor/engines/SoCalculator.h>
#include <Inventor/engines/SoCompose.h>
#include <Inventor/engines/SoComposeMatrix.h>
#include <Inventor/engines/SoComposeRotation.h>
#include <Inventor/engines/SoComposeRotationFromTo.h>
#include <Inventor/engines/SoComposeVec2f.h>
#include <Inventor/engines/SoComposeVec3f.h>
#include <Inventor/engines/SoComposeVec4f.h>
#include <Inventor/engines/SoComputeBoundingBox.h>
#include <Inventor/engines/SoConcatenate.h>
#include <Inventor/engines/SoCounter.h>
#include <Inventor/engines/SoDecomposeMatrix.h>
#include <Inventor/engines/SoDecomposeRotation.h>
#include <Inventor/engines/SoDecomposeVec2f.h>
#include <Inventor/engines/SoDecomposeVec3f.h>
#include <Inventor/engines/SoDecomposeVec4f.h>
#include <Inventor/engines/SoElapsedTime.h>
#include <Inventor/engines/SoEngine.h>
#include <Inventor/engines/SoEngineOutput.h>
#include <Inventor/engines/SoFieldConverter.h>
#include <Inventor/engines/SoGate.h>
#include <Inventor/engines/SoInterpolate.h>
#include <Inventor/engines/SoInterpolateFloat.h>
#include <Inventor/engines/SoInterpolateRotation.h>
#include <Inventor/engines/SoInterpolateVec2f.h>
#include <Inventor/engines/SoInterpolateVec3f.h>
#include <Inventor/engines/SoInterpolateVec4f.h>
#include <Inventor/engines/SoOnOff.h>
#include <Inventor/engines/SoOneShot.h>
#include <Inventor/engines/SoOutputData.h>
#include <Inventor/engines/SoSelectOne.h>
#include <Inventor/engines/SoTimeCounter.h>
#include <Inventor/engines/SoTransformVec3f.h>
#include <Inventor/engines/SoTriggerAny.h>

#include <Inventor/errors/SoErrors.h>
#include <Inventor/errors/SoDebugError.h>
#include <Inventor/errors/SoError.h>
#include <Inventor/errors/SoMemoryError.h>
#include <Inventor/errors/SoReadError.h>

#include <Inventor/events/SoSubEvent.h>
#include <Inventor/events/SoButtonEvent.h>
#include <Inventor/events/SoEvent.h>
#include <Inventor/events/SoEvents.h>
#include <Inventor/events/SoKeyboardEvent.h>
#include <Inventor/events/SoLocation2Event.h>
#include <Inventor/events/SoMotion3Event.h>
#include <Inventor/events/SoMouseButtonEvent.h>
#include <Inventor/events/SoSpaceballButtonEvent.h>

#include <Inventor/fields/SoSubField.h>
#include <Inventor/fields/SoFields.h>
#include <Inventor/fields/SoField.h>
#include <Inventor/fields/SoFieldContainer.h>
#include <Inventor/fields/SoFieldData.h>
#include <Inventor/fields/SoMFBitMask.h>
#include <Inventor/fields/SoMFBool.h>
#include <Inventor/fields/SoMFColor.h>
#include <Inventor/fields/SoMFEngine.h>
#include <Inventor/fields/SoMFEnum.h>
#include <Inventor/fields/SoMFFloat.h>
#include <Inventor/fields/SoMFInt32.h>
#include <Inventor/fields/SoMFLong.h>
#include <Inventor/fields/SoMFMatrix.h>
#include <Inventor/fields/SoMFName.h>
#include <Inventor/fields/SoMFNode.h>
#include <Inventor/fields/SoMFPath.h>
#include <Inventor/fields/SoMFPlane.h>
#include <Inventor/fields/SoMFRotation.h>
#include <Inventor/fields/SoMFShort.h>
#include <Inventor/fields/SoMFString.h>
#include <Inventor/fields/SoMFTime.h>
#include <Inventor/fields/SoMFUInt32.h>
#include <Inventor/fields/SoMFULong.h>
#include <Inventor/fields/SoMFUShort.h>
#include <Inventor/fields/SoMFVec2f.h>
#include <Inventor/fields/SoMFVec3f.h>
#include <Inventor/fields/SoMFVec4f.h>
#include <Inventor/fields/SoMField.h>
#include <Inventor/fields/SoSFBitMask.h>
#include <Inventor/fields/SoSFBool.h>
#include <Inventor/fields/SoSFColor.h>
#include <Inventor/fields/SoSFEngine.h>
#include <Inventor/fields/SoSFEnum.h>
#include <Inventor/fields/SoSFFloat.h>
#include <Inventor/fields/SoSFImage.h>
#include <Inventor/fields/SoSFInt32.h>
#include <Inventor/fields/SoSFLong.h>
#include <Inventor/fields/SoSFMatrix.h>
#include <Inventor/fields/SoSFName.h>
#include <Inventor/fields/SoSFNode.h>
#include <Inventor/fields/SoSFPath.h>
#include <Inventor/fields/SoSFPlane.h>
#include <Inventor/fields/SoSFRotation.h>
#include <Inventor/fields/SoSFShort.h>
#include <Inventor/fields/SoSFString.h>
#include <Inventor/fields/SoSFTime.h>
#include <Inventor/fields/SoSFTrigger.h>
#include <Inventor/fields/SoSFUInt32.h>
#include <Inventor/fields/SoSFULong.h>
#include <Inventor/fields/SoSFUShort.h>
#include <Inventor/fields/SoSFVec2f.h>
#include <Inventor/fields/SoSFVec3f.h>
#include <Inventor/fields/SoSFVec4f.h>
#include <Inventor/fields/SoSField.h>

#include <Inventor/manips/SoClipPlaneManip.h>
#include <Inventor/manips/SoDirectionalLightManip.h>
#include <Inventor/manips/SoPointLightManip.h>
#include <Inventor/manips/SoSpotLightManip.h>
#include <Inventor/manips/SoTransformManip.h>
#include <Inventor/manips/SoCenterballManip.h>
#include <Inventor/manips/SoHandleBoxManip.h>
#include <Inventor/manips/SoJackManip.h>
#include <Inventor/manips/SoTabBoxManip.h>
#include <Inventor/manips/SoTrackballManip.h>
#include <Inventor/manips/SoTransformBoxManip.h>
#include <Inventor/manips/SoTransformerManip.h>

#include <Inventor/misc/SoAuditorList.h>
#include <Inventor/misc/SoBase.h>
#include <Inventor/misc/SoBasic.h>
#include <Inventor/misc/SoByteStream.h>
#include <Inventor/misc/SoCallbackList.h>
#include <Inventor/misc/SoChildList.h>
#include <Inventor/misc/SoNormalGenerator.h>
#include <Inventor/misc/SoNotification.h>
#include <Inventor/misc/SoTranReceiver.h>
#include <Inventor/misc/SoState.h>
#include <Inventor/misc/SoTranscribe.h>
#include <Inventor/misc/SoTranSender.h>
#include <Inventor/misc/SoLightPath.h>
#include <Inventor/misc/SoTempPath.h>

#include <Inventor/lists/SbList.h>
#include <Inventor/lists/SbPList.h>
#include <Inventor/lists/SbIntList.h>
#include <Inventor/lists/SbVec3fList.h>
#include <Inventor/lists/SbStringList.h>
#include <Inventor/lists/SoActionMethodList.h>
#include <Inventor/lists/SoAuditorList.h>
#include <Inventor/lists/SoBaseList.h>
#include <Inventor/lists/SoCallbackList.h>
#include <Inventor/lists/SoDetailList.h>
#include <Inventor/lists/SoEnabledElementsList.h>
#include <Inventor/lists/SoEngineList.h>
#include <Inventor/lists/SoEngineOutputList.h>
#include <Inventor/lists/SoFieldList.h>
#include <Inventor/lists/SoNodeList.h>
#include <Inventor/lists/SoPathList.h>
#include <Inventor/lists/SoPickedPointList.h>
#include <Inventor/lists/SoTypeList.h>
#include <Inventor/lists/SoVRMLInterpOutputList.h>

#include <Inventor/nodekits/SoSubKit.h>
#include <Inventor/nodekits/SoNodeKit.h>
#include <Inventor/nodekits/SoNodeKitListPart.h>
#include <Inventor/nodekits/SoNodekitCatalog.h>
#include <Inventor/nodekits/SoBaseKit.h>
#include <Inventor/nodekits/SoAppearanceKit.h>
#include <Inventor/nodekits/SoCameraKit.h>
#include <Inventor/nodekits/SoInteractionKit.h>
#include <Inventor/nodekits/SoLightKit.h>
#include <Inventor/nodekits/SoSceneKit.h>
#include <Inventor/nodekits/SoSeparatorKit.h>
#include <Inventor/nodekits/SoShapeKit.h>
#include <Inventor/nodekits/SoWrapperKit.h>

#include <Inventor/nodes/SoSubNode.h>
#include <Inventor/nodes/SoNodes.h>
#include <Inventor/nodes/SoAnnotation.h>
#include <Inventor/nodes/SoAntiSquish.h>
#include <Inventor/nodes/SoArray.h>
#include <Inventor/nodes/SoAsciiText.h>
#include <Inventor/nodes/SoBaseColor.h>
#include <Inventor/nodes/SoBlinker.h>
#include <Inventor/nodes/SoCallback.h>
#include <Inventor/nodes/SoCamera.h>
#include <Inventor/nodes/SoClipPlane.h>
#include <Inventor/nodes/SoColorIndex.h>
#include <Inventor/nodes/SoComplexity.h>
#include <Inventor/nodes/SoCone.h>
#include <Inventor/nodes/SoCoordinate3.h>
#include <Inventor/nodes/SoCoordinate4.h>
#include <Inventor/nodes/SoCube.h>
#include <Inventor/nodes/SoCylinder.h>
#include <Inventor/nodes/SoDirectionalLight.h>
#include <Inventor/nodes/SoDrawStyle.h>
#include <Inventor/nodes/SoEnvironment.h>
#include <Inventor/nodes/SoEventCallback.h>
#include <Inventor/nodes/SoExtSelection.h>
#include <Inventor/nodes/SoFaceSet.h>
#include <Inventor/nodes/SoFile.h>
#include <Inventor/nodes/SoFont.h>
#include <Inventor/nodes/SoFontStyle.h>
#include <Inventor/nodes/SoGroup.h>
#include <Inventor/nodes/SoImage.h>
#include <Inventor/nodes/SoIndexedFaceSet.h>
#include <Inventor/nodes/SoIndexedLineSet.h>
#include <Inventor/nodes/SoIndexedNurbsCurve.h>
#include <Inventor/nodes/SoIndexedNurbsSurface.h>
#include <Inventor/nodes/SoIndexedShape.h>
#include <Inventor/nodes/SoIndexedTriangleStripSet.h>
#include <Inventor/nodes/SoInfo.h>
#include <Inventor/nodes/SoLOD.h>
#include <Inventor/nodes/SoLabel.h>
#include <Inventor/nodes/SoLevelOfDetail.h>
#include <Inventor/nodes/SoLight.h>
#include <Inventor/nodes/SoLightModel.h>
#include <Inventor/nodes/SoLineSet.h>
#include <Inventor/nodes/SoLinearProfile.h>
#include <Inventor/nodes/SoLocateHighlight.h>
#include <Inventor/nodes/SoMarkerSet.h>
#include <Inventor/nodes/SoMaterial.h>
#include <Inventor/nodes/SoMaterialBinding.h>
#include <Inventor/nodes/SoMatrixTransform.h>
#include <Inventor/nodes/SoMultipleCopy.h>
#include <Inventor/nodes/SoNode.h>
#include <Inventor/nodes/SoNonIndexedShape.h>
#include <Inventor/nodes/SoNormal.h>
#include <Inventor/nodes/SoNormalBinding.h>
#include <Inventor/nodes/SoNurbsCurve.h>
#include <Inventor/nodes/SoNurbsProfile.h>
#include <Inventor/nodes/SoNurbsSurface.h>
#include <Inventor/nodes/SoOrthographicCamera.h>
#include <Inventor/nodes/SoPackedColor.h>
#include <Inventor/nodes/SoPathSwitch.h>
#include <Inventor/nodes/SoPendulum.h>
#include <Inventor/nodes/SoPerspectiveCamera.h>
#include <Inventor/nodes/SoPickStyle.h>
#include <Inventor/nodes/SoPointLight.h>
#include <Inventor/nodes/SoPointSet.h>
#include <Inventor/nodes/SoPolygonOffset.h>
#include <Inventor/nodes/SoProfile.h>
#include <Inventor/nodes/SoProfileCoordinate2.h>
#include <Inventor/nodes/SoProfileCoordinate3.h>
#include <Inventor/nodes/SoQuadMesh.h>
#include <Inventor/nodes/SoResetTransform.h>
#include <Inventor/nodes/SoRotation.h>
#include <Inventor/nodes/SoRotationXYZ.h>
#include <Inventor/nodes/SoRotor.h>
#include <Inventor/nodes/SoScale.h>
#include <Inventor/nodes/SoSelection.h>
#include <Inventor/nodes/SoSeparator.h>
#include <Inventor/nodes/SoShape.h>
#include <Inventor/nodes/SoShapeHints.h>
#include <Inventor/nodes/SoShuttle.h>
#include <Inventor/nodes/SoSphere.h>
#include <Inventor/nodes/SoSpotLight.h>
#include <Inventor/nodes/SoSurroundScale.h>
#include <Inventor/nodes/SoSwitch.h>
#include <Inventor/nodes/SoText2.h>
#include <Inventor/nodes/SoText3.h>
#include <Inventor/nodes/SoTexture2.h>
#include <Inventor/nodes/SoTexture2Transform.h>
#include <Inventor/nodes/SoTextureCoordinate2.h>
#include <Inventor/nodes/SoTextureCoordinateBinding.h>
#include <Inventor/nodes/SoTextureCoordinateDefault.h>
#include <Inventor/nodes/SoTextureCoordinateEnvironment.h>
#include <Inventor/nodes/SoTextureCoordinateFunction.h>
#include <Inventor/nodes/SoTextureCoordinatePlane.h>
#include <Inventor/nodes/SoTransform.h>
#include <Inventor/nodes/SoTransformSeparator.h>
#include <Inventor/nodes/SoTransformation.h>
#include <Inventor/nodes/SoTranslation.h>
#include <Inventor/nodes/SoTriangleStripSet.h>
#include <Inventor/nodes/SoUnits.h>
#include <Inventor/nodes/SoVertexProperty.h>
#include <Inventor/nodes/SoVertexShape.h>
#include <Inventor/nodes/SoWWWAnchor.h>
#include <Inventor/nodes/SoWWWInline.h>



/* #include <Inventor/projectors/SbProjectors.h> */
/* #include <Inventor/projectors/SbCylinderPlaneProjector.h> */
/* #include <Inventor/projectors/SbCylinderProjector.h> */
/* #include <Inventor/projectors/SbCylinderSectionProjector.h> */
/* #include <Inventor/projectors/SbCylinderSheetProjector.h> */
/* #include <Inventor/projectors/SbLineProjector.h> */
/* #include <Inventor/projectors/SbPlaneProjector.h> */
/* #include <Inventor/projectors/SbProjector.h> */
/* #include <Inventor/projectors/SbSpherePlaneProjector.h> */
/* #include <Inventor/projectors/SbSphereProjector.h> */
/* #include <Inventor/projectors/SbSphereSectionProjector.h> */
/* #include <Inventor/projectors/SbSphereSheetProjector.h> */

#include <Inventor/sensors/SoSensors.h>
#include <Inventor/sensors/SoAlarmSensor.h>
#include <Inventor/sensors/SoDataSensor.h>
#include <Inventor/sensors/SoDelayQueueSensor.h>
#include <Inventor/sensors/SoFieldSensor.h>
#include <Inventor/sensors/SoIdleSensor.h>
#include <Inventor/sensors/SoNodeSensor.h>
#include <Inventor/sensors/SoOneShotSensor.h>
#include <Inventor/sensors/SoPathSensor.h>
#include <Inventor/sensors/SoSensor.h>
#include <Inventor/sensors/SoSensorManager.h>
#include <Inventor/sensors/SoTimerQueueSensor.h>
#include <Inventor/sensors/SoTimerSensor.h>

#include <Inventor/Qt/devices/SoQtDevice.h>
#include <Inventor/Qt/devices/SoQtKeyboard.h>
#include <Inventor/Qt/devices/SoQtMouse.h>
#include <Inventor/Qt/devices/SoQtSpaceball.h>
#include <Inventor/Qt/SoQtBasic.h>
#include <Inventor/Qt/SoQtComponent.h>
#include <Inventor/Qt/SoQtCursor.h>
#include <Inventor/Qt/SoQtGLWidget.h>
#include <Inventor/Qt/SoQt.h>
#include <Inventor/Qt/SoQtObject.h>
#include <Inventor/Qt/SoQtRenderArea.h>
#include <Inventor/Qt/viewers/SoQtViewer.h>
#include <Inventor/Qt/viewers/SoQtConstrainedViewer.h>
#include <Inventor/Qt/viewers/SoQtFullViewer.h>
#include <Inventor/Qt/viewers/SoQtExaminerViewer.h>
#include <Inventor/Qt/viewers/SoQtFlyViewer.h>
#include <Inventor/Qt/viewers/SoQtPlaneViewer.h>
#include <Inventor/Qt/widgets/SoQtPopupMenu.h>

/* #include <Inventor/Gtk/SoGtkGraphEditor.h> */
/* #include <Inventor/Gtk/SoGtkRoster.h> */
/* #include <Inventor/Gtk/SoGtk.h> */
/* #include <Inventor/Gtk/SoGtkBasic.h> */
/* #include <Inventor/Gtk/SoGtkObject.h> */
/* #include <Inventor/Gtk/SoGtkCursor.h> */
/* #include <Inventor/Gtk/SoGtkComponent.h> */
/* #include <Inventor/Gtk/SoGtkGLWidget.h> */
/* #include <Inventor/Gtk/SoGtkRenderArea.h> */
/* #include <Inventor/Gtk/devices/SoGtkDevice.h> */
/* #include <Inventor/Gtk/devices/SoGtkInputFocus.h> */
/* #include <Inventor/Gtk/devices/SoGtkKeyboard.h> */
/* #include <Inventor/Gtk/devices/SoGtkMouse.h> */
/* #include <Inventor/Gtk/devices/SoGtkSpaceball.h> */
/* #include <Inventor/Gtk/widgets/SoGtkPopupMenu.h> */
/* #include <Inventor/Gtk/viewers/SoGtkFullViewer.h> */
/* #include <Inventor/Gtk/viewers/SoGtkExaminerViewer.h> */
/* #include <Inventor/Gtk/viewers/SoGtkPlaneViewer.h> */
/* #include <Inventor/Gtk/viewers/SoGtkViewer.h> */
/* #include <Inventor/Gtk/viewers/SoGtkConstrainedViewer.h> */
/* #include <Inventor/Gtk/viewers/SoGtkFlyViewer.h> */

PyObject *
cast(PyObject *self, PyObject *args)
{
  swig_type_info *swig_type = 0;
  void *cast_obj = 0;
  int type_len;
  char *type, *ptr_type;
  PyObject *obj;

  if (!PyArg_ParseTuple(args,"Os", &obj, &type)) return NULL;
  type_len = strlen(type);

  /*
   * add a pointer sign to the string coming from the interpreter
   * e.g. "SoSeparator" becomes "SoSeparator *" - so that SWIG_TypeQuery()
   * can do its job.
   */
  ptr_type = (char *) malloc(type_len+3);
  if (ptr_type == NULL) return NULL;

  memset(ptr_type, 0, type_len+3);
  strncpy(ptr_type, type, type_len);
  strcat(ptr_type, " *");

  if ((swig_type = SWIG_TypeQuery(ptr_type)) == 0) { free(ptr_type); return NULL; }

  free(ptr_type);

  if ((SWIG_ConvertPtr(obj,(void **) &cast_obj, NULL, 1)) == -1) return NULL;

  return SWIG_NewPointerObj((void *) cast_obj, swig_type, 0);
}
%}


/**
 * SWIG - interface includes and general typemap definitions starts here
 **/

%include "typemaps.i"

%native(cast) PyObject *cast(PyObject *self, PyObject *args);

%rename(output) print(FILE * fp) const;
%rename(output) print(FILE * const fp) const;
%rename(output) print(FILE * const file = stdout);
%rename(srcFrom) from;
%rename(destTo) to;

/* generic typemaps to allow using python types instead of instances
 * within the python interpreter
 */
%typemap(in) SbName & {
  if (PyString_Check($input)) {
    $1 = new SbName(PyString_AsString($input));
  } else {
    SWIG_ConvertPtr($input,(void **) &$1, SWIGTYPE_p_SbName, 1);
  }
}

%typemap(in) SbString & {
  if (PyString_Check($input)) {
    $1 = new SbString(PyString_AsString($input));
  } else {
    SWIG_ConvertPtr($input,(void **) &$1, SWIGTYPE_p_SbString, 1);
  }
}

%typemap(in) SbTime & {
  if (PyFloat_Check($input)) {
    $1 = new SbTime(PyFloat_AsDouble($input));
  } else {
    SWIG_ConvertPtr($input,(void **) &$1, SWIGTYPE_p_SbTime, 1);
  }
}

%typemap(in) FILE * {
  if (PyFile_Check($input)) {
	$1 = PyFile_AsFile($input);;
  } else {
	PyErr_SetString(PyExc_TypeError, "expected a file object.");
  }
}

%include Inventor/SbBasic.h
%include Inventor/SbPList.h
%include Inventor/So.h
%include Inventor/SoDB.h
%include Inventor/SoFullPath.h
%include Inventor/SoNodeKitPath.h
%include Inventor/SoInput.h
%include Inventor/SoInteraction.h
%include Inventor/SoOffscreenRenderer.h
%include Inventor/SoOutput.h
%include Inventor/SoPath.h
%include Inventor/SoPickedPoint.h
%include Inventor/SoPrimitiveVertex.h
%include Inventor/SoSceneManager.h
%include Inventor/SoType.h
%include Inventor/Sb.h
%include Inventor/SbBox.h
%include Inventor/SbBSPTree.h
%include Inventor/SbLinear.h
%include Inventor/SoLists.h
%include Inventor/SbBox2f.h
%include Inventor/SbBox2s.h
%include Inventor/SbBox3f.h
%include Inventor/SbColor.h
%include Inventor/SbColor4f.h
%include Inventor/SbCylinder.h
%include Inventor/SbDict.h
%include Inventor/SbHeap.h
%include Inventor/SbImage.h
%include Inventor/SbLine.h
%include Inventor/SbMatrix.h
%include Inventor/SbName.h
%include Inventor/SbOctTree.h
%include Inventor/SbPlane.h
%include Inventor/SbRotation.h
%include Inventor/SbSphere.h
%include Inventor/SbString.h
%include Inventor/SbTesselator.h
%include Inventor/SbTime.h
%include Inventor/SbVec2f.h
%include Inventor/SbVec2s.h
%include Inventor/SbVec3f.h
%include Inventor/SbVec4f.h
%include Inventor/SbViewVolume.h
%include Inventor/SbViewportRegion.h
%include Inventor/SbXfBox3f.h

%include Inventor/lock/SoLockMgr.h

%include Inventor/system/inttypes.h

%include Inventor/VRMLnodes/SoVRMLInterpOutput.h
%include Inventor/VRMLnodes/SoVRMLInterpolator.h

%include Inventor/actions/SoSubAction.h
%include Inventor/actions/SoActions.h
%include Inventor/actions/SoAction.h
%include Inventor/actions/SoBoxHighlightRenderAction.h
%include Inventor/actions/SoCallbackAction.h
%include Inventor/actions/SoGLRenderAction.h
%include Inventor/actions/SoGetBoundingBoxAction.h
%include Inventor/actions/SoGetMatrixAction.h
%include Inventor/actions/SoGetPrimitiveCountAction.h
%include Inventor/actions/SoHandleEventAction.h
%include Inventor/actions/SoLineHighlightRenderAction.h
%include Inventor/actions/SoPickAction.h
%include Inventor/actions/SoRayPickAction.h
%include Inventor/actions/SoSearchAction.h
%include Inventor/actions/SoWriteAction.h

/* %include Inventor/bundles/SoBundle.h */
/* %include Inventor/bundles/SoMaterialBundle.h */
/* %include Inventor/bundles/SoTextureCoordinateBundle.h */

/* %include Inventor/caches/SoBoundingBoxCache.h */
/* %include Inventor/caches/SoCache.h */
/* %include Inventor/caches/SoConvexDataCache.h */
/* %include Inventor/caches/SoGLCacheList.h */
/* %include Inventor/caches/SoGLRenderCache.h */
/* %include Inventor/caches/SoNormalCache.h */
/* %include Inventor/caches/SoTextureCoordinateCache.h */

%include Inventor/details/SoSubDetail.h
%include Inventor/details/SoDetail.h
%include Inventor/details/SoDetails.h
%include Inventor/details/SoConeDetail.h
%include Inventor/details/SoCubeDetail.h
%include Inventor/details/SoCylinderDetail.h
%include Inventor/details/SoFaceDetail.h
%include Inventor/details/SoLineDetail.h
%include Inventor/details/SoNodeKitDetail.h
%include Inventor/details/SoPointDetail.h
%include Inventor/details/SoTextDetail.h

%include Inventor/draggers/SoDragger.h
%include Inventor/draggers/SoCenterballDragger.h
%include Inventor/draggers/SoDirectionalLightDragger.h
%include Inventor/draggers/SoDragPointDragger.h
%include Inventor/draggers/SoHandleBoxDragger.h
%include Inventor/draggers/SoJackDragger.h
%include Inventor/draggers/SoPointLightDragger.h
%include Inventor/draggers/SoRotateCylindricalDragger.h
%include Inventor/draggers/SoRotateDiscDragger.h
%include Inventor/draggers/SoRotateSphericalDragger.h
%include Inventor/draggers/SoScale1Dragger.h
%include Inventor/draggers/SoScale2Dragger.h
%include Inventor/draggers/SoScale2UniformDragger.h
%include Inventor/draggers/SoScaleUniformDragger.h
%include Inventor/draggers/SoSpotLightDragger.h
%include Inventor/draggers/SoTabBoxDragger.h
%include Inventor/draggers/SoTabPlaneDragger.h
%include Inventor/draggers/SoTrackballDragger.h
%include Inventor/draggers/SoTransformBoxDragger.h
%include Inventor/draggers/SoTransformerDragger.h
%include Inventor/draggers/SoTranslate1Dragger.h
%include Inventor/draggers/SoTranslate2Dragger.h

/* %include Inventor/elements/SoSubElement.h */
/* %include Inventor/elements/SoElements.h */
/* %include Inventor/elements/SoAccumulatedElement.h */
/* %include Inventor/elements/SoAmbientColorElement.h */
/* %include Inventor/elements/SoAnnoText3CharOrientElement.h */
/* %include Inventor/elements/SoAnnoText3FontSizeHintElement.h */
/* %include Inventor/elements/SoAnnoText3RenderPrintElement.h */
/* %include Inventor/elements/SoBBoxModelMatrixElement.h */
/* %include Inventor/elements/SoCacheElement.h */
/* %include Inventor/elements/SoClipPlaneElement.h */
/* %include Inventor/elements/SoComplexityElement.h */
/* %include Inventor/elements/SoComplexityTypeElement.h */
/* %include Inventor/elements/SoCoordinateElement.h */
/* %include Inventor/elements/SoCreaseAngleElement.h */
/* %include Inventor/elements/SoCullElement.h */
/* %include Inventor/elements/SoGLColorIndexElement.h */
/* %include Inventor/elements/SoDecimationPercentageElement.h */
/* %include Inventor/elements/SoDecimationTypeElement.h */
/* %include Inventor/elements/SoDiffuseColorElement.h */
/* %include Inventor/elements/SoDrawStyleElement.h */
/* %include Inventor/elements/SoElement.h */
/* %include Inventor/elements/SoEmissiveColorElement.h */
/* %include Inventor/elements/SoEnvironmentElement.h */
/* %include Inventor/elements/SoFloatElement.h */
/* %include Inventor/elements/SoFocalDistanceElement.h */
/* %include Inventor/elements/SoFontNameElement.h */
/* %include Inventor/elements/SoFontSizeElement.h */
/* %include Inventor/elements/SoGLAmbientColorElement.h */
/* %include Inventor/elements/SoGLCacheContextElement.h */
/* %include Inventor/elements/SoGLClipPlaneElement.h */
/* %include Inventor/elements/SoGLCoordinateElement.h */
/* %include Inventor/elements/SoGLDiffuseColorElement.h */
/* %include Inventor/elements/SoGLDrawStyleElement.h */
/* %include Inventor/elements/SoGLEmissiveColorElement.h */
/* %include Inventor/elements/SoGLEnvironmentElement.h */
/* %include Inventor/elements/SoGLLazyElement.h */
/* %include Inventor/elements/SoGLLightIdElement.h */
/* %include Inventor/elements/SoGLLightModelElement.h */
/* %include Inventor/elements/SoGLLinePatternElement.h */
/* %include Inventor/elements/SoGLLineWidthElement.h */
/* %include Inventor/elements/SoGLModelMatrixElement.h */
/* %include Inventor/elements/SoGLNormalElement.h */
/* %include Inventor/elements/SoGLNormalizeElement.h */
/* %include Inventor/elements/SoGLPointSizeElement.h */
/* %include Inventor/elements/SoGLPolygonOffsetElement.h */
/* %include Inventor/elements/SoGLPolygonStippleElement.h */
/* %include Inventor/elements/SoGLProjectionMatrixElement.h */
/* %include Inventor/elements/SoGLRenderPassElement.h */
/* %include Inventor/elements/SoGLShadeModelElement.h */
/* %include Inventor/elements/SoGLShapeHintsElement.h */
/* %include Inventor/elements/SoGLShininessElement.h */
/* %include Inventor/elements/SoGLSpecularColorElement.h */
/* %include Inventor/elements/SoGLTextureCoordinateElement.h */
/* %include Inventor/elements/SoGLTextureEnabledElement.h */
/* %include Inventor/elements/SoGLTextureImageElement.h */
/* %include Inventor/elements/SoGLTextureMatrixElement.h */
/* %include Inventor/elements/SoGLUpdateAreaElement.h */
/* %include Inventor/elements/SoGLViewingMatrixElement.h */
/* %include Inventor/elements/SoGLViewportRegionElement.h */
/* %include Inventor/elements/SoInt32Element.h */
/* %include Inventor/elements/SoLazyElement.h */
/* %include Inventor/elements/SoLightAttenuationElement.h */
/* %include Inventor/elements/SoLightElement.h */
/* %include Inventor/elements/SoLightModelElement.h */
/* %include Inventor/elements/SoLinePatternElement.h */
/* %include Inventor/elements/SoLineWidthElement.h */
/* %include Inventor/elements/SoLocalBBoxMatrixElement.h */
/* %include Inventor/elements/SoMaterialBindingElement.h */
/* %include Inventor/elements/SoModelMatrixElement.h */
/* %include Inventor/elements/SoNormalBindingElement.h */
/* %include Inventor/elements/SoNormalElement.h */
/* %include Inventor/elements/SoOverrideElement.h */
/* %include Inventor/elements/SoPickRayElement.h */
/* %include Inventor/elements/SoPickStyleElement.h */
/* %include Inventor/elements/SoPointSizeElement.h */
/* %include Inventor/elements/SoPolygonOffsetElement.h */
/* %include Inventor/elements/SoProfileCoordinateElement.h */
/* %include Inventor/elements/SoProfileElement.h */
/* %include Inventor/elements/SoProjectionMatrixElement.h */
/* %include Inventor/elements/SoReplacedElement.h */
/* %include Inventor/elements/SoShapeHintsElement.h */
/* %include Inventor/elements/SoShapeStyleElement.h */
/* %include Inventor/elements/SoShininessElement.h */
/* %include Inventor/elements/SoSpecularColorElement.h */
/* %include Inventor/elements/SoSwitchElement.h */
/* %include Inventor/elements/SoTextOutlineEnabledElement.h */
/* %include Inventor/elements/SoTextureCoordinateBindingElement.h */
/* %include Inventor/elements/SoTextureCoordinateElement.h */
/* %include Inventor/elements/SoTextureImageElement.h */
/* %include Inventor/elements/SoTextureMatrixElement.h */
/* %include Inventor/elements/SoTextureOverrideElement.h */
/* %include Inventor/elements/SoTextureQualityElement.h */
/* %include Inventor/elements/SoTransparencyElement.h */
/* %include Inventor/elements/SoUnitsElement.h */
/* %include Inventor/elements/SoViewVolumeElement.h */
/* %include Inventor/elements/SoViewingMatrixElement.h */
/* %include Inventor/elements/SoViewportRegionElement.h */
/* %include Inventor/elements/SoWindowElement.h */

%include Inventor/engines/SoSubEngine.h
%include Inventor/engines/SoEngines.h
%include Inventor/engines/SoBoolOperation.h
%include Inventor/engines/SoCalculator.h
%include Inventor/engines/SoCompose.h
%include Inventor/engines/SoComposeMatrix.h
%include Inventor/engines/SoComposeRotation.h
%include Inventor/engines/SoComposeRotationFromTo.h
%include Inventor/engines/SoComposeVec2f.h
%include Inventor/engines/SoComposeVec3f.h
%include Inventor/engines/SoComposeVec4f.h
%include Inventor/engines/SoComputeBoundingBox.h
%include Inventor/engines/SoConcatenate.h
%include Inventor/engines/SoCounter.h
%include Inventor/engines/SoDecomposeMatrix.h
%include Inventor/engines/SoDecomposeRotation.h
%include Inventor/engines/SoDecomposeVec2f.h
%include Inventor/engines/SoDecomposeVec3f.h
%include Inventor/engines/SoDecomposeVec4f.h
%include Inventor/engines/SoElapsedTime.h
%include Inventor/engines/SoEngine.h
%include Inventor/engines/SoEngineOutput.h
%include Inventor/engines/SoFieldConverter.h
%include Inventor/engines/SoGate.h
%include Inventor/engines/SoInterpolate.h
%include Inventor/engines/SoInterpolateFloat.h
%include Inventor/engines/SoInterpolateRotation.h
%include Inventor/engines/SoInterpolateVec2f.h
%include Inventor/engines/SoInterpolateVec3f.h
%include Inventor/engines/SoInterpolateVec4f.h
%include Inventor/engines/SoOnOff.h
%include Inventor/engines/SoOneShot.h
%include Inventor/engines/SoOutputData.h
%include Inventor/engines/SoSelectOne.h
%include Inventor/engines/SoTimeCounter.h
%include Inventor/engines/SoTransformVec3f.h
%include Inventor/engines/SoTriggerAny.h

%include Inventor/errors/SoErrors.h
%include Inventor/errors/SoDebugError.h
%include Inventor/errors/SoError.h
%include Inventor/errors/SoMemoryError.h
%include Inventor/errors/SoReadError.h

%include Inventor/events/SoSubEvent.h
%include Inventor/events/SoButtonEvent.h
%include Inventor/events/SoEvent.h
%include Inventor/events/SoEvents.h
%include Inventor/events/SoKeyboardEvent.h
%include Inventor/events/SoLocation2Event.h
%include Inventor/events/SoMotion3Event.h
%include Inventor/events/SoMouseButtonEvent.h
%include Inventor/events/SoSpaceballButtonEvent.h

%include Inventor/fields/SoSubField.h
%include Inventor/fields/SoFields.h
%include Inventor/fields/SoField.h
%include Inventor/fields/SoFieldContainer.h
%include Inventor/fields/SoFieldData.h
%include Inventor/fields/SoMFBitMask.h
%include Inventor/fields/SoMFBool.h
%include Inventor/fields/SoMFColor.h
%include Inventor/fields/SoMFEngine.h
%include Inventor/fields/SoMFEnum.h
%include Inventor/fields/SoMFFloat.h
%include Inventor/fields/SoMFInt32.h
%include Inventor/fields/SoMFLong.h
%include Inventor/fields/SoMFMatrix.h
%include Inventor/fields/SoMFName.h
%include Inventor/fields/SoMFNode.h
%include Inventor/fields/SoMFPath.h
%include Inventor/fields/SoMFPlane.h
%include Inventor/fields/SoMFRotation.h
%include Inventor/fields/SoMFShort.h
%include Inventor/fields/SoMFString.h
%include Inventor/fields/SoMFTime.h
%include Inventor/fields/SoMFUInt32.h
%include Inventor/fields/SoMFULong.h
%include Inventor/fields/SoMFUShort.h
%include Inventor/fields/SoMFVec2f.h
%include Inventor/fields/SoMFVec3f.h
%include Inventor/fields/SoMFVec4f.h
%include Inventor/fields/SoMField.h
%include Inventor/fields/SoSFBitMask.h
%include Inventor/fields/SoSFBool.h
%include Inventor/fields/SoSFColor.h
%include Inventor/fields/SoSFEngine.h
%include Inventor/fields/SoSFEnum.h
%include Inventor/fields/SoSFFloat.h
%include Inventor/fields/SoSFImage.h
%include Inventor/fields/SoSFInt32.h
%include Inventor/fields/SoSFLong.h
%include Inventor/fields/SoSFMatrix.h
%include Inventor/fields/SoSFName.h
%include Inventor/fields/SoSFNode.h
%include Inventor/fields/SoSFPath.h
%include Inventor/fields/SoSFPlane.h
%include Inventor/fields/SoSFRotation.h
%include Inventor/fields/SoSFShort.h
%include Inventor/fields/SoSFString.h
%include Inventor/fields/SoSFTime.h
%include Inventor/fields/SoSFTrigger.h
%include Inventor/fields/SoSFUInt32.h
%include Inventor/fields/SoSFULong.h
%include Inventor/fields/SoSFUShort.h
%include Inventor/fields/SoSFVec2f.h
%include Inventor/fields/SoSFVec3f.h
%include Inventor/fields/SoSFVec4f.h
%include Inventor/fields/SoSField.h

%include Inventor/manips/SoClipPlaneManip.h
%include Inventor/manips/SoDirectionalLightManip.h
%include Inventor/manips/SoPointLightManip.h
%include Inventor/manips/SoSpotLightManip.h
%include Inventor/manips/SoTransformManip.h
%include Inventor/manips/SoCenterballManip.h
%include Inventor/manips/SoHandleBoxManip.h
%include Inventor/manips/SoJackManip.h
%include Inventor/manips/SoTabBoxManip.h
%include Inventor/manips/SoTrackballManip.h
%include Inventor/manips/SoTransformBoxManip.h
%include Inventor/manips/SoTransformerManip.h

%include Inventor/misc/SoAuditorList.h
%include Inventor/misc/SoBase.h
%include Inventor/misc/SoBasic.h
%include Inventor/misc/SoByteStream.h
%include Inventor/misc/SoCallbackList.h
%include Inventor/misc/SoChildList.h
%include Inventor/misc/SoNormalGenerator.h
%include Inventor/misc/SoNotification.h
%include Inventor/misc/SoTranReceiver.h
%include Inventor/misc/SoState.h
%include Inventor/misc/SoTranscribe.h
%include Inventor/misc/SoTranSender.h
%include Inventor/misc/SoLightPath.h
%include Inventor/misc/SoTempPath.h

%include Inventor/lists/SbList.h
%include Inventor/lists/SbPList.h
%include Inventor/lists/SbIntList.h
%include Inventor/lists/SbVec3fList.h
%include Inventor/lists/SbStringList.h
%include Inventor/lists/SoActionMethodList.h
%include Inventor/lists/SoAuditorList.h
%include Inventor/lists/SoBaseList.h
%include Inventor/lists/SoCallbackList.h
%include Inventor/lists/SoDetailList.h
%include Inventor/lists/SoEnabledElementsList.h
%include Inventor/lists/SoEngineList.h
%include Inventor/lists/SoEngineOutputList.h
%include Inventor/lists/SoFieldList.h
%include Inventor/lists/SoNodeList.h
%include Inventor/lists/SoPathList.h
%include Inventor/lists/SoPickedPointList.h
%include Inventor/lists/SoTypeList.h
%include Inventor/lists/SoVRMLInterpOutputList.h

%include Inventor/nodekits/SoSubKit.h
%include Inventor/nodekits/SoNodeKit.h
%include Inventor/nodekits/SoNodeKitListPart.h
%include Inventor/nodekits/SoNodekitCatalog.h
%include Inventor/nodekits/SoBaseKit.h
%include Inventor/nodekits/SoAppearanceKit.h
%include Inventor/nodekits/SoCameraKit.h
%include Inventor/nodekits/SoInteractionKit.h
%include Inventor/nodekits/SoLightKit.h
%include Inventor/nodekits/SoSceneKit.h
%include Inventor/nodekits/SoSeparatorKit.h
%include Inventor/nodekits/SoShapeKit.h
%include Inventor/nodekits/SoWrapperKit.h

%include Inventor/nodes/SoSubNode.h
%include Inventor/nodes/SoNodes.h
%include Inventor/nodes/SoAnnotation.h
%include Inventor/nodes/SoAntiSquish.h
%include Inventor/nodes/SoArray.h
%include Inventor/nodes/SoAsciiText.h
%include Inventor/nodes/SoBaseColor.h
%include Inventor/nodes/SoBlinker.h
%include Inventor/nodes/SoCallback.h
%include Inventor/nodes/SoCamera.h
%include Inventor/nodes/SoClipPlane.h
%include Inventor/nodes/SoColorIndex.h
%include Inventor/nodes/SoComplexity.h
%include Inventor/nodes/SoCone.h
%include Inventor/nodes/SoCoordinate3.h
%include Inventor/nodes/SoCoordinate4.h
%include Inventor/nodes/SoCube.h
%include Inventor/nodes/SoCylinder.h
%include Inventor/nodes/SoDirectionalLight.h
%include Inventor/nodes/SoDrawStyle.h
%include Inventor/nodes/SoEnvironment.h
%include Inventor/nodes/SoEventCallback.h
%include Inventor/nodes/SoExtSelection.h
%include Inventor/nodes/SoFaceSet.h
%include Inventor/nodes/SoFile.h
%include Inventor/nodes/SoFont.h
%include Inventor/nodes/SoFontStyle.h
%include Inventor/nodes/SoGroup.h
%include Inventor/nodes/SoImage.h
%include Inventor/nodes/SoIndexedFaceSet.h
%include Inventor/nodes/SoIndexedLineSet.h
%include Inventor/nodes/SoIndexedNurbsCurve.h
%include Inventor/nodes/SoIndexedNurbsSurface.h
%include Inventor/nodes/SoIndexedShape.h
%include Inventor/nodes/SoIndexedTriangleStripSet.h
%include Inventor/nodes/SoInfo.h
%include Inventor/nodes/SoLOD.h
%include Inventor/nodes/SoLabel.h
%include Inventor/nodes/SoLevelOfDetail.h
%include Inventor/nodes/SoLight.h
%include Inventor/nodes/SoLightModel.h
%include Inventor/nodes/SoLineSet.h
%include Inventor/nodes/SoLinearProfile.h
%include Inventor/nodes/SoLocateHighlight.h
%include Inventor/nodes/SoMarkerSet.h
%include Inventor/nodes/SoMaterial.h
%include Inventor/nodes/SoMaterialBinding.h
%include Inventor/nodes/SoMatrixTransform.h
%include Inventor/nodes/SoMultipleCopy.h
%include Inventor/nodes/SoNode.h
%include Inventor/nodes/SoNonIndexedShape.h
%include Inventor/nodes/SoNormal.h
%include Inventor/nodes/SoNormalBinding.h
%include Inventor/nodes/SoNurbsCurve.h
%include Inventor/nodes/SoNurbsProfile.h
%include Inventor/nodes/SoNurbsSurface.h
%include Inventor/nodes/SoOrthographicCamera.h
%include Inventor/nodes/SoPackedColor.h
%include Inventor/nodes/SoPathSwitch.h
%include Inventor/nodes/SoPendulum.h
%include Inventor/nodes/SoPerspectiveCamera.h
%include Inventor/nodes/SoPickStyle.h
%include Inventor/nodes/SoPointLight.h
%include Inventor/nodes/SoPointSet.h
%include Inventor/nodes/SoPolygonOffset.h
%include Inventor/nodes/SoProfile.h
%include Inventor/nodes/SoProfileCoordinate2.h
%include Inventor/nodes/SoProfileCoordinate3.h
%include Inventor/nodes/SoQuadMesh.h
%include Inventor/nodes/SoResetTransform.h
%include Inventor/nodes/SoRotation.h
%include Inventor/nodes/SoRotationXYZ.h
%include Inventor/nodes/SoRotor.h
%include Inventor/nodes/SoScale.h
%include Inventor/nodes/SoSelection.h
%include Inventor/nodes/SoSeparator.h
%include Inventor/nodes/SoShape.h
%include Inventor/nodes/SoShapeHints.h
%include Inventor/nodes/SoShuttle.h
%include Inventor/nodes/SoSphere.h
%include Inventor/nodes/SoSpotLight.h
%include Inventor/nodes/SoSurroundScale.h
%include Inventor/nodes/SoSwitch.h
%include Inventor/nodes/SoText2.h
%include Inventor/nodes/SoText3.h
%include Inventor/nodes/SoTexture2.h
%include Inventor/nodes/SoTexture2Transform.h
%include Inventor/nodes/SoTextureCoordinate2.h
%include Inventor/nodes/SoTextureCoordinateBinding.h
%include Inventor/nodes/SoTextureCoordinateDefault.h
%include Inventor/nodes/SoTextureCoordinateEnvironment.h
%include Inventor/nodes/SoTextureCoordinateFunction.h
%include Inventor/nodes/SoTextureCoordinatePlane.h
%include Inventor/nodes/SoTransform.h
%include Inventor/nodes/SoTransformSeparator.h
%include Inventor/nodes/SoTransformation.h
%include Inventor/nodes/SoTranslation.h
%include Inventor/nodes/SoTriangleStripSet.h
%include Inventor/nodes/SoUnits.h
%include Inventor/nodes/SoVertexProperty.h
%include Inventor/nodes/SoVertexShape.h
%include Inventor/nodes/SoWWWAnchor.h
%include Inventor/nodes/SoWWWInline.h

/* %include Inventor/projectors/SbProjectors.h */
/* %include Inventor/projectors/SbCylinderPlaneProjector.h */
/* %include Inventor/projectors/SbCylinderProjector.h */
/* %include Inventor/projectors/SbCylinderSectionProjector.h */
/* %include Inventor/projectors/SbCylinderSheetProjector.h */
/* %include Inventor/projectors/SbLineProjector.h */
/* %include Inventor/projectors/SbPlaneProjector.h */
/* %include Inventor/projectors/SbProjector.h */
/* %include Inventor/projectors/SbSpherePlaneProjector.h */
/* %include Inventor/projectors/SbSphereProjector.h */
/* %include Inventor/projectors/SbSphereSectionProjector.h */
/* %include Inventor/projectors/SbSphereSheetProjector.h */

%include Inventor/sensors/SoSensors.h
%include Inventor/sensors/SoAlarmSensor.h
%include Inventor/sensors/SoDataSensor.h
%include Inventor/sensors/SoDelayQueueSensor.h
%include Inventor/sensors/SoFieldSensor.h
%include Inventor/sensors/SoIdleSensor.h
%include Inventor/sensors/SoNodeSensor.h
%include Inventor/sensors/SoOneShotSensor.h
%include Inventor/sensors/SoPathSensor.h
%include Inventor/sensors/SoSensor.h
%include Inventor/sensors/SoSensorManager.h
%include Inventor/sensors/SoTimerQueueSensor.h
%include Inventor/sensors/SoTimerSensor.h

%include Inventor/Qt/devices/SoQtDevice.h
%include Inventor/Qt/devices/SoQtKeyboard.h
%include Inventor/Qt/devices/SoQtMouse.h
%include Inventor/Qt/devices/SoQtSpaceball.h
%include Inventor/Qt/SoQtBasic.h
%include Inventor/Qt/SoQtComponent.h
%include Inventor/Qt/SoQtCursor.h
%include Inventor/Qt/SoQtGLWidget.h
%include Inventor/Qt/SoQt.h
%include Inventor/Qt/SoQtObject.h
%include Inventor/Qt/SoQtRenderArea.h
%include Inventor/Qt/viewers/SoQtViewer.h
%include Inventor/Qt/viewers/SoQtConstrainedViewer.h
%include Inventor/Qt/viewers/SoQtFullViewer.h
%include Inventor/Qt/viewers/SoQtExaminerViewer.h
%include Inventor/Qt/viewers/SoQtFlyViewer.h
%include Inventor/Qt/viewers/SoQtPlaneViewer.h
%include Inventor/Qt/widgets/SoQtPopupMenu.h

/* %include Inventor/Gtk/SoGtkBasic.h */
/* %include Inventor/Gtk/SoGtk.h */
/* %include Inventor/Gtk/SoGtkObject.h */
/* %include Inventor/Gtk/SoGtkCursor.h */
/* %include Inventor/Gtk/SoGtkComponent.h */
/* %include Inventor/Gtk/SoGtkRoster.h */
/* %include Inventor/Gtk/SoGtkGraphEditor.h */
/* %include Inventor/Gtk/SoGtkGLWidget.h */
/* %include Inventor/Gtk/SoGtkRenderArea.h */
/* %include Inventor/Gtk/SoGtkRoster.h */
/* %include Inventor/Gtk/SoGtkGraphEditor.h */
/* %include Inventor/Gtk/devices/SoGtkDevice.h */
/* %include Inventor/Gtk/devices/SoGtkInputFocus.h */
/* %include Inventor/Gtk/devices/SoGtkKeyboard.h */
/* %include Inventor/Gtk/devices/SoGtkMouse.h */
/* %include Inventor/Gtk/devices/SoGtkSpaceball.h */
/* %include Inventor/Gtk/widgets/SoGtkPopupMenu.h */
/* %include Inventor/Gtk/viewers/SoGtkViewer.h */
/* %include Inventor/Gtk/viewers/SoGtkFullViewer.h */
/* %include Inventor/Gtk/viewers/SoGtkConstrainedViewer.h */
/* %include Inventor/Gtk/viewers/SoGtkExaminerViewer.h */
/* %include Inventor/Gtk/viewers/SoGtkPlaneViewer.h */
/* %include Inventor/Gtk/viewers/SoGtkFlyViewer.h */
