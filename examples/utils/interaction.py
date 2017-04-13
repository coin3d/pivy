import sys
from PySide.QtGui import QApplication, QColor
from pivy import quarter, coin, graphics


class ConnectionPolygon(graphics.Polygon):
    std_col = "green"
    def __init__(self, markers, lines, dynamic=False):
        super(ConnectionPolygon, self).__init__(
            sum([m.points for m in markers], []), dynamic=dynamic)
        self.lines = lines
        self.markers = markers

        for l in self.lines:
            l.on_drag.append(self.updatePolygon)
        for m in self.markers:
            m.on_drag.append(self.updatePolygon)

    def updatePolygon(self):
        self.points = sum([m.points for m in self.markers], [])
        [foo() for foo in self.on_drag]

    @property
    def drag_objects(self):
        return self.lines + self.markers + [self]
        


class ConnectionLine(graphics.Line):
    def __init__(self, markers, dynamic=False):
        super(ConnectionLine, self).__init__(
            sum([m.points for m in markers], []), dynamic=dynamic)
        self.markers = markers
        for m in self.markers:
            m.on_drag.append(self.updateLine)

    def updateLine(self):
        self.points = sum([m.points for m in self.markers], [])
        [foo() for foo in self.on_drag]

    @property
    def drag_objects(self):
        return self.markers + [self]


def main():
    app = QApplication(sys.argv)

    viewer = quarter.QuarterWidget()

    root = graphics.InteractionSeparator(viewer.sorendermanager)

    m1 = graphics.Marker([[0, 0, 0]], dynamic=True)
    m2 = graphics.Marker([[1, 0, 0]], dynamic=True)
    m3 = graphics.Marker([[0, 1, 0]], dynamic=True)
    m4 = graphics.Marker([[0, 0, 2]], dynamic=True)

    l1 = ConnectionLine([m1, m2], dynamic=True)
    l2 = ConnectionLine([m2, m3], dynamic=True)
    l3 = ConnectionLine([m3, m1], dynamic=True)

    l4 = ConnectionLine([m1, m4], dynamic=True)
    l5 = ConnectionLine([m2, m4], dynamic=True)
    l6 = ConnectionLine([m3, m4], dynamic=True)

    p1 = ConnectionPolygon([m3, m2, m1], [], dynamic=True)
    p2 = ConnectionPolygon([m1, m2, m4], [], dynamic=True)
    p3 = ConnectionPolygon([m2, m3, m4], [], dynamic=True)
    p4 = ConnectionPolygon([m3, m1, m4], [], dynamic=True)

    root += [m1, m2, m3, m4, 
             l1, l2, l3, 
             l4, l5, l6,
             p1, p2, p3, p4]
    root.register()

    viewer.setSceneGraph(root)
    viewer.setBackgroundColor(QColor(255, 255, 255))
    viewer.setWindowTitle("minimal")
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
