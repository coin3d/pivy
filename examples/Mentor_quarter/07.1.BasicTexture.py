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
# chapter 7, example 1.
#
# This example displays a textured cube (default
# texture coords).
#

import sys

from PySide import QtGui
from pivy import coin, quarter


def main():
    # Initialize Inventor and Qt
    app = QtGui.QApplication([])
    viewer = quarter.QuarterWidget()

    root = coin.SoSeparator()

    # Choose a texture
    rock = coin.SoTexture2()
    root += rock
    rock.filename = "brick.1.rgb"

    # Make a cube
    root += coin.SoCube()

    viewer.sceneGraph = root
    viewer.setWindowTitle("Default Texture Coords")

    # In Inventor 2.1, if the machine does not have hardware texture
    # mapping, we must override the default drawStyle to display textures.
    # viewer.setDrawStyle(coin.SoGuiViewer.STILL, coin.SoGuiViewer.VIEW_AS_IS)

    viewer.show()
    viewer.viewAll()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
