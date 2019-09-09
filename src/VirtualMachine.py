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
        self.val = val

    def strOut(self):
        return str(self.val)


class JBinary(JExpr, metaclass=abc.ABCMeta):
    def __init__(self, l, r):
        self.left = l
        self.right = r


class JInt(JUnit):
    pass


class JAdd(JBinary):
    def strOut(self):
        lString = self.left.strOut()
        rString = self.right.strOut()
        outString = "( " + lString + " + " + rString + " )"
        return outString


class JMult(JBinary):
    def strOut(self):
        lString = self.left.strOut()
        rString = self.right.strOut()
        outString = "( " + lString + " * " + rString + " )"
        return outString
