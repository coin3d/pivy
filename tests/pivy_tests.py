#!/usr/bin/env python

###
# Copyright (c) 2002-2005, Tamer Fahmy <tamer@tammura.at>
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

from pivy.coin import *
import unittest
import math

class Autocasting(unittest.TestCase):
    def testFieldAutocast(self):
        """check autocasting for SoSFBool created through createInstance()"""
        t = SoType.fromName(SbName("SoSFBool"))
        self.failUnless(isinstance(t.createInstance(), SoSFBool),
                        'not autocasted to an SoSFBool instance')

    def testNodeAutocast(self):
        """check autocasting for SoCone created through createInstance()"""
        t = SoType.fromName(SbName("SoCone"))
        self.failUnless(isinstance(t.createInstance(), SoCone),
                        'not autocasted to an SoCone instance')

    def testNodeListAutocast(self):
        """check autocasting for elements in NodeList"""
        nl = SoNodeList()
        nl.append(SoCube())
        self.failUnless(isinstance(nl.get(0), SoCube),
                        'not autocasted to an SoCube instance')

    def testTypeAutocast(self):
        """check if type objects return casted instances"""
        tCube = SoType.fromName(SbName("SoCube"))
        cube = tCube.createInstance()
        self.failUnless(isinstance(cube, SoCube),
                        'SoType.createInstance not casted to SoCube')
        tSFBool = SoType.fromName(SbName("SoSFBool"))
        field = tSFBool.createInstance()
        self.failUnless(isinstance(field, SoSFBool),
                        'SoType.createInstance not casted to SoSFBool')
        tPath = SoType.fromName(SbName("SoPath"))
        path = tPath.createInstance()
        self.failUnless(isinstance(path, SoPath),
                        'SoType.createInstance not casted to SoPath') 

    def testFieldContainerAutocast(self):
        """check if a returned FieldContainer is casted"""
        m = SoMaterial()
        self.failUnless(isinstance(m.diffuseColor.getContainer(), SoMaterial),
                        'SoField.getContainer is not casted correctly')
                        
class FieldSetValue(unittest.TestCase):
    """checks various setValue(s) calls for fields"""
    def testSFBool(self):
        """check setValue for SFBool"""
        t = SoSFBool()
        s = SoSFBool()
        t.setValue(True)
        s.setValue(t)
        self.failUnless(True == t.getValue() == s.getValue(), 
                        'setValue on SoSFBool failed')

    def testSFColor(self):
        """check setValue for SFColor"""
        t = SoSFColor()
        s = SoSFColor()
        t.setValue(0,1,1)
        self.failUnless(t.getValue() == SbColor(0,1,1), 
                        'setValue 3 floats on SFColor failed')
        t.setValue([0,1,0])
        self.failUnless(t.getValue() == SbColor(0,1,0), 
                        'setValue float sequence on SFColor failed')
        t.setValue(SbColor(1,0,0))
        self.failUnless(t.getValue() == SbColor(1,0,0), 
                        'setValue SbColor on SFColor failed')
        t.setValue(SbVec3f(1,0,1))
        self.failUnless(t.getValue() == SbColor(1,0,1), 
                        'setValue SbVec3f on SFColor failed') 
        s.setValue(t)
        self.failUnless(t.getValue() == s.getValue(),
                        'setValue othe SFcolor on SFColor failed')
        
    def testSFEngine(self):
        """check setValue for SFEngine"""
        t = SoSFEngine()
        s = SoSFEngine()
        c = SoCounter()
        t.setValue(c)
        self.failUnless(t.getValue() == c, 
                        'setValue engine on SFEngine failed')
        s.setValue(t)
        self.failUnless(t.getValue() == s.getValue(), 
                        'setValue other SFEngine on SFEngine failed')

    def testSFString(self):
        """check setValue for SFString"""
        t = SoSFString()
        s = SoSFString()
        c = SbString('bla')
        t.setValue(c)
        self.failUnless(t.getValue() == c, 
                        'setValue SbString on SFString failed')
        t.setValue('hello')
        self.failUnless(t.getValue() == 'hello', 
                        'setValue string on SFString failed')        
        s.setValue(t)
        self.failUnless(t.getValue() == s.getValue(), 
                        'setValue other SFString on SFString failed')
        
    def testSFInt32(self):
        """check setValue for SFInt32"""
        t = SoSFInt32()
        s = SoSFInt32()
        t.setValue(10)
        s.setValue(t)
        self.failUnless(10 == t.getValue() == s.getValue(), 
                        'setValue on SoSFInt32 failed')

    def testSFFloat(self):
        """check setValue for SFFloat"""
        t = SoSFFloat()
        s = SoSFFloat()
        t.setValue(10.5)
        s.setValue(t)
        self.failUnless(10.5 == t.getValue() == s.getValue(), 
                        'setValue on SoSFFloat failed')

    def testSFShort(self):
        """check setValue for SFShort"""
        t = SoSFShort()
        s = SoSFShort()
        t.setValue(10)
        s.setValue(t)
        self.failUnless(10 == t.getValue() == s.getValue(), 
                        'setValue on SoSFShort failed')

    def testSFMatrix(self):
        """check setValue for SFMatrix"""
        t = SoSFMatrix()
        s = SoSFMatrix()
        # m = SbMatrix([[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0]])
        m2 = SbMatrix([[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]])
        t.setValue(m2)
        s.setValue(t)
        self.failUnless(m2 == t.getValue() == s.getValue(), 
                        'setValue on SoSFMatrix failed')                       

    def testSFName(self):
        """check setValue for SFName"""
        t = SoSFName()
        s = SoSFName()
        c = SbName('bla')
        t.setValue(c)
        self.failUnless(t.getValue() == c, 
                        'setValue SbName on SFName failed')
        t.setValue('hello')
        self.failUnless(t.getValue() == 'hello', 
                        'setValue string on SFName failed')        
        s.setValue(t)
        self.failUnless(t.getValue() == s.getValue(), 
                        'setValue other SFName on SFName failed')

    def testSFNode(self):
        """check setValue for SFNode"""
        t = SoSFNode()
        s = SoSFNode()
        c = SoCone()
        t.setValue(c)
        s.setValue(t)
        self.failUnless(c == t.getValue() == s.getValue(), 
                        'setValue on SoSFNode failed')
        self.failUnless(isinstance(t.getValue(), SoCone), 
                        'autocast on SoSFNode.getValue failed')
        
    def testSFRotation(self):
        """check setValue for SFRotation"""
        t = SoSFRotation()
        s = SoSFRotation()
        m = SbRotation(1,0,0,0)
        t.setValue(m)
        s.setValue(t)
        self.failUnless(m == t.getValue() == s.getValue(), 
                        'setValue on SoSFRotation failed') 
        t.setValue(0,1,0,0)
        self.failUnless(SbRotation(0,1,0,0) == t.getValue(),
                        'setValue on SoSFRotation from 4 values failed')
        t.setValue([0,0,1,0])
        self.failUnless(SbRotation(0,0,1,0) == t.getValue(),
                        'setValue on SoSFRotation from 4 values failed')        

    def testSFVec3f(self):
        """check setValue for SFVec3f"""
        t = SoSFVec3f()
        s = SoSFVec3f()
        t.setValue(0,1,1)
        self.failUnless(t.getValue() == SbVec3f(0,1,1), 
                        'setValue 3 floats on SFVec3f failed')
        t.setValue([0,1,0])
        self.failUnless(t.getValue() == SbVec3f(0,1,0), 
                        'setValue float sequence on SFVec3f failed')
        t.setValue(SbVec3f(1,0,0))
        self.failUnless(t.getValue() == SbVec3f(1,0,0), 
                        'setValue SbVec3f on SFVec3f failed')
        s.setValue(t)
        self.failUnless(t.getValue() == s.getValue(),
                        'setValue other SFVec3f on SFVec3f failed')

    def testSFVec2f(self):
        """check setValue for SFVec2f"""
        t = SoSFVec2f()
        s = SoSFVec2f()
        t.setValue(0,1)
        self.failUnless(t.getValue() == SbVec2f(0,1), 
                        'setValue 2 floats on SFVec2f failed')
        t.setValue([1,0])
        self.failUnless(t.getValue() == SbVec2f(1,0), 
                        'setValue float sequence on SFVec2f failed')
        t.setValue(SbVec2f(1,1))
        self.failUnless(t.getValue() == SbVec2f(1,1), 
                        'setValue SbVec2f on SFVec2f failed')
        s.setValue(t)
        self.failUnless(t.getValue() == s.getValue(),
                        'setValue other SFVec2f on SFVec2f failed')

    def testSFVec4f(self):
        """check setValue for SFVec4f"""
        t = SoSFVec4f()
        s = SoSFVec4f()
        t.setValue(0,1,1,0)
        self.failUnless(t.getValue() == SbVec4f(0,1,1,0), 
                        'setValue 4 floats on SFVec4f failed')
        t.setValue([0,1,0,1])
        self.failUnless(t.getValue() == SbVec4f(0,1,0,1), 
                        'setValue float sequence on SFVec4f failed')
        t.setValue(SbVec4f(1,0,0,1))
        self.failUnless(t.getValue() == SbVec4f(1,0,0,1), 
                        'setValue SbVec4f on SFVec4f failed')
        s.setValue(t)
        self.failUnless(t.getValue() == s.getValue(),
                        'setValue other SFVec4f on SFVec4f failed')

    def testSFImage(self):
        """check setValue for SFImage"""
        t = SoSFImage()
        s = SoSFImage()        
        t.setValue(SbVec2s(2,2), 1, "abcd")
        s.setValue(t)
        self.failUnless(("abcd", SbVec2s(2,2), 1) == t.getValue() == s.getValue(), 
                        'setValue on SoSFImage failed')

    def testSFImage3(self):
        """check setValue for SFImage3"""
        t = SoSFImage3()
        s = SoSFImage3()        
        t.setValue(SbVec3s(2,2,2), 1, "abcdefgh")
        s.setValue(t)
        self.failUnless(("abcdefgh", SbVec3s(2,2,2), 1) == t.getValue() == s.getValue(), 
                        'setValue on SoSFImage3 failed')

    def testSFPath(self):
        """check setValue for SFPath"""
        t = SoSFPath()
        s = SoSFPath()
        c = SoPath()
        c.ref()
        t.setValue(c)
        s.setValue(t)
        self.failUnless(c == t.getValue() == s.getValue(), 
                        'setValue on SoSFPath failed')
        self.failUnless(isinstance(t.getValue(), SoPath), 
                        'autocast on SoSFPath.getValue failed')

    def testSFPlane(self):
        """check setValue for SFPlane"""
        t = SoSFPlane()
        s = SoSFPlane()
        c = SbPlane()
        t.setValue(c)
        s.setValue(t)
        self.failUnless(c == t.getValue() == s.getValue(), 
                        'setValue on SoSFPlane failed')

    def testSFUInt32(self):
        """check setValue for SFUInt32"""
        t = SoSFUInt32()
        s = SoSFUInt32()
        t.setValue(10)
        s.setValue(t)
        self.failUnless(10 == t.getValue() == s.getValue(), 
                        'setValue on SoSFUInt32 failed')

    def testSFUShort(self):
        """check setValue for SFUShort"""
        t = SoSFUShort()
        s = SoSFUShort()
        t.setValue(10)
        s.setValue(t)
        self.failUnless(10 == t.getValue() == s.getValue(), 
                        'setValue on SoSFUShort failed')

    def testSFTime(self):
        """check setValue for SFTime"""
        t = SoSFTime()
        s = SoSFTime()
        t.setValue(150.5)
        s.setValue(t)
        self.failUnless(150.5 == t.getValue() == s.getValue(), 
                        'setValue on SoSFTime failed')

    def testMFBool(self):
        """check setValue(s) for MFBool"""
        t = SoMFBool()
        s = SoMFBool()
        t.setValues([0,1])
        self.failUnless(t.getValues() == [0,1],
                        'setValues with sequence on MFBool failed')
        t.setValues(2,[0,1])
        self.failUnless(t.getValues() == [0,1,0,1],
                        'setValues with start and sequence on MFBool failed')
        t.setValues(0,1,[1,0])
        self.failUnless(t.getValues() == [1,1,0,1],
                        'setValues with start, length and sequence on MFBool failed')
        t.setValue(s)
        self.failUnless(t.getValues() == s.getValues(),
                        'setValue with other MFBool on MFBool failed')
        t.setValue(0)
        self.failUnless(t.getValues() == [0],
                        'setValue with bool on MFBool failed')

    def testMFColor(self):
        """check setValue(s) for MFColor"""
        t = SoMFColor()
        s = SoMFColor()
        t.setValues([[0,0,1]])
        t.setValues(1,[[0,0,1]])
        t.setValues(2,1,[[0,0,1],[1,0,1]])
        self.failUnless(t.getValues() == [SbColor(0,0,1),SbColor(0,0,1),SbColor(0,0,1)],
                        'setValues with sequence of float triples on MFColor failed')                    
        t.setValue(s)
        self.failUnless(t.getValues() == s.getValues(),
                        'setValue with another MFColor failed' )
        t.setValues([SbColor(0,0,1)])
        t.setValues(1,[SbColor(0,0,1)])
        t.setValues(2,1,[SbColor(0,0,1), SbColor(1,0,1)])
        self.failUnless(t.getValues() == [SbColor(0,0,1),SbColor(0,0,1),SbColor(0,0,1)],
                        'setValues with sequence of SbColors on MFColor failed')                    
        t.setValues([])
        self.failUnless(t.getValues() == [SbColor(0,0,1),SbColor(0,0,1),SbColor(0,0,1)],
                        'setValue with empty sequence of SbColors failed' )

    def testMFEngine(self):
        """check setValue(s) for MFEngine"""
        t = SoMFEngine()
        s = SoMFEngine()
        c = SoCounter()
        c.ref()
        c2 = SoCounter()
        c2.ref()
        t.setValue(c)
        self.failUnless(t.getValues() == [c], 
                        'setValue engine on MFEngine failed')
        t.setValues([c,c2])
        self.failUnless(t.getValues() == [c,c2], 
                        'setValues on MFEngine failed')
        t.setValue(s)
        self.failUnless(t.getValues() == s.getValues(),
                        'setValue with other MFEngine on MFEngine failed')
        t.setValues(2,1,[c,c2])
        self.failUnless(t.getValues() == [None,None,c],
                        'setValues with start, length and sequence on MFEngine failed')

    def testMFEnum(self):
        """check setValue(s) for MFEnum"""
        t = SoMFEnum()
        s = SoMFEnum()
        t.setValues([0,2])
        self.failUnless(t.getValues() == [0,2],
                        'setValues with sequence on MFEnum failed')
        t.setValues(2,[0,1])
        self.failUnless(t.getValues() == [0,2,0,1],
                        'setValues with start and sequence on MFEnum failed')
        t.setValues(0,1,[-1,0])
        self.failUnless(t.getValues() == [-1,2,0,1],
                        'setValues with start, length and sequence on MFEnum failed')
        t.setValue(s)
        self.failUnless(t.getValues() == s.getValues(),
                        'setValue with other MFEnum on MFEnum failed')
        t.setValue(0)
        self.failUnless(t.getValues() == [0],
                        'setValue with single int on MFEnum failed')
        t.setValues([])
        self.failUnless(t.getValues() == [0],
                        'setValues with empty list on MFEnum failed')

    def testMFString(self):
        """check setValue(s) for MFString"""
        t = SoMFString()
        s = SoMFString()
        t.setValues(['1','2'])
        t.setValues(1,['3'])
        t.setValues(2,1,['4','5'])
        self.failUnless(t.getValues() == ['1','3','4'],
                        'setValues with sequence of strings on MFString failed')                    
        t.setValue(s)
        self.failUnless(t.getValues() == s.getValues(),
                        'setValue with another MFString failed' )
        t.setValues([SbString('1')])
        t.setValues(1,[SbString('2')])
        t.setValues(2,1,[SbString('3'), SbString('4')])
        self.failUnless(t.getValues() == ['1','2','3'],
                        'setValues with sequence of SbStrings on MFString failed')                    


    def testMFInt32(self):
        """check setValue(s) for MFInt32"""
        t = SoMFInt32()
        s = SoMFInt32()
        t.setValues([0,2])
        self.failUnless(t.getValues() == [0,2],
                        'setValues with sequence on MFInt32 failed')
        t.setValues(2,[0,1])
        self.failUnless(t.getValues() == [0,2,0,1],
                        'setValues with start and sequence on MFInt32 failed')
        t.setValues(0,1,[-1,0])
        self.failUnless(t.getValues() == [-1,2,0,1],
                        'setValues with start, length and sequence on MFInt32 failed')
        t.setValue(s)
        self.failUnless(t.getValues() == s.getValues(),
                        'setValue with other MFInt32 on MFInt32 failed')
        t.setValue(0)
        self.failUnless(t.getValues() == [0],
                        'setValue with single int on MFInt32 failed')
        t.setValues([])
        self.failUnless(t.getValues() == [0],
                        'setValues with empty list on MFInt32 failed')

    def testMFFloat(self):
        """check setValue(s) for MFFloat"""
        t = SoMFFloat()
        s = SoMFFloat()
        t.setValues([0.5,2])
        self.failUnless(t.getValues() == [0.5,2],
                        'setValues with sequence on MFFloat failed')
        t.setValues(2,[0,1])
        self.failUnless(t.getValues() == [0.5,2,0,1],
                        'setValues with start and sequence on MFFloat failed')
        t.setValues(0,1,[1.5,0])
        self.failUnless(t.getValues() == [1.5,2,0,1],
                        'setValues with start, length and sequence on MFFloat failed')
        t.setValue(s)
        self.failUnless(t.getValues() == s.getValues(),
                        'setValue with other MFFloat on MFFloat failed')
        t.setValue(-0.5)
        self.failUnless(t.getValues() == [-0.5],
                        'setValue with single int on MFFloat failed')
        t.setValues([])
        self.failUnless(t.getValues() == [-0.5],
                        'setValues with empty list on MFFloat failed')     

    def testMFShort(self):
        """check setValue(s) for MFShort"""
        t = SoMFShort()
        s = SoMFShort()
        t.setValues([0,2])
        self.failUnless(t.getValues() == [0,2],
                        'setValues with sequence on MFShort failed')
        t.setValues(2,[0,1])
        self.failUnless(t.getValues() == [0,2,0,1],
                        'setValues with start and sequence on MFShort failed')
        t.setValues(0,1,[-1,0])
        self.failUnless(t.getValues() == [-1,2,0,1],
                        'setValues with start, length and sequence on MFShort failed')
        t.setValue(s)
        self.failUnless(t.getValues() == s.getValues(),
                        'setValue with other MFShort on MFShort failed')
        t.setValue(0)
        self.failUnless(t.getValues() == [0],
                        'setValue with single int on MFShort failed')
        t.setValues([])
        self.failUnless(t.getValues() == [0],
                        'setValues with empty list on MFShort failed')
        
    def testMFMatrix(self):
        """check setValue(s) for MFMatrix"""
        t = SoMFMatrix()
        s = SoMFMatrix()
        m = SbMatrix([[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0]])
        m2 = SbMatrix([[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]])
        t.setValues([m])
        self.failUnless(t.getValues() == [m],
                        'setValues with sequence on MFMatrix failed')
        t.setValues(2,[m2,m2])
        self.failUnless(t.getValues()[2:4] == [m2,m2],
                        'setValues with start and sequence on MFMatrix failed')
        t.setValues(1,1,[m2,m])
        self.failUnless(t.getValues() == [m,m2,m2,m2],
                        'setValues with start, length and sequence on MFMatrix failed')
        t.setValue(s)
        self.failUnless(t.getValues() == s.getValues(),
                        'setValue with other MFMatrix on MFMatrix failed')
        t.setValue(m2)
        self.failUnless(t.getValues() == [m2],
                        'setValue with single int on MFMatrix failed')
        t.setValues([])
        self.failUnless(t.getValues() == [m2],
                        'setValues with empty list on MFMatrix failed')                     

    def testMFName(self):
        """check setValue(s) for MFName"""
        t = SoMFName()
        s = SoMFName()
        t.setValues(['1','2'])
        t.setValues(1,['3'])
        t.setValues(2,1,['4','5'])
        self.failUnless(t.getValues() == ['1','3','4'],
                        'setValues with sequence of Names on MFName failed')                    
        t.setValue(s)
        self.failUnless(t.getValues() == s.getValues(),
                        'setValue with another MFName failed' )
        t.setValues([SbName('1')])
        t.setValues(1,[SbName('2')])
        t.setValues(2,1,[SbName('3'), SbName('4')])
        self.failUnless(t.getValues() == ['1','2','3'],
                        'setValues with sequence of SbNames on MFName failed')                    

    def testMFNode(self):
        """check setValue(s) for MFNode"""
        t = SoMFNode()
        s = SoMFNode()
        c = SoMaterial()
        c.ref()
        c2 = SoTransform()
        c2.ref()
        t.setValue(c)
        self.failUnless(t.getValues() == [c], 
                        'setValue Node on MFNode failed')
        t.setValues([c,c2])
        self.failUnless(t.getValues() == [c,c2], 
                        'setValues on MFNode failed')
        t.setValue(s)
        self.failUnless(t.getValues() == s.getValues(),
                        'setValue with other MFNode on MFNode failed')
        t.setValues(2,1,[c,c2])
        self.failUnless(t.getValues() == [None,None,c],
                        'setValues with start, length and sequence on MFNode failed')         

    def testMFPath(self):
        """check setValue(s) for MFPath"""
        t = SoMFPath()
        s = SoMFPath()
        p = SoPath()
        p.ref()
        p2 = SoPath()
        p2.ref()
        t.setValue(p)
        self.failUnless(t.getValues() == [p], 
                        'setValue Path on MFPath failed')
        t.setValues([p,p2])
        self.failUnless(t.getValues() == [p,p2], 
                        'setValues on MFPath failed')
        t.setValue(s)
        self.failUnless(t.getValues() == s.getValues(),
                        'setValue with other MFPath on MFPath failed')
        t.setValues(2,1,[p,p2])
        self.failUnless(t.getValues() == [None,None,p],
                        'setValues with start, length and sequence on MFPath failed')         

    def testMFPlane(self):
        """check setValue(s) for MFPlane"""
        t = SoMFPlane()
        s = SoMFPlane()
        m = SbPlane(SbVec3f(1,0,0),0)
        m2 = SbPlane(SbVec3f(0,1,0),1)
        t.setValues([m])
        self.assertEqual(t.getValues(), [m])
        t.setValues(2,[m2,m2])
        self.assertEqual(t.getValues()[2:4],[m2,m2])
        t.setValues(1,1,[m2,m])
        self.assertEqual(t.getValues(), [m,m2,m2,m2])
        t.setValue(s)
        self.assertEqual(t.getValues(), s.getValues())
        t.setValue(m2)
        self.assertEqual(t.getValues(), [m2])
        t.setValues([])
        self.assertEqual(t.getValues(), [m2]) # appears to be the correct behaviour as in Coin :/

    def testMFRotation(self):
        """check setValue(s) for MFRotation"""
        t = SoMFRotation()
        s = SoMFRotation()
        m = SbRotation(1,0,0,0)
        m2 = SbRotation(0,0,0,1)
        t.setValues([m])
        self.assertEqual(t.getValues(), [m])
        t.setValues(2,[m2,m2])
        self.assertEqual(t.getValues()[2:4],[m2,m2])
        t.setValues(1,1,[m2,m])
        self.assertEqual(t.getValues(), [m,m2,m2,m2])
        t.setValue(s)
        self.assertEqual(t.getValues(), s.getValues())
        t.setValue(m2)
        self.assertEqual(t.getValues(), [m2])
        t.setValue(1,0,0,0)
        self.assertEqual(t.getValues(), [m])
        t.setValue([0,0,0,1])
        self.assertEqual(t.getValues(), [m2])
        t.setValues([])
        self.assertEqual(t.getValues(), [m2]) # appears to be the correct behaviour as in Coin :/

    def testMFTime(self):
        """check setValue(s) for MFTime"""
        t = SoMFTime()
        s = SoMFTime()
        t.setValues([SbTime(0.5),SbTime(2)])
        self.failUnless(t.getValues() == [SbTime(0.5),SbTime(2)],
                        'setValues with sequence on MFTime failed')
        t.setValues(2,[SbTime(0),SbTime(1)])
        self.failUnless(t.getValues() == [SbTime(0.5),SbTime(2),SbTime(0),SbTime(1)],
                        'setValues with start and sequence on MFTime failed')
        t.setValues(0,1,[SbTime(1.5),SbTime(0)])
        self.failUnless(t.getValues() == [SbTime(1.5),SbTime(2),SbTime(0),SbTime(1)],
                        'setValues with start, length and sequence on MFTime failed')
        t.setValue(s)
        self.failUnless(t.getValues() == s.getValues(),
                        'setValue with other MFTime on MFTime failed')
        t.setValue(SbTime(-0.5))
        self.failUnless(t.getValues() == [SbTime(-0.5)],
                        'setValue with single int on MFTime failed')
        t.setValues([])
        self.failUnless(t.getValues() == [SbTime(-0.5)],
                        'setValues with empty list on MFTime failed') 

    def testMFUInt32(self):
        """check setValue(s) for MFUInt32"""
        t = SoMFUInt32()
        s = SoMFUInt32()
        t.setValues([0,2])
        self.failUnless(t.getValues() == [0,2],
                        'setValues with sequence on MFUInt32 failed')
        t.setValues(2,[0,1])
        self.failUnless(t.getValues() == [0,2,0,1],
                        'setValues with start and sequence on MFUInt32 failed')
        t.setValues(0,1,[1,0])
        self.failUnless(t.getValues() == [1,2,0,1],
                        'setValues with start, length and sequence on MFUInt32 failed')
        t.setValue(s)
        self.failUnless(t.getValues() == s.getValues(),
                        'setValue with other MFUInt32 on MFUInt32 failed')
        t.setValue(0)
        self.failUnless(t.getValues() == [0],
                        'setValue with single int on MFUInt32 failed')
        t.setValues([])
        self.failUnless(t.getValues() == [0],
                        'setValues with empty list on MFUInt32 failed')

    def testMFUShort(self):
        """check setValue(s) for MFUShort"""
        t = SoMFUShort()
        s = SoMFUShort()
        t.setValues([0,2])
        self.failUnless(t.getValues() == [0,2],
                        'setValues with sequence on MFUShort failed')
        t.setValues(2,[0,1])
        self.failUnless(t.getValues() == [0,2,0,1],
                        'setValues with start and sequence on MFUShort failed')
        t.setValues(0,1,[1,0])
        self.failUnless(t.getValues() == [1,2,0,1],
                        'setValues with start, length and sequence on MFUShort failed')
        t.setValue(s)
        self.failUnless(t.getValues() == s.getValues(),
                        'setValue with other MFUShort on MFUShort failed')
        t.setValue(0)
        self.failUnless(t.getValues() == [0],
                        'setValue with single int on MFUShort failed')
        t.setValues([])
        self.failUnless(t.getValues() == [0],
                        'setValues with empty list on MFUShort failed')

    def testMFVec2f(self):
        """check setValue(s) for MFVec2f"""
        t = SoMFVec2f()
        s = SoMFVec2f()
        m = SbVec2f(1,0)
        m2 = SbVec2f(0,0)
        t.setValues([m])
        self.assertEqual(t.getValues(), [m])
        t.setValues(2,[m2,m2])
        self.assertEqual(t.getValues()[2:4],[m2,m2])
        t.setValues(1,1,[m2,m])
        self.assertEqual(t.getValues(), [m,m2,m2,m2])
        t.setValue(s)
        self.assertEqual(t.getValues(), s.getValues())
        t.setValue(m2)
        self.assertEqual(t.getValues(), [m2])
        t.setValues([])
        self.assertEqual(t.getValues(), [m2]) 
        t.setValues([[0,0],[1,0]])
        self.assertEqual(t.getValues(), [m2,m])
        t.setValue([0,0])
        self.assertEqual(t.getValues(), [m2])

    def testMFVec3f(self):
        """check setValue(s) for MFVec3f"""
        t = SoMFVec3f()
        s = SoMFVec3f()
        m = SbVec3f(1,0,0)
        m2 = SbVec3f(0,0,1)
        t.setValues([m])
        self.assertEqual(t.getValues(), [m])
        t.setValues(2,[m2,m2])
        self.assertEqual(t.getValues()[2:4],[m2,m2])
        t.setValues(1,1,[m2,m])
        self.assertEqual(t.getValues(), [m,m2,m2,m2])
        t.setValue(s)
        self.assertEqual(t.getValues(), s.getValues())
        t.setValue(m2)
        self.assertEqual(t.getValues(), [m2])
        t.setValues([])
        self.assertEqual(t.getValues(), [m2]) 
        t.setValues([[0,0,1],[1,0,0]])
        self.assertEqual(t.getValues(), [m2,m])
        t.setValue([0,0,1])
        self.assertEqual(t.getValues(), [m2])       

    def testMFVec4f(self):
        """check setValue(s) for MFVec4f"""
        t = SoMFVec4f()
        s = SoMFVec4f()
        m = SbVec4f(1,0,0,0)
        m2 = SbVec4f(0,0,1,0)
        t.setValues([m])
        self.assertEqual(t.getValues(), [m])
        t.setValues(2,[m2,m2])
        self.assertEqual(t.getValues()[2:4],[m2,m2])
        t.setValues(1,1,[m2,m])
        self.assertEqual(t.getValues(), [m,m2,m2,m2])
        t.setValue(s)
        self.assertEqual(t.getValues(), s.getValues())
        t.setValue(m2)
        self.assertEqual(t.getValues(), [m2])
        t.setValues([])
        self.assertEqual(t.getValues(), [m2]) 
        t.setValues([[0,0,1,0],[1,0,0,0]])
        self.assertEqual(t.getValues(), [m2,m])
        t.setValue([0,0,1,0])
        self.assertEqual(t.getValues(), [m2])        


class SbStringMethods(unittest.TestCase):
    """tests various string stuff"""
    def testCharConstructor(self):
        """check SbString(char *)"""
        s = SbString('hello')
        self.assertEqual(s.getString(), 'hello')

    def testCharLimits(self):
        """check SbString(char *, int begin, int end)"""
        s = SbString('hello', 1, 3)
        self.assertEqual(s.getString(), 'ell')

    def testOtherString(self):
        """check SbString(SbString)"""
        s = SbString('hello')
        t = SbString(s)
        self.assertEqual(s.getString(), t.getString())

    def testDigits(self):
        """check SbString(int)"""
        s = SbString(100)
        self.assertEqual(s.getString(), '100' )

class SbNameMethods(unittest.TestCase):
    """tests various Name stuff"""
    def testCharConstructor(self):
        """check SbName(char *)"""
        s = SbName('hello')
        self.assertEqual(s.getString(), 'hello')

    def testOtherName(self):
        """check SbName(SbName)"""
        s = SbName('hello')
        t = SbName(s)
        self.assertEqual(s.getString(), t.getString())

    def testOtherString(self):
        """check SbName(SbString)"""
        s = SbString('hello')
        t = SbName(s)
        self.assertEqual(s.getString(), t.getString())

    def testFromName(self):
        """check passing strings instead of SbName to SoType.fromName()"""
        t = SoType.fromName("SoCone")

class SbRotationMethods(unittest.TestCase):
    "tests various Rotation stuff"""
    def testAxisAngleCons(self):
        """check SbRotation(SbVector, float)"""
        r = SbRotation(SbVec3f(1,0,0), 3.14159264)
        self.assertEqual(r.getValue(), (1.0,0.0,0.0,-4.3711388286737929e-008))

    def testFloat4Cons(self):
        """check SbRotation(float[4])"""
        r = SbRotation((1.0,0.0,0.0,0.0))
        self.assertEqual(r.getValue(), (1.0,0.0,0.0,0.0))

    def testFloatsCons(self):
        """check SbRotation(float,float,float,float)"""
        r = SbRotation(1.0,0.0,0.0,0.0)
        self.assertEqual(r.getValue(), (1.0,0.0,0.0,0.0))

    def testMatrixCons(self):
        """check SbRotation(SbMatrix)"""
        m = SbMatrix()
        m.setRotate(SbRotation(1.0,0.0,0.0,0.0))
        r = SbRotation(m)
        self.assertEqual(r.getValue(), (1.0,0.0,0.0,0.0))

    def testVecFTCons(self):
        """check SbRotation(SbVec3f, SbVec3f)"""
        r = SbRotation(SbVec3f(1,0,0), SbVec3f(0,1,0))
        r = r*r
        self.assertEqual(r.getValue(), (0.0,0.0,1.0,0.0))

    def testAxisAngleSet(self):
        """check SbRotation.setValue(SbVector, float)"""
        r = SbRotation()
        r.setValue(SbVec3f(1,0,0), 3.14159264)
        self.assertEqual(r.getValue(), (1.0,0.0,0.0,-4.3711388286737929e-008))

    def testFloat4Set(self):
        """check SbRotation.setValue(float[4])"""
        r = SbRotation()
        r.setValue(1.0,0.0,0.0,0.0)
        self.assertEqual(r.getValue(), (1.0,0.0,0.0,0.0))

    def testFloatsSet(self):
        """check SbRotation.setValue(float,float,float,float)"""
        r = SbRotation()
        r.setValue(1.0,0.0,0.0,0.0)
        self.assertEqual(r.getValue(), (1.0,0.0,0.0,0.0))

    def testMatrixSet(self):
        """check SbRotation.setValue(SbMatrix)"""
        m = SbMatrix()
        m.setRotate(SbRotation(1.0,0.0,0.0,0.0))
        r = SbRotation()
        r.setValue(m)
        self.assertEqual(r.getValue(), (1.0,0.0,0.0,0.0))

    def testVecFTSet(self):
        """check SbRotation.setValue(SbVec3f, SbVec3f)"""
        r = SbRotation()
        r.setValue(SbVec3f(1,0,0), SbVec3f(0,1,0))
        r = r*r
        self.assertEqual(r.getValue(), (0.0,0.0,1.0,0.0))        

class SoBaseListMethods(unittest.TestCase):
    """tests various methods of SoBaseList"""
    def testGet(self):
        """check SoBaseList.get downcast type return"""
        l = SoBaseList()
        c = SoCone()
        l.append(c)
        self.assert_(isinstance(l.get(0), SoCone))

    def testItem(self):
        """check SoBaseList[] downcast type return"""
        l = SoBaseList()
        c = SoCone()
        l.append(c)
        self.assert_(isinstance(l[0], SoCone))

    def testSetItem(self):
        """check SoBaseList [0] = value support"""
        l = SoBaseList()
        f = SoCone()
        l.append(None) # note, that the set method underlying access does not expand!
        l[0] = f
        self.assert_(l[0].this == f.this)

    def testIteration(self):
        """check iteration support by all lists derived from SbPList"""
        l = SoBaseList()
        c = SoCone()
        l.append(c)
        for x in l:
            self.assert_(x.this == c.this)

class SoNodeListMethods(unittest.TestCase):
    """tests various methods of SoNodeList"""
    def testGet(self):
        """check SoNodeList.get() downcast type return"""
        l = SoNodeList()
        c = SoCone()
        l.append(c)
        self.assert_(isinstance(l.get(0), SoCone))

    def testItem(self):
        """check SoNodeList[] downcast type return"""
        l = SoNodeList()
        c = SoCone()
        l.append(c)
        self.assert_(isinstance(l[0], SoCone))

    def testSetItem(self):
        """check SoNodeList [0] = value support"""
        l = SoNodeList()
        c = SoCone()
        l.append(None) # note, that the set method underlying access does not expand!
        l[0] = c
        self.assert_(l[0].this == c.this)

class SoFieldListMethods(unittest.TestCase):
    """tests various methods of SoFieldList"""
    def testGet(self):
        """check SoFieldList.get() downcast type return"""
        l = SoFieldList()
        f = SoSFBool()
        l.append(f)
        self.assert_(isinstance(l.get(0), SoSFBool))

    def testItem(self):
        """check SoFieldList[] downcast type return"""
        l = SoFieldList()
        f = SoSFBool()
        l.append(f)
        self.assert_(isinstance(l[0], SoSFBool))

    def testSetItem(self):
        """check SoFieldList [0] = value support"""
        l = SoFieldList()
        f = SoSFBool()
        l[0] = f
        self.assert_(l[0] == f)

class FieldAssignment(unittest.TestCase):
    """tests field assignment for all kinds of types"""
    def testAssign(self):
        """check field assignment for all kinds of types"""
        n = SoCone()
        n.bottomRadius = 10
        self.assertEqual(n.bottomRadius.getValue(), 10 )
        n = SoInfo()
        n.string = "hello"
        self.assertEqual(n.string.getValue(), "hello" )

class SoFieldMethods(unittest.TestCase):
    """test SoField methods"""
    def testGet(self):
        """check SoField.get() ASCII field's value return"""
        s = SoSFVec3f()
        s.setValue(1,2,3)
        self.failUnless(s.get() == "1 2 3",
                        'SoField.get() failed')
                        
    def testLen(self):
        """check len() for MFields"""
        s = SoMFInt32()
        self.failUnless(len(s) == 0 == s.getNum(),
                        'len(s) on empty field failed')
        s.setValues([1,2,3])
        self.failUnless(len(s) == 3 == s.getNum(),
                        'len(s) on non-empty field failed')

class SbTimeMethods(unittest.TestCase):
    """test SbTime methods"""
    def testConstructors(self):
        """check SbTime constructors"""
        t1 = SbTime()
        t2 = SbTime(12.005)
        t3 = SbTime(12, 5000)
        self.assertEqual( t2, t3 )
        
    def testSetValue(self):
        """check SbTime setValue methods"""
        t1 = SbTime(12.005)
        t2 = SbTime()
        t2.setValue(12.005)
        self.assertEqual(t1, t2)
        t2.setValue(12, 5000)
        self.assertEqual(t1, t2)

class OperatorTests(unittest.TestCase):
    """checks various operator overloaded methods"""
    def testEqNone(self):
        """check __eq__ operator None comparison"""
        self.failUnless(not (SoSeparator() == None))
        
    def testNqNone(self):
        """check __nq__ operator None comparison"""
        self.failUnless((SoSeparator() != None))
        
if __name__ == "__main__":
    SoDB.init()
    unittest.main()
