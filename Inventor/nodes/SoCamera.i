%rename(pointAt_vec_vec) SoCamera::pointAt(const SbVec3f & targetpoint, const SbVec3f & upvector);

%feature("shadow") SoCamera::pointAt(const SbVec3f & targetpoint) %{
def pointAt(*args):
   if len(args) == 3:
      return apply(_coin.SoCamera_pointAt_vec_vec,args)
   return apply(_coin.SoCamera_pointAt,args)
%}

%rename(viewAll_nod_vpr) SoCamera::viewAll(SoNode * const sceneroot, const SbViewportRegion & vpregion, const float slack = 1.0f);

%feature("shadow") SoCamera::viewAll(SoPath * const path, const SbViewportRegion & vpregion, const float slack = 1.0f) %{
def viewAll(*args):
   if isinstance(args[1], SoNode):
      return apply(_coin.SoCamera_viewAll_nod_vpr,args)
   return apply(_coin.SoCamera_viewAll,args)
%}
