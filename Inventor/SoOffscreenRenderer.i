%extend SoOffscreenRenderer {
  PyObject * getBuffer() {
    SbVec2s size = self->getViewportRegion().getWindowSize();

    return PyString_FromStringAndSize((char *)self->getBuffer(),
                                      size[0] * size[1] * self->getComponents());
  }
}
