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
# chapter 3.
#
# Create a little scene graph and then name some nodes and
# get back nodes by name.
#

from pivy import *
import sys

def RemoveCube():
   # Remove the cube named 'MyCube' from the separator named
   # 'Root'.  In a real application, isOfType() would probably
   # be used to make sure the nodes are of the correct type
   # before doing the cast.
   # In Pivy no cast is necessary as it gets autocasted for you.

   myRoot = SoNode.getByName("Root")

   myCube = SoNode.getByName("MyCube")
   
   myRoot.removeChild(myCube)

def main():
   SoDB.init()
    
   # Create some objects and give them names:
   root = SoSeparator()
   root.ref()
   root.setName("Root")
    
   myCube = SoCube()
   root.addChild(myCube)
   myCube.setName("MyCube")
    
   mySphere = SoSphere()
   root.addChild(mySphere)
   mySphere.setName("MySphere")
    
   RemoveCube()

if __name__ == "__main__":
   main()
