import sys

from pivy.coin import SoSeparator
from pivy.coin import SoBaseColor
from pivy.coin import SbColor
from pivy.coin import SoCone

from pivy.quarter import QuarterApplication
from pivy.quarter import QuarterWidget


def main():

    app = QuarterApplication(sys.argv)

    root = SoSeparator()
    root.ref()
    col = SoBaseColor()
    col.rgb = SbColor(1, 1, 0)
    root.addChild(col)
    root.addChild(SoCone())

    viewer = QuarterWidget()
    viewer.setSceneGraph(root)

    viewer.show()
    result = app.exec_()
    return result

main()
