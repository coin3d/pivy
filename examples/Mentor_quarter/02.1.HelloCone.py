#!/usr/bin/env python

###
# Copyright (c) 2002-2007 Systems in Motion
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

###
# This is an example from the Inventor Mentor,
# chapter 2, example 1.
#
# Hello Cone example program; draws a red cone in a window.
#

import sys

from PySide import QtGui
from pivy import quarter, coin


def main():
    # Initialize Inventor. This returns a main window to use.
    # If unsuccessful, exit.

    app = QtGui.QApplication(sys.argv)
    viewer = quarter.QuarterWidget()

    if viewer is None:
        sys.exit(1)

    # Make a scene containing a red cone
    root = coin.SoSeparator()
    myCamera = coin.SoPerspectiveCamera()
    myMaterial = coin.SoMaterial()
    myMaterial.diffuseColor = (1.0, 0.0, 0.0)   # Red

    # add everything to the root (possible with 0.6)
    root += myCamera, coin.SoDirectionalLight(), myMaterial, coin.SoCone()

    # Make myCamera see everything.
    myCamera.viewAll(root, viewer.getSoRenderManager().getViewportRegion())

    # set scenegraph of viewer to our scene, change the title
    viewer.sceneGraph = root
    viewer.setWindowTitle("Hello Cone")

    # show the widget
    viewer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
