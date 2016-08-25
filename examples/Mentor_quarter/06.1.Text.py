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
# chapter 6, example 1.
#
# This example renders a globe and uses 2D text to label the
# continents Africa and Asia.
#

import sys
import os

from PySide import QtGui
from pivy import coin, quarter


def main():
    # Initialize Inventor and Qt
    app = QtGui.QApplication([])
    viewer = quarter.QuarterWidget()

    root = coin.SoGroup()

    # Choose a font
    myFont = coin.SoFont()
    myFont.name = "Times-Roman"
    myFont.size = 24.0
    root += myFont

    # Add the globe, a sphere with a texture map.
    # Put it within a separator.
    sphereSep = coin.SoSeparator()
    myTexture2 = coin.SoTexture2()
    sphereComplexity = coin.SoComplexity()
    sphereComplexity.value = 0.55
    root += sphereSep
    sphereSep += myTexture2, sphereComplexity, coin.SoSphere()
    myTexture2.filename = os.path.join(os.path.dirname(__file__), "globe.rgb")


    # Add Text2 for AFRICA, translated to proper location.
    africaSep = coin.SoSeparator()
    africaTranslate = coin.SoTranslation()
    africaText = coin.SoText2()
    africaTranslate.translation = (.25, .0, 1.25)
    africaText.string = "AFRICA"
    root += africaSep
    africaSep += africaTranslate, africaText

    # Add Text2 for ASIA, translated to proper location.
    asiaSep = coin.SoSeparator()
    asiaTranslate = coin.SoTranslation()
    asiaText = coin.SoText2()
    asiaTranslate.translation = (.8, .8, 0)
    asiaText.string = "ASIA"
    root += asiaSep
    root += asiaTranslate, asiaText

    viewer.sceneGraph = root
    viewer.setWindowTitle("2D Text")

    # In Inventor 2.1, if the machine does not have hardware texture
    # mapping, we must override the default drawStyle to display textures.
    # viewer.setDrawStyle(coin.SoGuiViewer.STILL, coin.SoGuiViewer.VIEW_AS_IS)

    viewer.show()
    viewer.viewAll()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
