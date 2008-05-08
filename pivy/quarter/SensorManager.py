from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QObject
from PyQt4.QtCore import QThread
from PyQt4.QtCore import SIGNAL

from pivy.coin import SoDB
from pivy.coin import SbTime
from pivy.coin import SoSceneManager
from pivy.coin import SoRenderManager

from SignalThread import SignalThread


class SensorManager(QObject):
    def __init__(self):

        self.mainthreadid = QThread.currentThreadId()

        self.signalthread = SignalThread()
        QObject.connect(self.signalthread, SIGNAL("triggerSignal()"), self.sensorQueueChanged)

        self.idletimer = QTimer()
        self.delaytimer = QTimer()
        self.timerqueuetimer = QTimer()

        self.idletimer.setSingleShot(True)
        self.delaytimer.setSingleShot(True)
        self.timerqueuetimer.setSingleShot(True)

        self.connect(self.idletimer, SIGNAL("timeout()"), self.idleTimeout)
        self.connect(self.delaytimer, SIGNAL("timeout()"), self.delayTimeout)
        self.connect(self.timerqueuetimer, SIGNAL("timeout()"), self.timerQueueTimeout)

        SoDB.getSensorManager().setChangedCallback(self.sensorQueueChangedCB, self)
        SoDB.setRealTimeInterval(1.0 / 25.0)
        SoRenderManager.enableRealTimeUpdate(False)

    def sensorQueueChangedCB(self, closure):
        thisp = closure
        # if we get a callback from another thread, route the callback
        # through SignalThread so that we receive the callback in the
        # QApplication thread (needed since QTimer isn't thread safe)
        if QThread.currentThreadId() != thisp.mainthreadid:
            if not thisp.signalthread.isRunning():
                thisp.signalthread.start()
            self.signalthread.trigger()
        else:
            print "ok"
            self.sensorQueueChanged()

    def sensorQueueChanged(self):
        sm = SoDB.getSensorManager()
        # Set up timer queue timeout if necessary.

        t = sm.isTimerSensorPending()
        if t:
            # FIXME 20080424 jkg: workaround for PivyExtensions/test/regression.py
            #ie. "interval = t - SbTime.getTimeOfDay()" wont work since t is
            #suddenly mixed up with smallchange... strange link error?
            a = SbTime()
            a.setValue(t.getValue())
            interval = a - SbTime.getTimeOfDay()

            # Qt v2.1.1 (at least) on MSWindows will fail to trigger the
            # timer if the interval is < 0.0.
            #
            # We also want to avoid setting it to 0.0, as that has a special
            # semantic meaning: trigger only when the application is idle and
            # event queue is empty -- which is not what we want to do here.
            #
            # So we clamp it, to a small positive value:
            if interval.getValue() <= 0.0:
                interval.setValue(1.0/5000.0)

            # Change interval of timerqueuetimer when head node of the
            # timer-sensor queue of SoSensorManager changes.
            if not self.timerqueuetimer.isActive():
                self.timerqueuetimer.start(interval.getMsecValue())
            else:
                self.timerqueuetimer.setInterval(interval.getMsecValue())

        # Stop timerqueuetimer if queue is completely empty.
        elif self.timerqueuetimer.isActive():
            self.timerqueuetimer.stop()

        if sm.isDelaySensorPending():
            self.idletimer.start(0)
            # Start idletimer at 0 seconds in the future. -- That means it will
            # trigger when the Qt event queue has been run through, i.e. when
            # the application is idle.
            if not self.idletimer.isActive():
                self.idletimer.start(0)

                t = SoDB.getDelaySensorTimeout()
                if t != SbTime.zero():
                    self.delaytimer.start(interval.getMsecValue())
        else:
            if self.idletimer.isActive():
                self.idletimer.stop()
            if self.delaytimer.isActive():
                self.delaytimer.stop()

    def idleTimeout(self):
        SoDB.getSensorManager().processTimerQueue()
        SoDB.getSensorManager().processDelayQueue(True)

        # The change callback is _not_ called automatically from
        # SoSensorManager after the process methods, so we need to
        # explicitly trigger it ourselves here.
        self.sensorQueueChanged()

    def timerQueueTimeout(self):
        SoDB.getSensorManager().processTimerQueue()

        # The change callback is _not_ called automatically from
        # SoSensorManager after the process methods, so we need to
        # explicitly trigger it ourselves here.
        self.sensorQueueChanged()

    def delayTimeout(self):
        SoDB.getSensorManager().processTimerQueue()
        SoDB.getSensorManager().processDelayQueue(False)

        # The change callback is _not_ called automatically from
        # SoSensorManager after the process methods, so we need to
        # explicitly trigger it ourselves here.
        self.sensorQueueChanged()
