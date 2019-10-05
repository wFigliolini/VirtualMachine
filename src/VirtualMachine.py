'''
Main file, containing J language defitions and High Level Functionallity
'''

import abc
import string
from collections import deque


Identities = {"+" : 0, "*" : 1, "-" : 0, "/" : 1, "<" : 0, "<=" : 0, "==" : 0, ">=" : 0, ">" : 0}
Prims = ["+", "-", "*", "/", "<", "<=", "==", ">=", ">"]



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
        elif isinstance(val, bool):
            self.val = val
        else:
            raise TypeError()

    def strOut(self):
        return str(self.val)

    def run(self):
        return self


class JInt(JUnit):
    pass

class JBool(JUnit):
    pass

def Add(args: tuple):
    lnum = args[1].run()
    rnum = args[2].run()
    return JInt(lnum.val + rnum.val)

def Sub(args: tuple):
    lnum = args[1].run()
    rnum = args[2].run()
    return JInt(lnum.val - rnum.val)

def Mult(args: tuple):
    lnum = args[1].run()
    rnum = args[2].run()
    return JInt(lnum.val * rnum.val)

def Div(args: tuple):
    lnum = args[1].run()
    rnum = args[2].run()
    return JInt(lnum.val / rnum.val)

def LT(args: tuple):
    lnum = args[1].run()
    rnum = args[2].run()
    return JBool(lnum.val < rnum.val)

def LTE(args: tuple):
    lnum = args[1].run()
    rnum = args[2].run()
    return JBool(lnum.val <= rnum.val)

def EQ(args: tuple):
    lnum = args[1].run()
    rnum = args[2].run()
    return JBool(lnum.val == rnum.val)

def GTE(args: tuple):
    lnum = args[1].run()
    rnum = args[2].run()
    return JBool(lnum.val >= rnum.val)

def GT(args: tuple):
    lnum = args[1].run()
    rnum = args[2].run()
    return JBool(lnum.val > rnum.val)

PrimFunc = {"+": Add, "-": Sub, "*": Mult, "/": Div, "<": GT, "<=": LTE, "==" : EQ, ">=" : GTE, ">" : GT }

class JApp(JExpr):
    def __init__(self, *args):
        self.args = args
    def run(self):
        if self.args[0] in Prims:
            op = self.args[0]
            args = self.args
            result = PrimFunc[op](args)
            return result
        else:
            return self.args[0]
    def strOut(self):
        out = "( "
        for arg in self.args:
            if isinstance(arg, str):
                out = out + arg + " "
            out += arg.strOut()
        out += " )"
        return out

class JIf(JExpr):
    def __init__(self, JC, JT, JF):
        self.JC = JC
        self.JT = JT
        self.JF = JF
    def run(self):
        return None
    def strOut(self):
        out = "( If " + self.JC.strOut() + " " + self.JT.strOut() + " " + self.JF.strOut() + " )"
        return out


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
        outString = "( " + self.op + " " + lString + " " + rString + " )"
        return outString



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

"""
Removes the operator from the start of the SExpr
SExprs are lists of the form (op, SExpr|str, ..., None)
"""
def desugar(se) -> JExpr:
    """
    could be clean up, but needs the second if statement for
    Cases of ( int  ) or ( Bool )
    """
    if isinstance(se, str):
        if se == "True":
            return JBool(True)
        elif se == "False":
            return JBool(False)
        return JInt(int(se))
    op = se[0]
    if op == "If":
        temp = list()
        for exp in se[1:]:
            if exp is None: break
            jexpr = desugar(exp)
            temp.append(jexpr)
        return JIf(temp[0], temp[1], temp[2])
    if op not in Prims:
        return JInt(int(se[0]))
    jexpr = None
    for exp in reversed(se):
        if exp == op:
            break
        if exp is None:
            jexpr = JInt(Identities[op])
            continue
        l = desugar(exp)
        jexpr = JApp(op, l, jexpr)
