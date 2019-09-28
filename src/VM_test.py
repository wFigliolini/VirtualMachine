'''
File containing Tests for the virtual machine
'''

import VirtualMachine as VM
import pytest


# Base cases: int, add, and multiply
def test_0():
    result = 5
    testString = "( 5 )"
    testfunc(testString, result)


def test_1():
    leftIn = 5
    rightIn = 10
    result = leftIn + rightIn
    testString = "( + 5 10 )"
    testfunc(testString, result)


def test_2():
    leftIn = 5
    rightIn = 10
    result = leftIn * rightIn
    testString = "( * 5 10 )"
    testfunc(testString, result)


# Recursive cases
def test_3():
    testString = "( + ( * 5 10 ) 2 )"
    testfunc(testString, 52)


def test_4():
    testString = "( * 10 ( + 20 15 ) )"
    testfunc(testString, 350)


def test_5():
    testString = "( * ( * 5 10 ) ( + 20 15 )"
    testfunc(testString, 1750)


def test_6():
    testString = "( - 10 )"
    testfunc(testString, -10)


def test_7():
    testString = "( - 10 5 )"
    testfunc(testString, 5)


def test_8():
    testString = "( + )"
    testfunc(testString, 0)


def test_9():
    testString = "( * )"
    testfunc(testString, 1)


def test_10():
    testString = "( + 5 )"
    testfunc(testString, 5)


def test_11():
    testString = "( + 5 10 15 )" 
    testfunc(testString, 30)


# Exception Tests
# No argument tests
def test_binary_No_Arg():
    with pytest.raises(TypeError):
        VM.JBinary()


def test_unit_No_Arg():
    with pytest.raises(TypeError):
        VM.JInt()


# Wrong Type Tests
def test_binary_Wrong_Arg():
    with pytest.raises(TypeError):
        VM.JBinary("+", 7, 'x')


def test_unit_Wrong_Arg():
    with pytest.raises(TypeError):
        VM.JInt('x')

def testfunc(input,output):
    sexpr = VM.SExpr(input)
    #print(sexpr)
    testProg = VM.desugar(sexpr)
    assert testProg.run() == output
