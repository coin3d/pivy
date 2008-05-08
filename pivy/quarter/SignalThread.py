from PyQt4.QtCore import QThread
from PyQt4.QtCore import QWaitCondition
from PyQt4.QtCore import QMutex
from PyQt4.QtCore import SIGNAL


class SignalThread(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)

        self.waitcond = QWaitCondition()
        self.mutex = QMutex()
        self.isstopped = False

    def trigger(self):
        """lock first to make sure the QThread is actually waiting for a signal"""
        self.mutex.lock()
        self.waitcond.wakeOne()
        self.mutex.unlock()

    def stopThread(self):
        self.mutex.lock()
        self.isstopped = True
        self.waitcond.wakeOne()
        self.mutex.unlock()

    def run(self):
        self.mutex.lock()
        while not self.isstopped:
            # just wait, and trigger every time we receive a signal
            self.waitcond.wait(self.mutex)
            if not self.isstopped:
                self.emit(SIGNAL("triggerSignal()"))
        self.mutex.unlock()
