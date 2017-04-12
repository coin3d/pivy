import sys
from PySide.QtGui import QApplication, QColor
from pivy import quarter, coin, highlevel


class test(coin.SoSeparator):
    def __init__(self):
        super(test, self).__init__()
        self.events = coin.SoEventCallback()
        self += self.events
        self.cb = self.events.addEventCallback(
            coin.SoLocation2Event.getClassTypeId(), self.my_cb)
        self.cb1 = self.events.addEventCallback(
            coin.SoEvent.getClassTypeId(), self.my_cb_1)

    def my_cb(self, *args):
        self.events.removeEventCallback(
            coin.SoLocation2Event.getClassTypeId(), self.cb)
    def my_cb_1(self, *args):
        self.events.removeEventCallback(
            coin.SoEvent.getClassTypeId(), self.cb1)        


def main():
    app = QApplication(sys.argv)



    viewer = quarter.QuarterWidget()

    root = coin.SoSeparator()
    root += coin.SoCone()
    root += test()

    viewer.setSceneGraph(root)
    viewer.setBackgroundColor(QColor(255, 255, 255))
    viewer.setWindowTitle("minimal")
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
