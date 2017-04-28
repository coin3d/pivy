import sys
from pivy import coin
from pivy.gui import soqt

# Initialize Coin (returns main window to use)
# If unsuccessful, exit.
myWindow = soqt.SoQt.init(sys.argv[0])
# Make a scene containing a red cone.
myMaterial = coin.SoMaterial()
myMaterial.diffuseColor = (1.0, 0.0, 0.0)
scene = coin.SoSeparator() 
scene.ref()
scene.addChild(myMaterial)
scene.addChild(coin.SoCone())
# Create a viewer to visualize our scene.
viewer = soqt.SoQtExaminerViewer(myWindow)
# Put our scene into viewer, change the title.
viewer.setSceneGraph(scene)
viewer.setTitle("Examiner Viewer")
viewer.show()
soqt.SoQt.show(myWindow)
soqt.SoQt.mainLoop()