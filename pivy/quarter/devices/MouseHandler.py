from PyQt4.QtCore import QEvent
from PyQt4.QtCore import QSize
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMouseEvent
from PyQt4.QtGui import QWheelEvent
from PyQt4.QtGui import QResizeEvent


from pivy.coin import SoLocation2Event
from pivy.coin import SbVec2s
from pivy.coin import SoButtonEvent
from pivy.coin import SoMouseButtonEvent

from DeviceHandler import DeviceHandler


class MouseHandler(DeviceHandler):
    def __init__(self):
        """The MouseHandler class provides translation of mouse events
        on the QuarterWidget. It is registered with the DeviceManager by
        default."""

        self.location2 = SoLocation2Event()
        self.mousebutton = SoMouseButtonEvent()
        self.windowsize = SbVec2s(-1, -1)

    def translateEvent(self, qevent):
        """Translates from QMouseEvents to SoLocation2Events and SoMouseButtonEvents"""

        if qevent.type() == QEvent.MouseMove:
            return self.mouseMoveEvent(qevent)

        if qevent.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonRelease):
            return self.mouseButtonEvent(qevent)

        if qevent.type() == QEvent.Wheel:
            return self.mouseWheelEvent(qevent)

        if qevent.type() == QEvent.Resize:
            self.resizeEvent(qevent)

        return None


    def resizeEvent(self, qevent):
        self.windowsize = SbVec2s(qevent.size().width(),
                                  qevent.size().height())

    def mouseMoveEvent(self, qevent):
        self.setModifiers(self.location2, qevent)

        assert(self.windowsize[1] != -1)
        pos = SbVec2s(qevent.pos().x(), self.windowsize[1] - qevent.pos().y() - 1)
        self.location2.setPosition(pos)
        return self.location2

    def mouseWheelEvent(self, qevent):
        assert(False and "not implemented")
        self.setModifiers(self.mousebutton, qevent)

        self.mousebutton.setPosition(self.location2.getPosition())

        # FIXME jkg:
  # QWheelEvent::delta() returns the distance that the wheel is
  # rotated, in eights of a degree. A positive value indicates that
  # the wheel was rotated forwards away from the user; a negative
  # value indicates that the wheel was rotated backwards toward the
  # user.
#      (qevent.delta() > 0) ?
#        self.mousebutton->setButton(SoMouseButtonEvent::BUTTON4) :
#        self.mousebutton->setButton(SoMouseButtonEvent::BUTTON5);
#
#      self.mousebutton->setState(SoButtonEvent::DOWN);
#      return self.mousebutton;


    def mouseButtonEvent(self, qevent):
        self.setModifiers(self.mousebutton, qevent)
        self.mousebutton.setPosition(self.location2.getPosition())

        if qevent.type() == QEvent.MouseButtonPress:
            self.mousebutton.setState(SoButtonEvent.DOWN)
        else:
            self.mousebutton.setState(SoButtonEvent.UP)

        if qevent.button() == Qt.LeftButton:
            self.mousebutton.setButton(SoMouseButtonEvent.BUTTON1)
        elif qevent.button() == Qt.RightButton:
            self.mousebutton.setButton(SoMouseButtonEvent.BUTTON2)
        elif qevent.button() == Qt.MidButton:
            # REMOVE when ready: hack to quit
            raise SystemExit
            self.mousebutton.setButton(SoMouseButtonEvent.BUTTON3)
        else:
            # FIXME jkg: default case
            self.mousebutton.setButton(SoMouseButtonEvent.ANY)
            SoDebugError.postInfo("MouseHandler.mouseButtonEvent",
                                  "Unhandled ButtonState = %x", event.button())
        return self.mousebutton
