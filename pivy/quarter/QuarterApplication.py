from PyQt4.QtGui import QApplication

from Quarter import Quarter

class QuarterApplication(QApplication):
    def __init__(self, args):
        QApplication.__init__(self, args)
        self.setApplicationName(args[0])

        self.quarter = Quarter()
