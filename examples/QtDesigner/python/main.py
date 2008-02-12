#!/usr/bin/env python

import sys
from pivy.gui.soqt import SoQt
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
from mainwindow import MainWindow

if __name__ == "__main__":

    SoQt.init(None)
    app = QApplication(sys.argv)
    window = MainWindow()
    QObject.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    window.show()
    sys.exit(app.exec_())
