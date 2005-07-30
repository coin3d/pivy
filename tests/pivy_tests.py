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

from pivy.coin import *
import unittest
import math

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

class FieldSetValue(unittest.TestCase):
    """checks various setValue(s) calls for fields"""
    def testSFBool(self):
        """check setValue for SFBool"""
        t = SoSFBool()
        s = SoSFBool()
        t.setValue(TRUE)
        s.setValue(t)
        self.failUnless(TRUE == t.getValue() == s.getValue(), 
                        'setValue on SoSFBool failed')
                        
    def testSFColor(self):
        """check setValue for SFColor"""
        t = SoSFColor()
        s = SoSFColor()
        t.setValue(0,1,1)
        self.failUnless( t.getValue() == SbColor(0,1,1), 
                         'setValue 3 floats on SFColor failed')
        t.setValue([0,1,0])
        self.failUnless( t.getValue() == SbColor(0,1,0), 
                         'setValue float sequence on SFColor failed')
        t.setValue(SbColor(1,0,0))
        self.failUnless( t.getValue() == SbColor(1,0,0), 
                         'setValue SbColor on SFColor failed')
        t.setValue(SbVec3f(1,0,1))
        self.failUnless( t.getValue() == SbColor(1,0,1), 
                         'setValue SbVec3f on SFColor failed') 
        s.setValue(t)
        self.failUnless( t.getValue() == s.getValue(),
                         'setValue othe SFcolor on SFColor failed')
      
    def testSFEngine(self):
        """check setValue for SFEngine"""
        t = SoSFEngine()
        s = SoSFEngine()
        c = SoCounter()
        t.setValue(c)
        self.failUnless( t.getValue() == c, 
                         'setValue engine on SFEngine failed')
        s.setValue(t)
        self.failUnless( t.getValue() == s.getValue(), 
                         'setValue other SFEngine on SFEngine failed')

    def testMFBool(self):
        """check setValue(s) for MFBool"""
        t = SoMFBool()
        s = SoMFBool()
        t.setValues([0,1])
        self.failUnless( t.getValues() == [0,1],
                         'setValues with sequence on MFBool failed')
        t.setValues(2,[0,1])
        self.failUnless( t.getValues() == [0,1,0,1],
                         'setValues with start and sequence on MFBool failed')
        t.setValues(0,1,[1,0])
        self.failUnless( t.getValues() == [1,1,0,1],
                         'setValues with start, length and sequence on MFBool failed')
        t.setValue(s)
        self.failUnless( t.getValues() == s.getValues(),
                         'setValue with other MFBool on MFBool failed')
        t.setValue(0)
        self.failUnless( t.getValues() == [0],
                         'setValue with bool on MFBool failed')

    def testMFColor(self):
        """check setValue(s) for MFColor"""
        t = SoMFColor()
        s = SoMFColor()
        t.setValues([[0,0,1]])
        t.setValues(1,[[0,0,1]])
        t.setValues(2,1,[[0,0,1],[1,0,1]])
        self.failUnless( t.getValues() == [SbColor(0,0,1),SbColor(0,0,1),SbColor(0,0,1)],
                         'setValues with sequence of float triples on MFColor failed')                    
        t.setValue(s)
        self.failUnless( t.getValues() == s.getValues(),
                         'setValue with another MFColor failed' )
        t.setValues([SbColor(0,0,1)])
        t.setValues(1,[SbColor(0,0,1)])
        t.setValues(2,1,[SbColor(0,0,1), SbColor(1,0,1)])
        self.failUnless( t.getValues() == [SbColor(0,0,1),SbColor(0,0,1),SbColor(0,0,1)],
                                 'setValues with sequence of SbColors on MFColor failed')                    
        t.setValues([])
        self.failUnless( t.getValues() == [SbColor(0,0,1),SbColor(0,0,1),SbColor(0,0,1)],
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
        self.failUnless( t.getValues() == [c], 
                         'setValue engine on MFEngine failed')
        t.setValues([c,c2])
        self.failUnless( t.getValues() == [c,c2], 
                         'setValues on MFEngine failed')
        t.setValue(s)
        self.failUnless( t.getValues() == s.getValues(),
                         'setValue with other MFEngine on MFEngine failed')
        t.setValues(2,1,[c,c2])
        self.failUnless( t.getValues() == [None,None,c],
                         'setValues with start, length and sequence on MFEngine failed')
                         
    def testMFString(self):
        """check setValue(s) for MFString"""
        t = SoMFString()
        s = SoMFString()
        t.setValues(['1','2'])
        t.setValues(1,['3'])
        t.setValues(2,1,['4','5'])
        self.failUnless( t.getValues() == ['1','3','4'],
                         'setValues with sequence of strings on MFString failed')                    
        t.setValue(s)
        self.failUnless( t.getValues() == s.getValues(),
                         'setValue with another MFString failed' )
        t.setValues([SbString('1')])
        t.setValues(1,[SbString('2')])
        t.setValues(2,1,[SbString('3'), SbString('4')])
        self.failUnless( t.getValues() == ['1','2','3'],
                         'setValues with sequence of SbStrings on MFString failed')                    
                         
                         
    def testMFInt32(self):
        """check setValue(s) for MFInt32"""
        t = SoMFInt32()
        s = SoMFInt32()
        t.setValues([0,2])
        self.failUnless( t.getValues() == [0,2],
                         'setValues with sequence on MFInt32 failed')
        t.setValues(2,[0,1])
        self.failUnless( t.getValues() == [0,2,0,1],
                         'setValues with start and sequence on MFInt32 failed')
        t.setValues(0,1,[1,0])
        self.failUnless( t.getValues() == [1,2,0,1],
                         'setValues with start, length and sequence on MFInt32 failed')
        t.setValue(s)
        self.failUnless( t.getValues() == s.getValues(),
                         'setValue with other MFInt32 on MFInt32 failed')
        t.setValue(0)
        self.failUnless( t.getValues() == [0],
                         'setValue with single int on MFInt32 failed')
        t.setValues([])
        self.failUnless( t.getValues() == [0],
                         'setValues with empty list on MFInt32 failed')

    def testMFFloat(self):
        """check setValue(s) for MFFloat"""
        t = SoMFFloat()
        s = SoMFFloat()
        t.setValues([0.5,2])
        self.failUnless( t.getValues() == [0.5,2],
                         'setValues with sequence on MFFloat failed')
        t.setValues(2,[0,1])
        self.failUnless( t.getValues() == [0.5,2,0,1],
                         'setValues with start and sequence on MFFloat failed')
        t.setValues(0,1,[1.5,0])
        self.failUnless( t.getValues() == [1.5,2,0,1],
                         'setValues with start, length and sequence on MFFloat failed')
        t.setValue(s)
        self.failUnless( t.getValues() == s.getValues(),
                         'setValue with other MFFloat on MFFloat failed')
        t.setValue(-0.5)
        self.failUnless( t.getValues() == [-0.5],
                         'setValue with single int on MFFloat failed')
        t.setValues([])
        self.failUnless( t.getValues() == [-0.5],
                         'setValues with empty list on MFFloat failed')     

    def testMFShort(self):
        """check setValue(s) for MFShort"""
        t = SoMFShort()
        s = SoMFShort()
        t.setValues([0,2])
        self.failUnless( t.getValues() == [0,2],
                         'setValues with sequence on MFShort failed')
        t.setValues(2,[0,1])
        self.failUnless( t.getValues() == [0,2,0,1],
                         'setValues with start and sequence on MFShort failed')
        t.setValues(0,1,[1,0])
        self.failUnless( t.getValues() == [1,2,0,1],
                         'setValues with start, length and sequence on MFShort failed')
        t.setValue(s)
        self.failUnless( t.getValues() == s.getValues(),
                         'setValue with other MFShort on MFShort failed')
        t.setValue(0)
        self.failUnless( t.getValues() == [0],
                         'setValue with single int on MFShort failed')
        t.setValues([])
        self.failUnless( t.getValues() == [0],
                     'setValues with empty list on MFShort failed')
                     
    def testMFMatrix(self):
        """check setValue(s) for MFMatrix"""
        t = SoMFMatrix()
        s = SoMFMatrix()
        m = SbMatrix([[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0]])
        m2 = SbMatrix([[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]])
        t.setValues([m])
        self.failUnless( t.getValues() == [m],
                         'setValues with sequence on MFMatrix failed')
        t.setValues(2,[m2,m2])
        self.failUnless( t.getValues()[2:4] == [m2,m2],
                         'setValues with start and sequence on MFMatrix failed')
        t.setValues(1,1,[m2,m])
        self.failUnless( t.getValues() == [m,m2,m2,m2],
                         'setValues with start, length and sequence on MFMatrix failed')
        t.setValue(s)
        self.failUnless( t.getValues() == s.getValues(),
                         'setValue with other MFMatrix on MFMatrix failed')
        t.setValue(m2)
        self.failUnless( t.getValues() == [m2],
                         'setValue with single int on MFMatrix failed')
        t.setValues([])
        self.failUnless( t.getValues() == [m2],
                     'setValues with empty list on MFMatrix failed')                     
       
    def testMFName(self):
        """check setValue(s) for MFName"""
        t = SoMFName()
        s = SoMFName()
        t.setValues(['1','2'])
        t.setValues(1,['3'])
        t.setValues(2,1,['4','5'])
        self.failUnless( t.getValues() == ['1','3','4'],
                         'setValues with sequence of Names on MFName failed')                    
        t.setValue(s)
        self.failUnless( t.getValues() == s.getValues(),
                         'setValue with another MFName failed' )
        t.setValues([SbName('1')])
        t.setValues(1,[SbName('2')])
        t.setValues(2,1,[SbName('3'), SbName('4')])
        self.failUnless( t.getValues() == ['1','2','3'],
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
        self.failUnless( t.getValues() == [c], 
                         'setValue Node on MFNode failed')
        t.setValues([c,c2])
        self.failUnless( t.getValues() == [c,c2], 
                         'setValues on MFNode failed')
        t.setValue(s)
        self.failUnless( t.getValues() == s.getValues(),
                         'setValue with other MFNode on MFNode failed')
        t.setValues(2,1,[c,c2])
        self.failUnless( t.getValues() == [None,None,c],
                         'setValues with start, length and sequence on MFNode failed')         

    def testMFRotation(self):
        """check setValue(s) for MFRotation"""
        t = SoMFRotation()
        s = SoMFRotation()
        m = SbRotation(1,0,0,0)
        m2 = SbRotation(0,0,0,1)
        t.setValues([m])
        self.assertEqual( t.getValues(), [m])
        t.setValues(2,[m2,m2])
        self.assertEqual( t.getValues()[2:4],[m2,m2])
        t.setValues(1,1,[m2,m])
        self.assertEqual( t.getValues(), [m,m2,m2,m2])
        t.setValue(s)
        self.assertEqual( t.getValues(), s.getValues())
        t.setValue(m2)
        self.assertEqual( t.getValues(), [m2])
        t.setValues([])
        self.assertEqual( t.getValues(), [m2])  
        
    def testMFVec2f(self):
        """check setValue(s) for MFVec2f"""
        t = SoMFVec2f()
        s = SoMFVec2f()
        m = SbVec2f(1,0)
        m2 = SbVec2f(0,0)
        t.setValues([m])
        self.assertEqual( t.getValues(), [m])
        t.setValues(2,[m2,m2])
        self.assertEqual( t.getValues()[2:4],[m2,m2])
        t.setValues(1,1,[m2,m])
        self.assertEqual( t.getValues(), [m,m2,m2,m2])
        t.setValue(s)
        self.assertEqual( t.getValues(), s.getValues())
        t.setValue(m2)
        self.assertEqual( t.getValues(), [m2])
        t.setValues([])
        self.assertEqual( t.getValues(), [m2]) 
        t.setValues([[0,0],[1,0]])
        self.assertEqual( t.getValues(), [m2,m])
        t.setValue([0,0])
        self.assertEqual( t.getValues(), [m2])
        
    def testMFVec3f(self):
        """check setValue(s) for MFVec3f"""
        t = SoMFVec3f()
        s = SoMFVec3f()
        m = SbVec3f(1,0,0)
        m2 = SbVec3f(0,0,1)
        t.setValues([m])
        self.assertEqual( t.getValues(), [m])
        t.setValues(2,[m2,m2])
        self.assertEqual( t.getValues()[2:4],[m2,m2])
        t.setValues(1,1,[m2,m])
        self.assertEqual( t.getValues(), [m,m2,m2,m2])
        t.setValue(s)
        self.assertEqual( t.getValues(), s.getValues())
        t.setValue(m2)
        self.assertEqual( t.getValues(), [m2])
        t.setValues([])
        self.assertEqual( t.getValues(), [m2]) 
        t.setValues([[0,0,1],[1,0,0]])
        self.assertEqual( t.getValues(), [m2,m])
        t.setValue([0,0,1])
        self.assertEqual( t.getValues(), [m2])       
        
    def testMFVec4f(self):
        """check setValue(s) for MFVec4f"""
        t = SoMFVec4f()
        s = SoMFVec4f()
        m = SbVec4f(1,0,0,0)
        m2 = SbVec4f(0,0,1,0)
        t.setValues([m])
        self.assertEqual( t.getValues(), [m])
        t.setValues(2,[m2,m2])
        self.assertEqual( t.getValues()[2:4],[m2,m2])
        t.setValues(1,1,[m2,m])
        self.assertEqual( t.getValues(), [m,m2,m2,m2])
        t.setValue(s)
        self.assertEqual( t.getValues(), s.getValues())
        t.setValue(m2)
        self.assertEqual( t.getValues(), [m2])
        t.setValues([])
        self.assertEqual( t.getValues(), [m2]) 
        t.setValues([[0,0,1,0],[1,0,0,0]])
        self.assertEqual( t.getValues(), [m2,m])
        t.setValue([0,0,1,0])
        self.assertEqual( t.getValues(), [m2])        
        

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
        """SoBaseList.get should return downcast type"""
        l = SoBaseList()
        c = SoCone()
        l.append(c)
        self.assert_(isinstance(l.get(0), SoCone))
        
    def testItem(self):
        """SoBaseList[] should return downcast type"""
        l = SoBaseList()
        c = SoCone()
        l.append(c)
        self.assert_(isinstance(l[0], SoCone))
        
class SoNodeListMethods(unittest.TestCase):
    """tests various methods of SoNodeList"""
    def testGet(self):
        """SoNodeList.get should return downcast type"""
        l = SoNodeList()
        c = SoCone()
        l.append(c)
        self.assert_(isinstance(l.get(0), SoCone))
        
    def testItem(self):
        """SoNodeList[] should return downcast type"""
        l = SoNodeList()
        c = SoCone()
        l.append(c)
        self.assert_(isinstance(l[0], SoCone))

class SoFieldListMethods(unittest.TestCase):
    """tests various methods of SoFieldList"""
    def testGet(self):
        """SoFieldList.get should return downcast type"""
        l = SoFieldList()
        f = SoSFBool()
        l.append(f)
        self.assert_(isinstance(l.get(0), SoSFBool))
        
    def testItem(self):
        """SoFieldList[] should return downcast type"""
        l = SoFieldList()
        f = SoSFBool()
        l.append(f)
        self.assert_(isinstance(l[0], SoSFBool))
        
if __name__ == "__main__":
    SoDB.init()
    unittest.main()
