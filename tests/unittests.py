#!/usr/bin/env python

###
# Copyright (c) 2002-2004, Tamer Fahmy <tamer@tammura.at>
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
# Pivy unit test suite
#
# For detailed info on its usage and on how to write additional test cases
# read:
#   - http://pyunit.sourceforge.net/pyunit.html
#   - http://diveintopython.org/unit_testing/
#
# Invoke this script with '--help' for usage information.
#

from pivy import *
import unittest

class Autocasting(unittest.TestCase):
    def testFieldAutocast(self):
        """Check that SoSFBool created through createInstance() is autocasted to a SoSFBool field instance"""
        t = SoType.fromName(SbName("SoSFBool"))
        self.failUnless(isinstance(t.createInstance(), SoSFBool),
                        'not autocasted to an SoSFBool instance')
        
    def testNodeAutocast(self):
        """Check that SoCone created through createInstance() is autocasted to a SoCone node instance"""
        t = SoType.fromName(SbName("SoCone"))
        self.failUnless(isinstance(t.createInstance(), SoCone),
                        'not autocasted to an SoCone instance')

    def testNodeListAutocast(self):
        """Check that elements in NodeList classes are autocasted"""
        nl = SoNodeList()
        nl.append(SoCube())
        self.failUnless(isinstance(nl.get(0), SoCube),
                        'not autocasted to an SoCube instance')

if __name__ == "__main__":
    SoDB.init()
    unittest.main()
