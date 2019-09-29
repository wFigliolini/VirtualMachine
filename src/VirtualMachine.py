'''
Main file, containing J language defitions and High Level Functionallity
'''

import abc
import string
from collections import deque


Identities = {"+" : 0, "*" : 1, "-" : 0, "/" : 1}
Prims = ["+", "-","*", "/"]

"""
Converts strings into SExprs
will remove opening ( from string and assumes
that it was removed from previous call
"""
class SExpr(list):
    def __init__(self, se):
        if isinstance(se, str):
            listSE = se.split()
            if listSE[0] == "(":
                listSE.pop(0)
        elif isinstance(se, list):
            listSE = se
        else:
            raise TypeError()
        while listSE:
            next = listSE[0]
            listSE.pop(0)
            if next == "(":
                #New Function, need to recurse for new SExpr
                self.append(SExpr(listSE))
            elif next == ")":
                #Function Complete, return new null-terminated SExpr
                self.append(None)
                return
            else:
                self.append(next)
        self.append(None)


class JExpr(object, metaclass=abc.ABCMeta):
    # Abstract Method for execution
    @abc.abstractmethod
    def run(self):
        raise NotImplemented()

    # Abstract method for printer
    @abc.abstractmethod
    def strOut(self):
        raise NotImplemented()


class JUnit(JExpr, metaclass=abc.ABCMeta):
    def __init__(self, val):
        if isinstance(val, int):
            self.val = val
        else:
            raise TypeError()

    def strOut(self):
        return str(self.val)

    def run(self):
        return self.val


class JBinary(JExpr):
    def __init__(self, op, l, r):
        if isinstance(l, JExpr) and isinstance(r, JExpr):
            self.op = op
            self.left = l
            self.right = r
        else:
            raise TypeError()

    def run(self):
        leftRes = self.left.run()
        rightRes = self.right.run()
        if self.op == "+":
            return leftRes + rightRes
        elif self.op == "*":
            return leftRes * rightRes
        else:
            raise Exception("Invalid Operator")

    def strOut(self):
        lString = self.left.strOut()
        rString = self.right.strOut()
        outString = "(" + self.op + " " + lString + " " + rString + " )"
        return outString


class JInt(JUnit):
    pass


class JProg(object):
    def __init__(self, expr):
        self.expr = expr

    def run(self):
        return self.expr.run()

    def strOut(self):
        return self.expr.strOut()

"""
Removes the operator from the start of the SExpr
SExprs are lists of the form (op, SExpr|str, ..., None)
"""
def desugar(se) -> JExpr:
    """
    could be clean up, but needs the second if statement for
    Cases for ( int )
    """
    if isinstance(se, str):
        return JInt(int(se))
    op = se[0]
    if op not in Prims:
        return JInt(int(se[0]))
    if op == "-":
        #unary case (op SExpr None)
        if len(se) == 3:
            r = desugar(se[1])
            return JBinary("*", JInt(-1), r)
        #binary case (op SExpr SExpr None)
        if len(se) == 4:
            l = desugar(se[1])
            r = desugar(["-"] + [se[2]] + [None])
            return JBinary("+", l, r)
    jexpr = None
    for exp in reversed(se):
        if exp == op:
            return jexpr
        if exp is None:
            jexpr = JInt(Identities[op])
            continue
        l = desugar(exp)
        jexpr = JBinary(op, l, jexpr)
