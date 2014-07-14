#!/usr/bin/env python

import os
import sys
import argparse

from pyparsing import (
    Literal, Combine,
    Word, Optional,
    nums, alphas,alphanums,
    Group, OneOrMore,
    stringEnd,stringStart
    )

from PathAction import PathAction

class PathParser(object):
    """
    This class uses the pyparsing module. Refer to that module for details
    about how it works. In general, it provides an object oriented method for
    building a grammar. The grammar is built in the init function. In general
    it is undesirable to have many PathParsers, so the intention is to make one and
    share it. The parsePath function is the main function. It returns an array of
    actions, parsed from the string passed in.
    """

    def __init__(self):
        """
        Construct the path grammar and store it in the object.
        Refer to the SVG Path specification for details.
        http://www.w3.org/TR/SVG/paths.html#PathDataMovetoCommands
        I do not guarantee this is a complete or correct grammar, but it works
        for the paths that I have parsed.
        """
        self.firstM = True

        dot = Literal(".")
        comma = Literal(",").suppress()
        exponent = Combine(Word("Ee") + Optional("-") + Word(nums))
        float = Combine(Optional("-") + Word(nums) + dot + Word(nums) + Optional(exponent))
        float2 = Combine(Optional("-") + Word(nums) + Optional(exponent))
        integer = Combine(Optional("-") + Word(nums))
        flag = Word("01")

        xyval = float | float2 | integer
        point = xyval + Optional(comma) + xyval
        cval = Group(point) + Group(point) + Group(point)
        arc = Group(point) + xyval + flag + flag + Group(point)
        cubicBez = Group(point) + Group(point)

        M_command = Word("Mm") + OneOrMore(Group(point))
        C_command = Word("Cc") + OneOrMore(Group(cval))
        L_command = Word("Ll") + OneOrMore(Group(point))
        A_command = Word("Aa") + OneOrMore(Group(arc))
        H_command = Word("Hh") + OneOrMore(xyval)
        V_command = Word("Vv") + OneOrMore(xyval)
        S_command = Word("Ss") + OneOrMore(Group(cubicBez))
        Q_command = Word("Qq") + OneOrMore(Group(cubicBez))
        T_command = Word("Tt") + OneOrMore(xyval)
        Z_command = Word("Zz")
        svgcommand = M_command \
                     | A_command \
                     | C_command \
                     | L_command \
                     | H_command | V_command | S_command \
                     | Q_command | T_command | Z_command

        aPath = OneOrMore(svgcommand) + stringEnd
        self.phrase = aPath

        L_command.setParseAction(lambda s,l,t: self.actionL(s,l,t))
        M_command.setParseAction(lambda s,l,t: self.actionM(s,l,t))
        C_command.setParseAction(lambda s,l,t: self.actionC(s,l,t))
        A_command.setParseAction(lambda s,l,t: self.actionA(s,l,t))
        S_command.setParseAction(lambda s,l,t: self.actionS(s,l,t))
        Q_command.setParseAction(lambda s,l,t: self.actionQ(s,l,t))
        T_command.setParseAction(lambda s,l,t: self.actionT(s,l,t))
        H_command.setParseAction(lambda s,l,t: self.actionH(s,l,t))
        V_command.setParseAction(lambda s,l,t: self.actionV(s,l,t))
        Z_command.setParseAction(lambda s,l,t: self.actionZ(s,l,t))

    def parsePath(self,path):
        """
        Parse the passed in path string.
        Returns an array of actions from the path
        """
        self.actions = []
        self.firstM = True
        self.phrase.parseString(path)
        return self.actions

    def actionC(self,s,l,t):
        #print "Generating an Ellipse"
        if t[0] == 'C':
            isAbs = True
        else:
            isAbs = False

        for x in range(1,len(t)):
            c = t[x] # This is 3 points
            if len(c) == 3:
                [x1,y1] = [float(xx) for xx in c[0]]
                [x2,y2] = [float(xx) for xx in c[1]]
                [x3,y3] = [float(xx) for xx in c[2]]
                points = []
                points.append([x1,y1])
                points.append([x2,y2])
                points.append([x3,y3])
                self.actions.append(PathAction("curve",points,isAbs))

    def actionA(self,s,l,t):
        if t[0] == 'A':
            isAbs = True
        else:
            isAbs = False

        for x in range(1,len(t)):
            c = t[x] # This is 3 points
            if len(c) == 5:
                [rx,ry] = [float(xx) for xx in c[0]]
                rot = float(c[1])
                largeArcFlag = int(c[2])
                sweepFlag = int(c[3])
                [x,y] = [float(xx) for xx in c[4]]
                points = []
                points.append([x,y])
                pa = PathAction("arc",points,isAbs)
                pa.setOpts({
                    'largeArc':largeArcFlag,
                    'sweepFlag':sweepFlag,
                    'rotation':rot,
                    'rx':rx,
                    'ry':ry
                })

                self.actions.append(pa)
            else:
                raise "Invalid Arc"

    def actionS(self,s,l,t):
        #print "Generating a Cubic Bezier"
        pass

    def actionQ(self,s,l,t):
        #print "Generating a Cubic Bezier Q type"
        pass

    def actionT(self,s,l,t):
        #print "Generating a Simple Cubic Bezier"
        pass

    def actionH(self,s,l,t):
        if t[0] == 'H':
            isAbs = True
        else:
            isAbs = False

        for x in range(1,len(t)):
            [xval] = [float(xx) for xx in t[x]]
            self.actions.append(PathAction("hline",[[xval]],isAbs))

    def actionV(self,s,l,t):
        if t[0] == 'V':
            isAbs = True
        else:
            isAbs = False

        for x in range(1,len(t)):
            [yval] = [float(xx) for xx in t[x]]
            self.actions.append(PathAction("vline",[[yval]],isAbs))

    def actionL(self,s,l,t):
        if t[0] == 'L':
            isAbs = True
        else:
            isAbs = False

        for x in range(1,len(t)):
            [xval,yval] = [float(xx) for xx in t[x]]
            self.actions.append(PathAction("line",[[xval,yval]],isAbs))

    def actionM(self,s,l,t):

        mchar = t[0]
        if mchar == 'M':
            """ The first M is always absolute """
            isAbs = True
        else:
            isAbs = False

        for x in range(1,len(t)):
            [xval,yval] = [float(xx) for xx in t[x]]
            if mchar == 'm' and self.firstM:
                self.firstM = False
                self.actions.append(PathAction("move",[[xval,yval]],True))
            elif x > 1:
                # If there is more than one move, then the moves after the
                # first are implicity "lineto"s
                self.actions.append(PathAction("line",[[xval,yval]],isAbs))
            else:
                self.actions.append(PathAction("move",[[xval,yval]],isAbs))

    def actionZ(self,s,l,t):
        self.actions.append(PathAction('close',[],False))

def parsePaths(file):

    pp = PathParser()

    with open(file,'r') as fp:
        paths = [p.strip() for p in fp if p.strip() and p[0] != '#']

    for path in paths:
        print("Parsing:%s" % path.strip())
        actions = pp.parsePath(path.strip())
        for a in actions:
            print a

def recursiveTest():
    grammar = OneOrMore(Word(alphas)) + Literal('end')
    grammar.parseString('First Second Third end')

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("file",
                      help="Specify the path file to parse.")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        sys.exit("Specified Path file does not exist.")

    parsePaths(args.file)
    print ("Parse complete")


if __name__ == '__main__':
    main()
