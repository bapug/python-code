from math import sqrt

class Point(object):
    """
    Point class that provides a range of
    point based operations.
    """

    def __init__(self,*args):
        object.__init__(self)
        if len(args) == 2:
            self.x = args[0]
            self.y = args[1]
        elif len(args) == 1:
            if isinstance(args[0],list) or isinstance(args[0],tuple):
                pts = args[0]
                self.x = pts[0]
                self.y = pts[1]
            elif isinstance(args[0],Point):
                self.x = args[0].x
                self.y = args[0].y
            else:
                raise Exception("Invalid Type:%s" % type(args[0]))
        else:
            raise Exception("Invalid Initialization")

    def __repr__(self):
        return "Point(%f,%f)" % (self.x,self.y)

    def __add__(self,other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x,y)

    def __sub__(self,other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x,y)

    def __mul__(self,other):
        if isinstance(other,Point):
            return Point(self.x*other.x,self.y*other.y)

        fac = float(other)
        x = self.x*fac
        y = self.y*fac
        return Point(x,y)

    def __abs__(self):
        return Point(abs(self.x),abs(self.y))

    def __eq__(self,other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __cmp__(self,other):
        if self.x == other.x and self.y == other.y:
            return 0

        # Use upper-right comparison
        if self.x > other.x and self.y > other.y:
            return 1
        else:
            return -1

    def __getitem__(self,item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y

        if not item:
            print "Item invalid"
        else:
            print "Invalid Point Object Index:%d" % item
        raise Exception("Bad Item")

    def distance(self,other):
        dx = abs(self.x-other.x)
        dy = abs(self.y-other.y)

        return sqrt(dx**2+dy**2)

    def midPoint(self,other):
        mx = (self.x+other.x)/2
        my = (self.y+other.y)/2
        return Point(mx,my)

    def inCircle(self,center,radius):
        distanceSquared = \
            (center.x-self.x)**2 \
            +(center.y-self.y)**2

        if distanceSquared < (radius**2):
            return True

    def array(self):
        return [self.x,self.y]

    def mag(self):
        mag = sqrt(self.x*self.x + self.y*self.y)
        return mag

    def normalize(self):
        mag = self.mag()
        if mag == 0:
            return Point(0,0)
        else:
            return Point(self.x/mag,self.y/mag)

    def vector(self,other):

        dx = other.x - self.x
        dy = other.y - self.y

        return Point(dx,dy)




