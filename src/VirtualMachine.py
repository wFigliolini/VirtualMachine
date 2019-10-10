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

    def isContext(self):
        return False

    def plug(self, je):
        raise NotImplemented()

    def isVal(self):
        return False


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

    def plug(self):
        raise Exception("Plug should never be called on Unit")

    def isVal(self):
        return True


class JInt(JUnit):
    pass


class JBool(JUnit):
    pass


def Add(args: list):
    while len(args) < 3:
        args.append(JInt(Identities[args[0]]))
    result = 0
    for arg in args[1:]:
        result += arg.run().val
    return JInt(result)


def Sub(args: list):
    while len(args) < 3:
        args.insert(1, JInt(Identities[args[0]]))
    result = args[1].run().val
    for arg in args[2:]:
        result -= arg.run().val
    return JInt(result)


def Mult(args: list):
    while len(args) < 3:
        args.append(JInt(Identities[args[0]]))
    result = 1
    for arg in args[1:]:
        result *= arg.run().val
    return JInt(result)


def Div(args: list):
    while len(args) < 3:
        args.insert(1, JInt(Identities[args[0]]))
    result = args[1].run().val
    for arg in args[2:]:
        result /= arg.run().val
    return JInt(result)


def LT(args: list):
    print(args)
    while len(args) < 3:
        args.append(0)
    lnum = args[1].run()
    rnum = args[2].run()
    result = lnum.val < rnum.val
    return JBool(result)


def LTE(args: list):
    while len(args) < 3:
        args.append(0)
    lnum = args[1].run()
    rnum = args[2].run()
    result = lnum.val <= rnum.val
    return JBool(result)


def EQ(args: list):
    print(args)
    while len(args) < 3:
        args.append(0)
    lnum = args[1].run()
    rnum = args[2].run()
    result = lnum.val == rnum.val
    return JBool(result)


def GTE(args: list):
    while len(args) < 3:
        args.append(0)
    lnum = args[1].run()
    rnum = args[2].run()
    result = lnum.val >= rnum.val
    return JBool(result)


def GT(args: list):
    while len(args) < 3:
        args.append(0)
    lnum = args[1].run()
    rnum = args[2].run()
    result = lnum.val > rnum.val
    return JBool(result)


PrimFunc = {"+": Add, "-": Sub, "*": Mult, "/": Div, "<=": LTE, ">=" : GTE, "<": LT,  "==" : EQ,  ">" : GT }


class JApp(JExpr):
    def __init__(self, JL: list):
        self.JL = JL

    def run(self):
        if self.JL[0] in Prims:
            op = self.JL[0]
            JL = self.JL
            result = PrimFunc[op](JL)
            return result
        else:
            return self.JL[0]

    def strOut(self):
        out = "( "
        for arg in self.JL:
            if isinstance(arg, str):
                out = out + arg + " "
            out += arg.strOut()
        out += " )"
        return out

    def isContext(self):
        result = False
        for expr in self.JL:
            if expr is None:
                return True
            else:
                result = expr.isContext()
                if result:
                    return result

    def plug(self, je):
        for i, e in enumerate(self.JL):
            if e is None:
                self.JL[i] = je
                return
            elif e.isContext():
                e.plug(je)
                return


class JIf(JExpr):
    def __init__(self, JL):
        self.JL = JL

    def run(self):
        c = self.JL[0].run()
        if c.val:
            return self.JL[1].run()
        else:
            return self.JL[2].run()

    def strOut(self):
        out = "( If " + self.JL[0] + " " + self.JL[1] + " " + self.JL[2] + " )"
        return out

    def isContext(self):
        result = False
        for expr in self.JL:
            if expr is None:
                return True
            else:
                result = expr.isContext()
                if result:
                    return result

    def plug(self, je):
        for i, e in enumerate(self.JL):
            if e is None:
                self.JL[i] = je
                return
            elif e.isContext():
                e.plug(je)
                return


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
                # New Function, need to recurse for new SExpr
                self.append(SExpr(listSE))
            elif next == ")":
                # Function Complete, return new null-terminated SExpr
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
        return fixdesugar(se)
    op = se[0]
    if op == "If":
        temp = mkList(se)
        return JIf(temp[:3])
    if op not in Prims:
        return fixdesugar(se[0])
    jexprs = mkList(se, op)
    return JApp(jexprs)

# desugar helper functions


def fixdesugar(se):
    if se == "True":
        return JBool(True)
    elif se == "False":
        return JBool(False)
    return JInt(int(se))


def mkList(se, start=None):
    l = list()
    if start is not None:
        l.append(start)
    for exp in se[1:]:
        if exp is None:
            break
        jexpr = desugar(exp)
        l.append(jexpr)
    return l


"""
Using None to denote Holes in already existing data structures
As None is not a valid JExpr, and should never appear in compilation
"""


