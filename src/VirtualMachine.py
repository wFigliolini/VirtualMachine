'''
Main file, containing J language defitions and High Level Functionallity
'''

import abc
import string
import os
import subprocess
from collections import deque


Identities = {"+": 0, "*": 1, "-": 0, "/": 1, "<": 0, "<=": 0, "==": 0,
              ">=": 0, ">": 0}
Prims = ["+", "-", "*", "/", "<", "<=", "==", ">=", ">"]
PrimDict = {"+": "ADD", "-": "SUB", "*": "MULT", "/": "DIV", "<": "LT",
            "<=": "LTE", "==": "EQ", ">=": "GTE", ">": "GT"}


def genName():
    s = "x" + str(genName.i)
    genName.i += 1
    return s


genName.i = 0


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

    def getContext(self):
        raise NotImplemented()

    def containsNone(self):
        return False

    def moveContext(self, expr):
        raise NotImplemented()

    def createContext(self):
        raise NotImplemented()

    def make(self, BodyList, name):
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

    def plug(self, je):
        raise Exception("Plug should never be called on Unit")

    def isVal(self):
        return True

    def findRedex(self):
        raise Exception("Units are not valid Redexes")

    def tiny(self):
        raise Exception("Tiny should not be called on Unit")

    def isRunnable(self):
        raise Exception("isRunnable should not be called on Unit")

    def getContext(self):
        raise Exception("getContext should not be called on Unit")

    def moveContext(self, expr):
        raise Exception("moveContext should not be called on Unit")

    def createContext(self, expr):
        raise Exception("createContext should not be called on Prim")


class JInt(JUnit):
    def make(self, BodyList, name):
        BodyList.append("num* {} = (num*) malloc(sizeof(num));\n".format(name))
        BodyList.append("{}->m.tag = NUM;\n".format(name))
        BodyList.append("{}->n = {!s};\n".format(name, self.val))


class JBool(JUnit):
    def make(self, BodyList, name):
        BodyList.append("bool* {} = (bool*) malloc(sizeof(bool));\n".format(name))
        BodyList.append("{}->m.tag = BOOL;\n".format(name))
        if self.val:
            x = 1
        else:
            x = 0
        BodyList.append("{}->n = {!s};\n".format(name, x))


class JPrim(JExpr):
    def __init__(self, prim):
        self.prim = prim

    def strOut(self):
        return self.prim

    def run(self):
        return PrimFunc[self.prim]

    def plug(self, je):
        raise Exception("Plug should never be called on Prim")

    def isVal(self):
        return True

    def findRedex(self):
        raise Exception("Prims are not valid Redexes")

    def tiny(self):
        raise Exception("Tiny should not be called on Prim")

    def isRunnable(self):
        raise Exception("isRunnable should not be called on Prim")

    def getContext(self):
        raise Exception("getContext should not be called on Prim")

    def moveContext(self, expr):
        raise Exception("moveContext should not be called on Prim")

    def createContext(self, expr):
        raise Exception("createContext should not be called on Prim")

    def make(self, BodyList, name):
        BodyList.append("prim* {} = (prim*) malloc(sizeof(prim));\n".format(name))
        BodyList.append("{}->m.tag = PRIM;\n".format(name))
        BodyList.append("{}->p = {};\n".format(name, PrimDict[self.prim]))


def Add(args: list):
    while len(args) < 3:
        args.append(JInt(Identities[args[0].prim]))
    result = 0
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


PrimFunc = {"+": Add, "-": Sub, "*": Mult, "/": Div, "<=": LTE, ">=": GTE,
            "<": LT,  "==": EQ,  ">": GT}


class JApp(JExpr):
    def __init__(self, JL: list):
        self.JL = JL

    def run(self):
        if isinstance(self.JL[0], JPrim):
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
        for i, expr in enumerate(self.JL):
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

    def getContext(self):
        for i, e in enumerate(self.JL):
            if e.isVal():
                continue
            if e.containsNone():
                result = e
                self.JL[i] = None
                return result
            elif e.isContext():
                result = e.getContext()
                return result
        raise Exception("getContext called on non-context App")

    def containsNone(self):
        return not (self.JL.count(None) == 0)

    def moveContext(self, expr):
        i = self.JL.index(None)
        self.JL[i] = expr
        if (i+1) == len(self.JL):
            result = self.tiny()
        else:
            result = self.JL[i+1]
            self.JL[i+1] = None
        return result

    def createContext(self):
        expr = self.JL[0]
        self.JL[0] = None
        return expr

    def make(self, BodyList, name):
        BodyList.append("app* {0} = (app*) malloc(sizeof(app));\n".format(name))
        BodyList.append("{0}->m.tag = APP;\n".format(name))
        n = genName()
        self.JL[0].make(BodyList, n)
        BodyList.append("{0}->f = {1};\n".format(name, n))
        BodyList.append("{0}->args = (exprlist*) malloc(sizeof(exprlist));\n".format(name))
        tempname = genName()
        BodyList.append("exprlist* {0} = {1}->args;\n".format(tempname, name))
        for i, e in enumerate(self.JL[1:]):
            n = genName()
            e.make(BodyList, n)
            BodyList.append("{0}->e = {1};\n".format(tempname, n))
            if i+1 != len(self.JL):
                BodyList.append("{0}->l = (exprlist*) malloc(sizeof(exprlist));\n".format(tempname))
                BodyList.append("{0} = {0}->l;\n".format(tempname))
        BodyList.append("{0}->l = NULL;\n".format(tempname))


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
        if self.JL[0] is None:
            return True
        else:
            return self.JL[0].isContext()

    def plug(self, je):
        if self.JL[0] is None:
            self.JL[0] = je
        else:
            self.JL[0].plug(je)

    def findRedex(self):
        if self.JL[0].isRunnable():
            result = self.JL[0]
            self.JL[0] = None
            return result
        else:
            result = self.JL[0].findRedex()
            return result

    def tiny(self):
        if self.JL[0].val:
            return self.JL[1]
        else:
            return self.JL[2]

    def isRunnable(self):
        return self.JL[0].isVal()

    def getContext(self):
        if self.JL[0].containsNone():
            result = self.JL[0]
            self.JL[0] = None
            return result
        elif self.JL[0].isContext():
            result = self.JL[0].getContext()
            return result
        else:
            raise Exception("getContext called on non-context If")

    def containsNone(self):
        return self.JL[0] is None

    def moveContext(self, expr):
        self.JL[0] = expr
        result = self.tiny()
        return result

    def createContext(self):
        expr = self.JL[0]
        self.JL[0] = None
        return expr

    def make(self, BodyList, name):
        BodyList.append("jif* {} = (jif*) malloc(sizeof(jif));\n".format(name))
        BodyList.append("{}->m.tag = IF;\n".format(name))
        n = genName()
        self.JL[0].make(BodyList, n)
        BodyList.append("{}->c = {};\n".format(name, n))
        n = genName()
        self.JL[1].make(BodyList, n)
        BodyList.append("{}->t = {};\n".format(name, n))
        n = genName()
        self.JL[2].make(BodyList, n)
        BodyList.append("{}->f = {};\n".format(name, n))


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
    if je.isRunnable():
        return je.tiny()
    e = je.findRedex()
    e = e.tiny()
    je.plug(e)
    return je


def large(je):
    while not je.isVal():
        je = small(je)
    return je


def inject(je):
    return (je, None)


def extract(st):
    return st[0]


def getContext(con):
    if con.containsNone():
        newCon = con
        con = None
        return newCon
    else:
        newCon = con.getContext()
        return newCon


def addContext(expr, con):
    if con is None:
        con = expr
    else:
        con.plug(expr)
    return con


def moveContext(expr, con):
    resultExpr = con.moveContext(expr)
    if not con.isContext():
        con = None
    return (resultExpr, con)


def CC0(st):
    # variables for tracking the state of the machine
    exp = st[0]
    con = st[1]

    while True:
        if con is None:
            # final state
            if exp.isVal():
                return (exp, con)
            # intial state is the same for both Apps and Ifs
            else:
                temp = exp.JL[0]
                exp.JL[0] = None
                con = addContext(exp, con)
                exp = temp
        else:
            if exp.isVal():
                currCon = getContext(con)
                exp, currCon = moveContext(exp, currCon)
                if (currCon is not None) and con != currCon:
                    con = addContext(currCon, con)
                if not con.isContext():
                    con = None
            else:
                temp = exp.createContext()
                con = addContext(exp, con)
                exp = temp


def CCRun(je):
    return extract(CC0(inject(je)))


def makeBody(file, je):
    BodyList = ["#include \"JVM.h\"\n","int main(int arg, char* argv[]){\n"]
    je.make(BodyList, genName())
    BodyList.append("expr* e = x0;\n")
    BodyList.append("num* r = (num*) malloc(sizeof(num));\n")
    BodyList.append("expr** rl = &r;\n")
    BodyList.append("VM(e, rl);\n")
    BodyList.append("if(r->m.tag == NUM){\n")
    BodyList.append("\tnum* result1 = (num*) r;\n")
    BodyList.append("\tprintf(\"%i\", result1->n); }\n")
    BodyList.append("else if(r->m.tag == BOOL){\n")
    BodyList.append("\tbool* result2 = (bool*) r;\n")
    BodyList.append("\tprintf(\"%s\", result2->n ? \"True\" : \"False\");}\n")
    BodyList.append("\n")
    BodyList.append("return 0;\n")
    BodyList.append("}")
    file.writelines(BodyList)


def print(je):
    fileout = open("JVMsample.c", "w")
    makeBody(fileout, je)


def CKrun(je):
    fileout = open(".JRun.c", "w")
    makeBody(fileout, je)
    os.system("gcc -c JVM.c -o JVM.o")
    os.system("gcc -o .a.out .JRun.c JVM.o")
    result = subprocess.check_output("./.a.out", shell=True)
    fileout.close()
    os.remove(".JRun.c")
    os.remove(".JRun.o")
    os.remove(".a.out")
    return result
