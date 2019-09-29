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
#Bool Base Cases
def test_J1_0():
    testString = "( True )"
    testfunc(testString, True)


def test_J1_1():
    testString = "( False )"
    testfunc(testString, False)


#Comparisons
def test_J1_2():
    testString = "( < 5 3 )"
    testfunc(testString, False)


def test_J1_3():
    testString = "( <= 6 6 )"
    testfunc(testString, True)


def test_J1_4():
    testString = "( == 7 7 )"
    testfunc(testString, True)


def test_J1_5():
    testString = "( >= 5 6 )"
    testfunc(testString, False)


def test_J1_6():
    testString = "( > 6 5 )"
    testfunc(testString, True)


#If checking
def test_J1_7():
    testString = "( If ( True ) ( 5 ) ( 6 ) )"
    testfunc(testString, 5)


def test_J1_8():
    testString = "( If ( False ) ( 5 ) ( 6 ) )"
    testfunc(testString, 6)

#If Execution Order
def test_J1_9():
    testString = "( If ( > 6 7 ) ( 5 ) ( 6 ) )"
    testfunc(testString, 6)


def test_J1_10():
    testString = "( If ( < 6 7 ) ( 5 ) ( 6 ) )"
    testfunc(testString, 5)


def test_J1_11():
    testString = "( If ( == 6 6 ) ( 5 ) ( 6 ) )" 
    testfunc(testString, 5)

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
    print(sexpr)
    testProg = VM.desugar(sexpr)
    actual = testProg.run()
    assert actual.val == output
