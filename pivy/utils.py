from PySide import QtCore, QtGui
from pivy import coin


def addMarkerFromSvg(file_path, marker_name, pixel_x=10, pixel_y=None,
                     isLSBFirst=False, isUpToDown=False):
    """adds a new marker bitmap from a vector graphic (svg)"""

    # get an icon from the svg rendered with the given pixel
    pixel_y = pixel_y or pixel_x
    icon = QtGui.QIcon(file_path)
    icon = QtGui.QBitmap(icon.pixmap(pixel_x, pixel_y))

    # create a XMP-icon
    buffer=QtCore.QBuffer()
    buffer.open(buffer.WriteOnly)
    icon.save(buffer,"XPM")
    buffer.close()

    # get a string from the XMP-icon
    ary = str(buffer.buffer())
    ary = ary.replace('\n', "").replace('"', "").replace(";", "")
    ary = ary.replace("}", "").replace("#", "x").replace(".", " ")
    string = str.join("", ary.split(",")[3:])
    
    # add the new marker style
    setattr(coin.SoMarkerSet, marker_name, coin.SoMarkerSet.getNumDefinedMarkers())
    coin.SoMarkerSet.addMarker(getattr(coin.SoMarkerSet, marker_name), 
                               coin.SbVec2s([pixel_x, pixel_y]), string,
                               isLSBFirst, isUpToDown)
