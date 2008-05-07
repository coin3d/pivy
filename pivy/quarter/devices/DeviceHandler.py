from pivy.coin import SbTime


class DeviceHandler:
    """
    The DeviceHandler class is the base class for eventhandlers
  such as the KeyboardHandler and MouseHandler. It can be subclassed
  to create event handlers for other devices.
"""
    def __init__(self):
        pass

    def setManager(self, manager):
        self.manager = manager

    def setModifiers(self, soevent, qevent):
        # FIXME: How do we get the time from the qevent? (20070306 frodo)
        soevent.setTime(SbTime.getTimeOfDay())

        # Note: On Mac OS X, the ControlModifier value corresponds to the
        # Command keys on the Macintosh keyboard, and the MetaModifier
        # value corresponds to the Control keys.
        #print "FIXME jkg: setmodifiers"
#        print soevent
#        soevent.setShiftDown(qevent.modifiers() and Qt.ShiftModifier)
#        soevent.setAltDown(qevent.modifiers() and Qt.AltModifier)
#        soevent.setCtrlDown(qevent.modifiers() and Qt.ControlModifier)
