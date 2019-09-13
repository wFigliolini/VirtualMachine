'''
Main file, containing J language defitions and High Level Functionallity
'''

import abc
import string
from collections import deque


class cons(object):
    def __init__(self, l: str, r: cons = None):
        first = l
        second = r


def isCons(se):
    return isinstance(se, cons)


def len(se):
    if se is None:
        return 0
    elif isCons(se):
        return 1+len(se)
    else:
        raise TypeError()


class SExpr(cons):
    def __init__(self, se: str):
        terms = se.split()
        self.first = terms[0]
        terms.remove(0)
        curr = self
        for term in terms:
            curr.second = cons(term)
            curr = curr.second


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


class JBinary(JExpr, metaclass=abc.ABCMeta):
    def __init__(self, l, r):
        if isinstance(l, JExpr) and isinstance(r, JExpr):
            self.left = l
            self.right = r
        else:
            raise TypeError()


class JInt(JUnit):
    pass


class JAdd(JBinary):
    def strOut(self):
        lString = self.left.strOut()
        rString = self.right.strOut()
        outString = "( " + lString + " + " + rString + " )"
        return outString

    def run(self):
        leftRes = self.left.run()
        rightRes = self.right.run()
        return leftRes + rightRes


class JMult(JBinary):
    def strOut(self):
        lString = self.left.strOut()
        rString = self.right.strOut()
        outString = "( " + lString + " * " + rString + " )"
        return outString

    def run(self):
        leftRes = self.left.run()
        rightRes = self.right.run()
        return leftRes * rightRes


class JProg(object):
    def __init__(self, expr):
        self.expr = expr

    def run(self):
        return self.expr.run()

    def strOut(self):
        return self.expr.strOut()


def desugar(se: SExpr) -> JExpr:
    pass
