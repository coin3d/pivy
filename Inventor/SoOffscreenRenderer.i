%rename(SoOffscreenRenderer_gl) SoOffscreenRenderer::SoOffscreenRenderer(SoGLRenderAction * action);

%feature("shadow") SoOffscreenRenderer::SoOffscreenRenderer %{
def __init__(self,*args):
   newobj = None
   if isinstance(args[0], SoGLRenderAction):
      newobj = apply(_pivy.new_SoOffscreenRenderer_gl,args)
   else:
      newobj = apply(_pivy.new_SoOffscreenRenderer,args)
   if newobj:
      self.this = newobj.this
      self.thisown = 1
%}

%rename(render_nod) SoOffscreenRenderer::render(SoNode * scene);

%feature("shadow") SoOffscreenRenderer::render(SoPath * scene) %{
def render(*args):
   if isinstance(args[1], SoNode):
      return apply(_pivy.SoOffscreenRenderer_render_nod,args)
   return apply(_pivy.SoOffscreenRenderer_render,args)
%}

%rename(writeToPostScript_fil_vec) SoOffscreenRenderer::writeToPostScript(FILE * fp, const SbVec2f & printsize) const;
%rename(writeToPostScript_chr) SoOffscreenRenderer::writeToPostScript(const char * filename) const;
%rename(writeToPostScript_chr_vec) SoOffscreenRenderer::writeToPostScript(const char * filename, const SbVec2f & printsize) const;

%feature("shadow") SoOffscreenRenderer::writeToPostScript(FILE * fp) const %{
def writeToPostScript(*args):
   if len(args) == 3:
      if isinstance(args[2], SbVec2f):
         return apply(_pivy.SoOffscreenRenderer_writeToPostScript_fil_vec,args)
      else:
         return apply(_pivy.SoOffscreenRenderer_writeToPostScript_chr_vec,args)
   elif type(args[1]) == type(""):
         return apply(_pivy.SoOffscreenRenderer_writeToPostScript_chr,args)
   return apply(_pivy.SoOffscreenRenderer_writeToPostScript,args)
%}

%rename(writeToRGB_chr) SoOffscreenRenderer::writeToRGB(const char * filename) const;

%feature("shadow") SoOffscreenRenderer::writeToRGB(FILE * fp) const %{
def writeToRGB(*args):
   if type(args[1]) == type(""):
         return apply(_pivy.SoOffscreenRenderer_writeToRGB_chr,args)
   return apply(_pivy.SoOffscreenRenderer_writeToRGB,args)
%}

%extend SoOffscreenRenderer {
  PyObject * getBuffer() {
    SbVec2s size = self->getViewportRegion().getWindowSize();

    return PyString_FromStringAndSize((char *)self->getBuffer(),
                                      size[0] * size[1] * self->getComponents());
  }
}
