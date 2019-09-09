'''
Main file, containing J language defitions and High Level Functionallity
'''

import abc


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
