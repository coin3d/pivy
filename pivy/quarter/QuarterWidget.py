from PyQt4.QtOpenGL import QGLWidget
from PyQt4.QtOpenGL import QGLFormat
from PyQt4.QtOpenGL import QGL
from PyQt4.QtCore import Qt

from pivy.coin import SoRenderManager
from pivy.coin import SoEventManager
#from pivy.coin import SoSceneManager
from pivy.coin import SoSearchAction
from pivy.coin import SoCamera
from pivy.coin import SoPerspectiveCamera
from pivy.coin import SoTransform
from pivy.coin import ScXML
from pivy.coin import SoScXMLStateMachine
from pivy.coin import cast
from pivy.coin import SoGLCacheContextElement

from pivy.coin import SoDirectionalLight
from pivy.coin import SoSeparator
from pivy.coin import SbColor4f
from pivy.coin import SbName
from pivy.coin import SbViewportRegion

from devices import DeviceManager
from devices import MouseHandler

from eventhandlers import EventManager


# FIXME jkg: change to private/static method?
def renderCB(closure, manager):
    print "rendercb"
    assert(closure)
    thisp = closure
    thisp.makeCurrent()
    thisp.actualRedraw()
    if (thisp.doubleBuffer()):
        thisp.swapBuffers()
    thisp.doneCurrent()

class QuarterWidget(QGLWidget):
    def __init__(self, parent = None, sharewidget = None):
        QGLWidget.__init__(self, parent)

        # from QuarterWidgetP
        self.cachecontext_list = []
        self.cachecontext = self.findCacheContext(self, sharewidget)
        #self.statecursormap = StateCursorMap()

        self.scene = None
        self.contextmenu = None
        self.contextmenuenabled = True

        self.sorendermanager = SoRenderManager()
        self.soeventmanager = SoEventManager()

        #Mind the order of initialization as the XML state machine uses
        #callbacks which depends on other state being initialized
        self.eventmanager = EventManager(self)
        self.devicemanager = DeviceManager(self)

        statechangecb = staticmethod(self.statechangecb)

        statemachine = ScXML.readFile("coin:scxml/navigation/examiner.xml")
        if (statemachine and statemachine.isOfType(SoScXMLStateMachine.getClassTypeId())):
            sostatemachine = cast(statemachine, "SoScXMLStateMachine")
            print sostatemachine
            statemachine.addStateChangeCallback(statechangecb, self)
            self.soeventmanager.setNavigationSystem(None)
            self.soeventmanager.addSoScXMLStateMachine(sostatemachine)
            sostatemachine.initialize()
            print "ok"

        self.headlight = SoDirectionalLight()
        self.headlight.ref()

        raise SystemExit

        #self.sorendermanager.setAutoClipping(SoRenderManager.VARIABLE_NEAR_PLANE)
        self.sorendermanager.setRenderCallback(renderCB, self)
        # FIXME jkg: set alpha 0
        self.sorendermanager.setBackgroundColor(SbColor4f(0, 0, 0, 0))
        self.sorendermanager.activate()
        #self.sorendermanager.addPreRenderCallback(prerendercb, self)
        #self.sorendermanager.addPostRenderCallback(postrendercb, self)

        #self.soeventmanager.setNavigationState(SoEventManager.MIXED_NAVIGATION)

        self.devicemanager.registerDevice(MouseHandler())
#        self.devicemanager.registerDevice(KeyboardHandler())
#        self.eventmanager.registerEventHandler(DragDropHandler())

        # set up a cache context for the default SoGLRenderAction
        self.sorendermanager.getGLRenderAction().setCacheContext(self.getCacheContextId())

        self.setStateCursor("interact", Qt.ArrowCursor)
        self.setStateCursor("idle", Qt.OpenHandCursor)
        self.setStateCursor("rotate", Qt.ClosedHandCursor)
        self.setStateCursor("pan", Qt.SizeAllCursor)
        self.setStateCursor("zoom", Qt.SizeVerCursor)
        self.setStateCursor("seek", Qt.CrossCursor)
        self.setStateCursor("spin", Qt.OpenHandCursor)

        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus);


    def setSceneGraph(self, node):
        if node and self.scene==node:
            return

        camera = None
        superscene = None
        viewall = False

        if node:
            node.ref()
            self.scene = node
            self.scene.ref()

            superscene = SoSeparator()
            superscene.addChild(self.headlight)

            camera = self.searchForCamera(node)
            if not camera:
                camera = SoPerspectiveCamera()
                superscene.addChild(camera)
                viewall = True
                # FIXME jkg: remove when viewAll is in place
                xf = SoTransform()
                xf.set("translation 0 0 -4")
                superscene.addChild(xf)

            superscene.addChild(node)
            node.unref()

        self.soeventmanager.setSceneGraph(superscene)
        self.sorendermanager.setSceneGraph(superscene)
        self.soeventmanager.setCamera(camera)
        self.sorendermanager.setCamera(camera)

        if viewall:
            self.viewAll()

        if superscene:
            superscene.touch()

    def viewAll(self):
        print "FIXME jkg: missing nav viewall stuff"

    def initializeGL(self):
        # NOTE 20080507 jkg: got unexplainable hang here yesterday. but not today
        self.setFormat(QGLFormat(QGL.DepthBuffer))

    def resizeGL(self, width, height):
        vp = SbViewportRegion(width, height)
        self.sorendermanager.setViewportRegion(vp)
        self.soeventmanager.setViewportRegion(vp)

    def paintGL(self):
        self.actualRedraw()

    def actualRedraw(self):
        self.sorendermanager.render(True, True)

    def event(self, event):
        """Translates Qt Events into Coin events and passes them on to the
          scenemanager for processing. If the event can not be translated or
          processed, it is forwarded to Qt and the method returns false. This
          method could be overridden in a subclass in order to catch events of
          particular interest to the application programmer."""
        if self.eventmanager.handleEvent(event):
            return

        print "event not handled", event

        raise Exception("hm")
        soevent = self.devicemanager.translateEvent(event)
        if (soevent and self.soeventmanager.processEvent(soevent)):
            return True

        QGLWidget.event(self, event)

    def setStateCursor(self, state, cursor):
        """  You can set the cursor you want to use for a given navigation
          state. See the Coin documentation on navigation for information
          about available states"""
        # will overwrite the value of an existing item
        #self.statecursormap->insert(state, cursor);
        pass


    # QuarterWidgetP

    def searchForCamera(self, root):
        sa = SoSearchAction()
        sa.setInterest(SoSearchAction.FIRST)
        sa.setType(SoCamera.getClassTypeId())
        sa.apply(root)


#include "QuarterWidgetP.h"
#include <Quarter/QuarterWidget.h>
#include <Quarter/devices/DeviceManager.h>

#include <QtGui/QCursor>
#include <QtCore/QMap>

#include <Inventor/nodes/SoCamera.h>
#include <Inventor/nodes/SoNode.h>
#include <Inventor/actions/SoSearchAction.h>
#include <Inventor/elements/SoGLCacheContextElement.h>
#include <Inventor/lists/SbList.h>
#include <Inventor/SoEventManager.h>
#include <Inventor/scxml/SoScXMLStateMachine.h>

#include "ContextMenu.h"



    def getCacheContextId(self):
        return self.cachecontext.id

    def findCacheContext(self, widget, sharewidget):

        class QuarterWidgetP_cachecontext:
            def __init__(self):
                self.widgetlist = []
                self.id = None

        for cachecontext in self.cachecontext_list:
            for widget in cachecontext.widgetlist:
                if (widget == sharewidget):
                    cachecontext.widgetlist.append(widget)
                    return cachecontext;
        cachecontext = QuarterWidgetP_cachecontext()
        cachecontext.id = SoGLCacheContextElement.getUniqueCacheContext()
        cachecontext.widgetlist.append(widget)
        self.cachecontext_list.append(cachecontext)

        return cachecontext

    def prerendercb(userdata, manager):
        #thisp = static_cast<QuarterWidgetP *>(userdata);
        thisp = userdata
        evman = thisp.soeventmanager
        assert(evman)

        for c in range(evman.getNumSoScXMLStateMachines()):
            statemachine = evman.getSoScXMLStateMachine(c)
            statemachine.preGLRender()

    def postrendercb(userdata, manager):
        #QuarterWidgetP * thisp = static_cast<QuarterWidgetP *>(userdata);
        evman = thisp.soeventmanager
        assert(evman)
        for c in range(evman.getNumSoScXMLStateMachines()):
            statemachine = evman.getSoScXMLStateMachine(c)
            statemachine.postGLRender()

    def statechangecb(userdata, statemachine, stateid, enter, foo):
        contextmenurequest = SbName("contextmenurequest")
        #QuarterWidgetP * thisp = static_cast<QuarterWidgetP *>(userdata);
        assert(thisp and thisp.master)
        if (enter):
            state = SbName(stateid)
        if (thisp.contextmenuenabled and state == contextmenurequest):
            if (not thisp.contextmenu):
                self.contextmenu = ContextMenu(self)
            self.contextmenu.exec_(self.devicemanager.getLastGlobalPosition())
#        if (statecursormap.contains(state)):
#            cursor = statecursormap.value(state)
#            self.setCursor(cursor)
