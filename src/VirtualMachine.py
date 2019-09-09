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
    def print(self):
        raise NotImplemented()


class JUnit(JExpr, metaclass=abc.ABCMeta):
    def __init__(self, val):
        self.val = val


class JBinary(JExpr, metaclass=abc.ABCMeta):
    def __init__(self, l, r):
        self.left = l
        self.right = r


class JInt(JUnit):
    pass


class JAdd(JBinary):
    pass


class JMult(JBinary):
    pass
