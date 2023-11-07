#!/usr/bin/env python

###
# Copyright (c) 2002-2008 Kongsberg SIM
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

import sys

from pivy.qt.QtWidgets import QApplication

from pivy.coin import SoSeparator
from pivy.coin import SoBaseColor
from pivy.coin import SbColor
from pivy.coin import SoCone

from pivy.quarter import QuarterWidget

def main():
    app = QApplication(sys.argv)

    root = SoSeparator()
    col = SoBaseColor()
    col.rgb = SbColor(1, 1, 0)
    root.addChild(col)
    root.addChild(SoCone())

    viewer = QuarterWidget()
    viewer.setSceneGraph(root)

    viewer.setWindowTitle("minimal")
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
