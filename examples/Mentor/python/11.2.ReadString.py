#!/usr/bin/env python

###
# Copyright (c) 2002, Tamer Fahmy <tamer@tammura.at>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#   * Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

###
# This is an example from the Inventor Mentor,
# chapter 11, example 2.
#
# Example of creatinge a scene graph by reading from a string.
# Create a dodecahedron, made of an IndexedFaceSet.  
#

from sogui import *
from pivy import *
import sys

#############################################################
# CODE FOR The Inventor Mentor STARTS HERE

# Reads a dodecahedron from the following string: 
# (Note: ANSI compilers automatically concatenate 
# adjacent string literals together, so the compiler sees 
# this as one big string)
#
# this note can be happily igonored for python programs! --tamer ;)
# use the elegant triple quote feature of python instead

dodecahedron = """Separator {
   Normal {
      vector [
         0.553341 0 0.832955, 0.832955 0.553341 0,
         0.832955 -0.553341 0, 0 -0.832955 0.553341,
         -0.553341 0 0.832955, 0 0.832955 0.553341,
         0 0.832955 -0.553341, -0.832955 0.553341 0,
         -0.832955 -0.553341 0, 0 -0.832955 -0.553341,
         0.553341 0 -0.832955, -0.553341 0 -0.832955,
      ]
   }
   NormalBinding { value PER_FACE }
   Material {
      diffuseColor [
         1  0  0,   0 1  0,   0  0 1,   0  1  1,
         1  0  1,  .5 1  0,  .5  0 1,  .5  1  1,
         1 .3 .7,  .3 1 .7,  .3 .7 1,  .5 .5 .8
      ]
   }
   MaterialBinding { value PER_FACE }
   Coordinate3 {
      point [
         1.7265 0 0.618,    1 1 1,
         0 0.618 1.7265,    0 -0.618 1.7265,
         1 -1 1,    -1 -1 1,
         -0.618 -1.7265 0,    0.618 -1.7265 0,
         1 -1 -1,    1.7265 0 -0.618,
         1 1 -1,    0.618 1.7265 0,
         -0.618 1.7265 0,    -1 1 1,
         -1.7265 0 0.618,    -1.7265 0 -0.618,
         -1 -1 -1,    0 -0.618 -1.7265,
         0 0.618 -1.7265,    -1 1 -1
      ]
   }
   IndexedFaceSet {
      coordIndex [
         1, 2, 3, 4, 0, -1,  0, 9, 10, 11, 1, -1,
         4, 7, 8, 9, 0, -1,  3, 5, 6, 7, 4, -1,
         2, 13, 14, 5, 3, -1,  1, 11, 12, 13, 2, -1,
         10, 18, 19, 12, 11, -1,  19, 15, 14, 13, 12, -1,
         15, 16, 6, 5, 14, -1,  8, 7, 6, 16, 17, -1,
         9, 8, 17, 18, 10, -1,  18, 17, 16, 15, 19, -1,
      ]
   }
}"""

# Routine to create a scene graph representing a dodecahedron
def makeDodecahedron():
    # Read from the string.
    input = SoInput()
    input.setBuffer(dodecahedron)

    result = SoDB_readAll(input)

    return result

# CODE FOR The Inventor Mentor ENDS HERE
#############################################################

def main():
    # Initialize Inventor and Qt
    myWindow = SoGui.init(sys.argv[0])
    if myWindow == None: sys.exit(1)

    root = makeDodecahedron()
    root.ref()

    myViewer = SoGuiExaminerViewer(myWindow)
    myViewer.setSceneGraph(root)
    myViewer.setTitle("String Reader")
    myViewer.show()

    SoGui.show(myWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()
