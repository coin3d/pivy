from PyQt4 import QtCore

from pivy import coin

class DeviceHandler:
    """
    The DeviceHandler class is the base class for eventhandlers
    such as the KeyboardHandler and MouseHandler. It can be subclassed
    to create event handlers for other devices.
    """
    
    def setManager(self, manager):
        self.manager = manager

    def setModifiers(self, soevent, qevent):
        # FIXME: How do we get the time from the qevent? (20070306 frodo)
        soevent.setTime(coin.SbTime.getTimeOfDay())

        # Note: On Mac OS X, the ControlModifier value corresponds to the
        # Command keys on the Macintosh keyboard, and the MetaModifier
        # value corresponds to the Control keys.
        soevent.setShiftDown(int(qevent.modifiers() & QtCore.Qt.ShiftModifier) == QtCore.Qt.ShiftModifier)    
        soevent.setAltDown(int(qevent.modifiers() & QtCore.Qt.AltModifier) == QtCore.Qt.AltModifier)
        soevent.setCtrlDown(int(qevent.modifiers() & QtCore.Qt.ControlModifier) == QtCore.Qt.ControlModifier)
