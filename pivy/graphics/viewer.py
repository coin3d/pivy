from __future__ import print_function
from pivy import quarter, coin
from PySide2 import QtGui, QtCore
import tempfile

class Viewer(quarter.QuarterWidget):
    def __init__(self, *args, **kwrds):
        try:
            self.app = QtGui.QApplication([])
        except RuntimeError:
            self.app = QtGui.QApplication.instance()

        super(Viewer, self).__init__(*args, **kwrds)
        self.sg = coin.SoSeparator()
        self.sg += [coin.SoOrthographicCamera()]
        self.setSceneGraph(self.sg)
        self.setBackgroundColor(coin.SbColor(1,1,1))
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

    def show(self, exec_widget=True):
        super(Viewer, self).show()
        self.viewAll()
        rec = self.app.desktop().screenGeometry()
        self.move(rec.width() - self.size().width(), 
                  rec.height() - self.size().height())
        if not exec_widget:
            timer = QtCore.QTimer()
            # timer.timeout.connect(self.close)
            timer.singleShot(20, self.close)
        self.app.exec_()
        try:
            from IPython.display import Image
            return Image(self.name)
        except ImportError as e:
            print(e)



    def closeEvent(self, *args):
        image = self.grabFrameBuffer()
        _, name = tempfile.mkstemp(suffix=".png")
        image.save(name, "png")
        self.name = name
