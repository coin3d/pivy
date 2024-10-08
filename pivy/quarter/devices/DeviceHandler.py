###
# Copyright (c) 2002-2008 Kongsberg SIM
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

from pivy.qt import QtCore

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
        soevent.setShiftDown(qevent.modifiers() & QtCore.Qt.ShiftModifier == QtCore.Qt.ShiftModifier)
        soevent.setAltDown(qevent.modifiers() & QtCore.Qt.AltModifier == QtCore.Qt.AltModifier)
        soevent.setCtrlDown(qevent.modifiers() & QtCore.Qt.ControlModifier == QtCore.Qt.ControlModifier)
