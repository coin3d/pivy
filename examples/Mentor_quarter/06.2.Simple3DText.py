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
# chapter 6, example 2.
#
# This example renders a globe and uses 3D text to label the
# continents Africa and Asia.
#

import sys

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
    myFont.size = .2
    root += myFont

    # We'll color the front of the text white, and the sides
    # dark grey. coin.So use a materialBinding of PER_PART and
    # two diffuseColor values in the material node.
    myMaterial = coin.SoMaterial()
    myBinding = coin.SoMaterialBinding()
    myMaterial.diffuseColor.set1Value(0, coin.SbColor(1, 1, 1))
    myMaterial.diffuseColor.set1Value(1, coin.SbColor(.1, .1, .1))
    myBinding.value = coin.SoMaterialBinding.PER_PART
    root += myMaterial, myBinding

    # Create the globe
    sphereSep = coin.SoSeparator()
    myTexture2 = coin.SoTexture2()
    sphereComplexity = coin.SoComplexity()
    sphereComplexity.value = 0.55
    root += sphereSep
    sphereSep += myTexture2, sphereComplexity, coin.SoSphere()
    myTexture2.filename = "globe.rgb"

    # Add Text3 for AFRICA, transformed to proper location.
    africaSep = coin.SoSeparator()
    africaTransform = coin.SoTransform()
    africaText = coin.SoText3()
    africaTransform.rotation.setValue(coin.SbVec3f(0, 1, 0), .4)
    africaTransform.translation = (.25, .0, 1.25)
    africaText.parts = coin.SoText3.ALL
    africaText.string = "AFRICA"
    root += africaSep
    africaSep += africaTransform, africaText

    # Add Text3 for ASIA, transformed to proper location.
    asiaSep = coin.SoSeparator()
    asiaTransform = coin.SoTransform()
    asiaText = coin.SoText3()
    asiaTransform.rotation.setValue(coin.SbVec3f(0, 1, 0), 1.5)
    asiaTransform.translation = (.8, .6, .5)
    asiaText.parts = coin.SoText3.ALL
    asiaText.string = "ASIA"
    root += asiaSep
    asiaSep += asiaTransform, asiaText

    viewer.setSceneGraph(root)
    viewer.setWindowTitle("3D Text")

    # In Inventor 2.1, if the machine does not have hardware texture
    # mapping, we must override the default drawStyle to display textures.
    # viewer.setDrawStyle(coin.SoGuiViewer.STILL, coin.SoGuiViewer.VIEW_AS_IS)

    viewer.show()
    viewer.viewAll()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
