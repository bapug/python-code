__author__ = 'kutenai'


from Point import Point

class PathAction(object):
    """
    Class to represent the actions in a path.
    The type is one of the move, arc, line, etc.
    The points is a list of x,y values. Their meaning
    depends on the type. The isAbs defines if these
    points are absolute or relative. The options allow
    extra values, such as are present with the arc,
    to be passed.

    """

    def __init__(self,type,points,isAbs = True):

        self.type = type
        self.points = points
        self.isAbs = isAbs
        self.opts = {}

        if self.type == "move":
            self.char = 'm'
        elif self.type == 'curve':
            self.char = 'c'
        elif self.type == "arc":
            self.char = 'a'
        elif self.type == "line":
            self.char = 'l'
        elif self.type == "close":
            self.char = 'z'
        else:
            self.char = "?"

        if self.isAbs:
            self.char = self.char.upper()


    def __str__(self):
        s = self.char
        if self.isAbs:
            s = s + " Abs"
        else:
            s = s + " Rel"

        for p in self.points:
            s = s + " %f,%f" % (p[0],p[1])

        return s

    def setOpts(self,opts):
        for k in opts:
            self.opts[k] = opts[k]

    def getPoints(self,currPt,xform):
        """
        If this is an absolute action, then check
        to see if there is a transform. If so,
        transform the points and return the new
        values. If there is no transform, return
        the current values.

        If this is a relative action, then add the
        currPt x,y values to the points and return
        the new value.
        """
        if self.isAbs:
            # Absolute values.
            newPts = []
            for pt in self.points:
                x,y = xform.transformPoint(pt[0],
                                            pt[1])
                newPts.append(Point(x,y))

            return newPts
        else:
            # Relative points, offset with the currPt
            pts = []
            for pt in self.points:
                sx,sy = xform.scalePoint(pt[0],
                                        pt[1])
                x = sx + currPt[0]
                y = sy + currPt[1]
                pts.append(Point(x,y))

            return pts

