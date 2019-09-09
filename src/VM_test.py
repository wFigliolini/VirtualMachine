'''
File containing Tests for the virtual machine
'''

import VirtualMachine as VM
import pytest


# Base cases: int, add, and multiply
def test_0():
    result = 5
    testProg = VM.JProg(VM.JInt(result))
    assert testProg.run() == result


def test_1():
    leftIn = 5
    rightIn = 10
    result = leftIn + rightIn
    testProg = VM.JProg(VM.JAdd(VM.JInt(leftIn), VM.JInt(rightIn)))
    assert testProg.run() == result


def test_2():
    leftIn = 5
    rightIn = 10
    result = leftIn * rightIn
    testProg = VM.JProg(VM.JMult(VM.JInt(leftIn), VM.JInt(rightIn)))
    assert testProg.run() == result


# Recursive cases
def test_3():
    expr = VM.JMult(VM.JInt(5), VM.JInt(10))
    testProg = VM.JProg(VM.JAdd(expr, VM.JInt(2)))
    assert testProg.run() == 52


def test_4():
    expr1 = VM.JInt(10)
    expr2 = VM.JAdd(VM.JInt(20), VM.JInt(15))
    testProg = VM.JProg(VM.JMult(expr1, expr2))
    assert testProg.run() == 350


def test_5():
    expr1 = VM.JMult(VM.JInt(5), VM.JInt(10))
    expr2 = VM.JAdd(VM.JInt(20), VM.JInt(15))
    testProg = VM.JProg(VM.JMult(expr1, expr2))
    assert testProg.run() == 1750


# Exception Tests
# No argument tests
def test_binary_No_Arg():
    with pytest.raises(TypeError):
        VM.JAdd()


def test_unit_No_Arg():
    with pytest.raises(TypeError):
        VM.JInt()


# Wrong Type Tests
def test_binary_Wrong_Arg():
    with pytest.raises(TypeError):
        VM.JAdd(7, 'x')


def test_unit_Wrong_Arg():
    with pytest.raises(TypeError):
        VM.JInt('x')
