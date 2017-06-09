import unittest
from PySide import QtCore
import shiboken

class ShibokenTests(unittest.TestCase):
    """shiboken_64bit_test.py"""
    def testAdresses(self):
        q = QtCore.QObject()
        ptr = shiboken.getCppPointer(q)
        print("CppPointer to an instance of PySide.QtCore.QObject = 0x%016X" % ptr[0])

        # None of the following is expected to raise an OverflowError on 64-bit systems
        shiboken.wrapInstance(0xFFFFFFFF, QtCore.QObject)  # largest 32-bit address
        shiboken.wrapInstance(0xFFFFFFF, QtCore.QObject) # a regular, slightly smaller 32-bit address
        shiboken.wrapInstance(0x100000000, QtCore.QObject) # an actual 64-bit address (> 4 GB, the first non 32-bit address)
        shiboken.wrapInstance(0xFFFFFFFFFFFFFFFF, QtCore.QObject) # largest 64-bit address

if __name__ == "__main__":
    unittest.main(verbosity=4)