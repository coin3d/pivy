from PyQt4.QtGui import QImage
from pivy.coin import SbImage


# FIXME jkg: wrapper for SbImage needs to be updated


def readImageCB(filename, image, closure):
    return closure.readImage(filename, image)


class ImageReader():
    def __init__(self):
      SbImage.addReadImageCB(readImageCB, self)

    def __del__(self):
      SbImage.removeReadImageCB(readImageCB, self)

    def readImage(self, filename, sbimage):
        image = QImage()
        if (image.load(filename.getString())):
            # Keep in 8-bits mode if that was what we read
            if (image.depth() == 8 and image.isGrayscale()):
                c = 1
            else:
                # FIXME: consider if we should detect allGrayscale() and alpha (c = 2)
                # FIXME: ternary operator requires 2.5 or higher
                c = 4 if image.hasAlphaChannel() else 3
                image.convertToFormat(QImage.Format_ARGB32 if image.hasAlphaChannel() else QImage.Format_RGB32)

                # TODO: implement
                #sbimage.setValue(SbVec2s(image.width(), image.height()), c, None)

                return True
        return False
