import sys
from PySide.QtGui import QApplication, QColor
from pivy import quarter, coin, highlevel

def main():
    app = QApplication(sys.argv)

    viewer = quarter.QuarterWidget()

    root = highlevel.InteractionSeparator(viewer.sorendermanager)
    marker1 = highlevel.Marker([[0, 0, 0], [0, 1, 0]], dynamic=True)
    marker2 = highlevel.Marker([[1, 0, 0]], dynamic=True)
    root += marker1, marker2
    root.register()

    viewer.setSceneGraph(root)
    viewer.setBackgroundColor(QColor(255, 255, 255))
    viewer.setWindowTitle("minimal")
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
