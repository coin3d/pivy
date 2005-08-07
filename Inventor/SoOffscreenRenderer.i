%rename(SoOffscreenRenderer_gl) SoOffscreenRenderer::SoOffscreenRenderer(SoGLRenderAction * action);

%feature("shadow") SoOffscreenRenderer::SoOffscreenRenderer %{
def __init__(self,*args):
   newobj = None
   if isinstance(args[0], SoGLRenderAction):
      newobj = apply(_coin.new_SoOffscreenRenderer_gl,args)
   else:
      newobj = apply(_coin.new_SoOffscreenRenderer,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
      del newobj.thisown
%}

%ignore SoOffscreenRenderer::getBuffer();

%extend SoOffscreenRenderer {
  PyObject * getBuffer() {
    SbVec2s size = self->getViewportRegion().getWindowSize();

    return PyString_FromStringAndSize((char *)self->getBuffer(),
                                      size[0] * size[1] * self->getComponents());
  }
}
