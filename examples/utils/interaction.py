import sys
from PySide.QtGui import QApplication, QColor
from pivy import quarter, coin, graphics


class ConnectionPolygon(graphics.Polygon):
    std_col = "green"
    def __init__(self, markers, dynamic=False):
        super(ConnectionPolygon, self).__init__(
            sum([m.points for m in markers], []), dynamic=dynamic)
        self.markers = markers

        for m in self.markers:
            m.on_drag.append(self.updatePolygon)

    def updatePolygon(self):
        self.points = sum([m.points for m in self.markers], [])

    @property
    def drag_objects(self):
        return self.markers
        


class ConnectionLine(graphics.Line):
    def __init__(self, markers, dynamic=False):
        super(ConnectionLine, self).__init__(
            sum([m.points for m in markers], []), dynamic=dynamic)
        self.markers = markers
        for m in self.markers:
            m.on_drag.append(self.updateLine)

    def updateLine(self):
        self.points = sum([m.points for m in self.markers], [])

    @property
    def drag_objects(self):
        return self.markers


def main():
    app = QApplication(sys.argv)

    viewer = quarter.QuarterWidget()

    root = graphics.InteractionSeparator(viewer.sorendermanager)

    m1 = graphics.Marker([[-1, -1, -1]], dynamic=True)
    m2 = graphics.Marker([[-1,  1, -1]], dynamic=True)
    m3 = graphics.Marker([[ 1,  1, -1]], dynamic=True)
    m4 = graphics.Marker([[ 1, -1, -1]], dynamic=True)

    m5 = graphics.Marker([[-1, -1,  1]], dynamic=True)
    m6 = graphics.Marker([[-1,  1,  1]], dynamic=True)
    m7 = graphics.Marker([[ 1,  1,  1]], dynamic=True)
    m8 = graphics.Marker([[ 1, -1,  1]], dynamic=True)

    points = [m1, m2, m3, m4, m5, m6, m7, m8]

    l01 = ConnectionLine([m1, m2], dynamic=True)
    l02 = ConnectionLine([m2, m3], dynamic=True)
    l03 = ConnectionLine([m3, m4], dynamic=True)
    l04 = ConnectionLine([m4, m1], dynamic=True)

    l05 = ConnectionLine([m5, m6], dynamic=True)
    l06 = ConnectionLine([m6, m7], dynamic=True)
    l07 = ConnectionLine([m7, m8], dynamic=True)
    l08 = ConnectionLine([m8, m5], dynamic=True)

    l09 = ConnectionLine([m1, m5], dynamic=True)
    l10 = ConnectionLine([m2, m6], dynamic=True)
    l11 = ConnectionLine([m3, m7], dynamic=True)
    l12 = ConnectionLine([m4, m8], dynamic=True)

    lines = [l01, l02, l03, l04, l05, l06, l07, l08, l09, l10, l11, l12]

    p1 = ConnectionPolygon([m1, m2, m3, m4], dynamic=True)
    p2 = ConnectionPolygon([m8, m7, m6, m5], dynamic=True)
    p3 = ConnectionPolygon([m5, m6, m2, m1], dynamic=True)
    p4 = ConnectionPolygon([m6, m7, m3, m2], dynamic=True)
    p5 = ConnectionPolygon([m7, m8, m4, m3], dynamic=True)
    p6 = ConnectionPolygon([m8, m5, m1, m4], dynamic=True)

    polygons = [p1, p2, p3, p4, p5, p6]

    root += points + lines + polygons
    root.register()

    viewer.setSceneGraph(root)
    viewer.setBackgroundColor(QColor(255, 255, 255))
    viewer.setWindowTitle("minimal")
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
