import sys
from PySide import QtGui
from pivy import quarter, coin
from OpenGL.GL import *


class CapPlane():
    def __init__(self, plane, node):
        self.plane = plane  # SbPlane
        self.node = node
        self.normal = plane.getNormal()
        self.dist = plane.getDistanceFromOrigin()

    def stencilBuffer(self):
        eq = GLdouble_4(*self.normal, self.dist)
        glClipPlane(GL_CLIP_PLANE0, eq)

        glEnable(GL_CLIP_PLANE0)

        glEnable(GL_STENCIL_TEST)
        glClear(GL_STENCIL_BUFFER_BIT)
        glDisable(GL_DEPTH_TEST)
        glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)

        glStencilFunc(GL_ALWAYS, 0, 0)
        glStencilOp(GL_KEEP, GL_KEEP, GL_INCR)
        glCullFace(GL_FRONT)
        self.draw_box()

        glStencilOp(GL_KEEP, GL_KEEP, GL_DECR)
        glCullFace(GL_BACK)
        self.draw_box()

        glEnable(GL_STENCIL_TEST)
        glClear(GL_STENCIL_BUFFER_BIT)
        glDisable(GL_DEPTH_TEST)
        glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)

        glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_CLIP_PLANE0)
        glStencilFunc(GL_NOTEQUAL, 0, ~0)

        glColor3f(0.0, 0.2, 1)
        glBegin(GL_QUADS)
        glVertex3fv([-1.1,-1.1, 1.1])
        glVertex3fv([ 1.1,-1.1, 1.1])
        glVertex3fv([ 1.1, 1.1, -1.1])
        glVertex3fv([-1.1, 1.1, -1.1])
        glEnd()

        glDisable(GL_STENCIL_TEST)
        glEnable(GL_CLIP_PLANE0)
        self.draw_box()
        glDisable(GL_CLIP_PLANE0)

    def draw_box(self):
        glDisable(GL_LIGHTING)
        glPushMatrix()
        glColor3f(0.0, 0.7, 0.0)
        glBegin(GL_QUADS)
        glVertex3fv([-1,-1, -1])
        glVertex3fv([-1, 1, -1])
        glVertex3fv([ 1, 1, -1])
        glVertex3fv([ 1,-1, -1])

        glVertex3fv([-1,-1, 1])
        glVertex3fv([-1, 1, 1])
        glVertex3fv([ 1, 1, 1])
        glVertex3fv([ 1,-1, 1])

        glVertex3fv([1, -1,-1])
        glVertex3fv([1, -1, 1])
        glVertex3fv([1,  1, 1])
        glVertex3fv([1,  1,-1])

        glVertex3fv([-1, -1,-1])
        glVertex3fv([-1, -1, 1])
        glVertex3fv([-1,  1, 1])
        glVertex3fv([-1,  1,-1])

        glVertex3fv([-1, 1, -1])
        glVertex3fv([-1, 1,  1])
        glVertex3fv([ 1, 1,  1])
        glVertex3fv([ 1, 1, -1])

        glVertex3fv([-1, -1, -1])
        glVertex3fv([-1, -1,  1])
        glVertex3fv([ 1, -1,  1])
        glVertex3fv([ 1, -1, -1])
        glEnd()
        glPopMatrix()
        glEnable(GL_LIGHTING)

# Callback routine to render the floor using OpenGL
def myCallbackRoutine(cap, action):
    global handled
    # only render the floor during GLRender actions:
    if not action.isOfType(coin.SoGLRenderAction.getClassTypeId()):
        return
    cap.stencilBuffer()

def main():
    app = QtGui.QApplication(sys.argv)
    viewer = quarter.QuarterWidget()

    # build a scene (sphere, cube)
    plane = coin.SbPlane(coin.SbVec3f(0, 1, 1), coin.SbVec3f(0, 0, 0))
    root = coin.SoSeparator()
    myCallback = coin.SoCallback()
    cap = CapPlane(plane, root)
    myCallback.setCallback(myCallbackRoutine, cap)
    root += myCallback, coin.SoSphere()

    viewer.setSceneGraph(root)
    viewer.setBackgroundColor(coin.SbColor(.5, .5, .5))
    viewer.setWindowTitle("GL stencil buffer")

    viewer.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
