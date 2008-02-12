#!/usr/bin/env python

import sys
from pivy.gui.soqt import SoQt
from PyQt4.QtGui import QApplication
from mainwindow import MainWindow

if __name__ == "__main__":

    SoQt.init(None)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
