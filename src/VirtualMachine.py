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

    def findRedex(self):
        raise NotImplemented()

    def tiny(self):
        raise NotImplemented()

    def isRunnable(self):
        return True

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

    def findRedex(self):
        raise Exception("Units are not valid Redexes")
    
    def tiny(self):
        raise Exception("Tiny should not be called on Unit")
    
    def isRunnable(self):
        raise Exception("isRunnable should not be called on Unit")

class JInt(JUnit):
    pass


class JBool(JUnit):
    pass

class JPrim(JExpr):
    def __init__(self, prim):
        self.prim = prim
        
    def strOut(self):
        return self.prim
    
    def run(self):
        return PrimFunc[self.prim]
    
    def plug(self):
        raise Exception("Plug should never be called on Prim")

    def isVal(self):
        return True

    def findRedex(self):
        raise Exception("Prims are not valid Redexes")
    
    def tiny(self):
        raise Exception("Tiny should not be called on Prim")
    
    def isRunnable(self):
        raise Exception("isRunnable should not be called on Prim")


def Add(args: list):
    while len(args) < 3:
        args.append(JInt(Identities[args[0].prim]))
    result = 0
    print(args)
    for arg in args[1:]:
        result += arg.run().val
    return JInt(result)


def Sub(args: list):
    while len(args) < 3:
        args.insert(1, JInt(Identities[args[0].prim]))
    result = args[1].run().val
    for arg in args[2:]:
        result -= arg.run().val
    return JInt(result)


def Mult(args: list):
    while len(args) < 3:
        args.append(JInt(Identities[args[0].prim]))
    result = 1
    print(args)
    for arg in args[1:]:
        result *= arg.run().val
    return JInt(result)


def Div(args: list):
    while len(args) < 3:
        args.insert(1, JInt(Identities[args[0].prim]))
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
            op = self.JL[0].run()
            JL = self.JL
            result = op(JL)
            return result
        else:
            return self.JL[0]

    def strOut(self):
        out = "( "
        for arg in self.JL:
            if isinstance(arg, str):
                out = out + arg + " "
                continue
            out = out + arg.strOut() + " "
        out += " )"
        return out

    def isContext(self):
        result = False
        for expr in self.JL:
            if expr is None:
                return True
            elif expr in Prims:
                continue
            else:
                result = expr.isContext()
                if result:
                    return result

    def plug(self, je):
        for i, e in enumerate(self.JL):
            if e is None:
                self.JL[i] = je
                return
            elif e in Prims:
                continue
            elif e.isContext():
                e.plug(je)
                return

    def findRedex(self):
        result = None
        for i, e in enumerate(self.JL):
            if e.isVal():
                continue
            elif e.isRunnable():
                result = e
                self.JL[i] = None
                return result
            else:
                result = e.findRedex()
                return result

    def tiny(self):
        if isinstance(self.JL[0], JPrim):
            op = self.JL[0].run()
            JL = self.JL
            result = op(JL)
            return result
        else:
            return self.JL[0]        
    
    def isRunnable(self):
        result = True
        for expr in self.JL:
            if not expr.isVal():
                result = False
                break
        return result


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
        out = "( If " + self.JL[0].strOut() + " " + self.JL[1].strOut() + " " + self.JL[2].strOut() + " )"
        return out

    def isContext(self):
        result = False
        for expr in self.JL:
            if expr is None:
                return True
            else:
                result = expr.isContext()
                if result:
                    break
        return result

    def plug(self, je):
        for i, e in enumerate(self.JL):
            if e is None:
                self.JL[i] = je
                return
            elif e.isContext():
                e.plug(je)
                return

    def findRedex(self):
        result = None
        for i, e in enumerate(self.JL):
            if e.isVal():
                continue
            elif e.isRunnable():
                result = e
                self.JL[i] = None
                return result
            else:
                result = e.findRedex()
                return result
        

    def tiny(self):
        if self.JL[0].val:
            return self.JL[1]
        else:
            return self.JL[2]

    def isRunnable(self):
        result = True
        for expr in self.JL:
            if not expr.isVal():
                result = False
                break
        return result
        #return self.JL[0].isVal()

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
    jexprs = mkList(se, JPrim(op))
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


# Small step interpreter functions
def small(je):
    e = je.findRedex()
    if e is None:
        return je.tiny()
    e = e.tiny()
    je.plug(e)
    return je

def large(je):
    while not je.isVal():
        je = small(je)
    return je
