from PyQt4.QtOpenGL import QGLWidget
from PyQt4.QtOpenGL import QGLFormat
from PyQt4.QtOpenGL import QGL
from PyQt4.QtCore import Qt

from pivy.coin import SoRenderManager
from pivy.coin import SoEventManager
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
from devices import KeyboardHandler

from eventhandlers import EventManager


# FIXME jkg: (1) this is not called and (2) change to private/static method?
def renderCB(closure, rendermanagerdummy):
    thisp = closure
    assert(thisp)
    thisp.makeCurrent()
    thisp.actualRedraw()
    if (thisp.doubleBuffer()):
        thisp.swapBuffers()
    thisp.doneCurrent()

# FIXME jkg: lacking ContextMenu
def statechangecb(userdata, statemachine, stateid, enter, foo):
    contextmenurequest = SbName("contextmenurequest")
    thisp = userdata
    assert(thisp)
    state = SbName()
    if enter:
        state = SbName(stateid)
    if thisp.contextmenuenabled and state == contextmenurequest:
        if not thisp.contextmenu:
            thisp.contextmenu = ContextMenu(self)
        thisp.contextmenu.exec_(self.devicemanager.getLastGlobalPosition())
        if state in statecursormap.keys():
            cursor = thisp.statecursormap[state]
            thisp.setCursor(cursor)

def prerendercb(userdata, manager):
    thisp = userdata
    evman = thisp.soeventmanager
    assert(thisp and evman)
    for c in range(evman.getNumSoScXMLStateMachines()):
        statemachine = evman.getSoScXMLStateMachine(c)
        statemachine.preGLRender()

def postrendercb(userdata, manager):
    thisp = userdata
    evman = thisp.soeventmanager
    assert(evman)
    for c in range(evman.getNumSoScXMLStateMachines()):
        statemachine = evman.getSoScXMLStateMachine(c)
        statemachine.postGLRender()


class QuarterWidget(QGLWidget):
    def __init__(self, parent = None, sharewidget = None):
        QGLWidget.__init__(self, parent)

        # from QuarterWidgetP
        self.cachecontext_list = []
        self.cachecontext = self.findCacheContext(self, sharewidget)
        self.statecursormap = {}

        self.scene = None
        self.contextmenu = None
        self.contextmenuenabled = True

        self.sorendermanager = SoRenderManager()
        self.soeventmanager = SoEventManager()

        #Mind the order of initialization as the XML state machine uses
        #callbacks which depends on other state being initialized
        self.eventmanager = EventManager(self)
        self.devicemanager = DeviceManager(self)

        statemachine = ScXML.readFile("coin:scxml/navigation/examiner.xml")
        if (statemachine and statemachine.isOfType(SoScXMLStateMachine.getClassTypeId())):
            sostatemachine = cast(statemachine, "SoScXMLStateMachine")
            statemachine.addStateChangeCallback(statechangecb, self)
            self.soeventmanager.setNavigationSystem(None)
            self.soeventmanager.addSoScXMLStateMachine(sostatemachine)
            sostatemachine.initialize()

        self.headlight = SoDirectionalLight()
        self.headlight.ref()

        self.sorendermanager.setAutoClipping(SoRenderManager.VARIABLE_NEAR_PLANE)
        self.sorendermanager.setRenderCallback(renderCB, self)
        self.sorendermanager.setBackgroundColor(SbColor4f(0, 0, 0, 0))
        self.sorendermanager.activate()
        self.sorendermanager.addPreRenderCallback(prerendercb, self)
        self.sorendermanager.addPostRenderCallback(postrendercb, self)

        self.soeventmanager.setNavigationState(SoEventManager.MIXED_NAVIGATION)

        self.devicemanager.registerDevice(MouseHandler())
        self.devicemanager.registerDevice(KeyboardHandler())
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
        """ Reposition the current camera to display the entire scene"""
        if self.soeventmanager.getNavigationSystem():
            self.soeventmanager.getNavigationSystem().viewAll()

        viewallevent = SbName("sim.coin3d.coin.navigation.ViewAll")
        for c in range(self.soeventmanager.getNumSoScXMLStateMachines()):
            sostatemachine = self.soeventmanager.getSoScXMLStateMachine(c)
            if (sostatemachine.isActive()):
                sostatemachine.queueEvent(viewallevent)
                sostatemachine.processEventQueue()

    def initializeGL(self):
        # NOTE jkg: DepthBuffer is enabled by default, so I dont see why Quarter (C++) sets it
        pass

    def resizeGL(self, width, height):
        vp = SbViewportRegion(width, height)
        self.sorendermanager.setViewportRegion(vp)
        self.soeventmanager.setViewportRegion(vp)

    def paintGL(self):
        self.actualRedraw()

    def actualRedraw(self):
        self.sorendermanager.render(True, True)

    def event(self, qevent):
        """Translates Qt Events into Coin events and passes them on to the
          scenemanager for processing. If the event can not be translated or
          processed, it is forwarded to Qt and the method returns false. This
          method could be overridden in a subclass in order to catch events of
          particular interest to the application programmer."""

        if self.eventmanager.handleEvent(qevent):
            return True

        soevent = self.devicemanager.translateEvent(qevent)
        if (soevent and self.soeventmanager.processEvent(soevent)):
            return True

        QGLWidget.event(self, qevent)
        return True

    def setStateCursor(self, state, cursor):
        self.statecursormap[state] = cursor

    def searchForCamera(self, root):
        sa = SoSearchAction()
        sa.setInterest(SoSearchAction.FIRST)
        sa.setType(SoCamera.getClassTypeId())
        sa.apply(root)

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
