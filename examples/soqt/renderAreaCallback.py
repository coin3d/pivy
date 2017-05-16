# this doesn't work currently with Pyside. the wrapInstance methode of shiboken works in a different way and doesn't
# return the best match subclass like sip did. This is actually a bug with shiboken and not with pivy wrappers.
# https://bugreports.qt.io/browse/PYSIDE-31?jql=project%20%3D%20PYSIDE%20AND%20resolution%20%3D%20Unresolved%20ORDER%20BY%20assignee%20ASC%2C%20priority%20DESC

import sys
from pivy import coin
from pivy.gui import soqt
from PySide.QtCore import QEvent

def foo(a, event):
	if event.type() == QEvent.MouseButtonPress:
		print(event)  # event is not a QMouseEvent like it was with pyqt4
		print(event.button())

appWindow = soqt.SoQt.init(sys.argv[0])
root = coin.SoSeparator()
myRenderArea = soqt.SoQtRenderArea(appWindow)
myRenderArea.setSceneGraph(root)
myRenderArea.setTitle("My Event Handler")
myRenderArea.setEventCallback(foo, myRenderArea)

myRenderArea.show()
soqt.SoQt.show(appWindow)
soqt.SoQt.mainLoop()
