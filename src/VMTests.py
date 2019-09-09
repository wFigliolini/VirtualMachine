'''
File containing Tests for the virtual machine
'''

import VirtualMachine as VM
import pytest


class J0Tests(object):
    # Base cases: int, add, and multiply
    def test0(self):
        result = 5
        testProg = VM.JProg(VM.JInt(result))
        assert testProg.run() == result

    def test1(self):
        leftIn = 5
        rightIn = 10
        result = leftIn + rightIn
        testProg = VM.JProg(VM.JAdd(VM.JInt(leftIn), VM.JInt(rightIn)))
        assert testProg.run() == result

    def test2(self):
        leftIn = 5
        rightIn = 10
        result = leftIn * rightIn
        testProg = VM.JProg(VM.JMult(VM.JInt(leftIn), VM.JInt(rightIn)))
        assert testProg.run() == result

    # Recursive cases
    def test3(self):
        expr = VM.JMult(VM.JInt(5), VM.JInt(10))
        testProg = VM.JProg(VM.JAdd(expr, VM.JInt(2)))
        assert testProg.run() == 100

    def test4(self):
        expr1 = VM.JInt(10)
        expr2 = VM.JAdd(VM.JInt(20), VM.JInt(15))
        testProg = VM.JProg(VM.JMult(expr1, expr2))
        assert testProg.run() == 350

    def test5(self):
        expr1 = VM.JMult(VM.JInt(5), VM.JInt(10))
        expr2 = VM.JAdd(VM.JInt(20), VM.JInt(15))
        testProg = VM.JProg(VM.JMult(expr1, expr2))
        assert testProg.run() == 1750
    
    # Exception Tests
    # No argument tests
    def binaryNoArg(self):
        with pytest.raises(TypeError):
            VM.JAdd()

    def unitNoArg(self):
        with pytest.raises(TypeError):
            VM.JInt()
    # Wrong Type Tests
    def binaryNoArg(self):
        with pytest.raises(TypeError):
            VM.JAdd(7, 'x')

    def unitNoArg(self):
        with pytest.raises(TypeError):
            VM.JInt('x')
