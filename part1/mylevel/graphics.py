#E.S. Stenberg (m226252)
import math
import numpy

class Point3D:
    def __init__(self,val,*args):
        if (type(val) is numpy.ndarray):
            self.v = val
        elif (args and len(args) == 2):
            self.v = numpy.array([val,args[0],args[1]], dtype='float64')
        else:
            raise Exception("invalid Arguments to Point3D")
    def __str__(self):
        return str(self.v)
    def __repr__(self):
        return str(self.v)
    def __add__(self,v2):
        return Point3D(numpy.asarray([self.v[i] + v2.v[i] for i in [0,1,2]]))
    def __sub__(self,v2):
        if isinstance( v2, Point3D):
            return Vector3D(numpy.array([self.v[i] - v2.v[i] for i in range(len(v2.v))],dtype='float64'))
        elif isinstance(v2, Vector3D):
            return Vector3D(numpy.array([self.v[i] - v2.v[i] for i in range(len(v2.v))], dtype='float64'))
    def distancesquared(self,v2):
        return sum([math.pow(self.v[i]-v2.v[i],2) for i in range(len(v2.v))])
    def distance(self,v2):
        return math.pow(self.distancesquared(v2),.5)
    def copy(self,):
        return Point3D(self.v)
    def __mul__(self,constant):
        return Point3D([self.v[i]*constant for i in range(len(self.v))])

class Vector3D:
    def __init__(self,array, *args):
        if type(array) is numpy.ndarray:
            self.v = array
        elif args and len(args) == 2:
            self.v = numpy.array([array,args[0],args[1]],dtype='float64')
        else:
            raise Exception("Invalid Args to Vector3D")
    def __str__(self):
        return str(self.v)
    def __add__(self,v2):
        if isinstance(v2,Vector3D):
            return Vector3D(self.v + v2.v)
        elif isinstance(v2, Normal):
            return Vector3D(self.v + v2.v)
    def __sub__(self,v2):
        return Vector3D(self.v-v2.v)
    def __mul__(self,v2):
        if isinstance(v2,Vector3D):
            return Vector3D(numpy.array([self.v[i]*v2.v[i] for i in range(len(self.v))], dtype='float64'))
        elif isinstance(v2,int) or isinstance(v2,float):
            return Vector3D(numpy.array([self.v[index]*v2 for index in range(len(self.v))],dtype='float64'))
    def __div__(self,v2):
        return Vector3D(numpy.array([(self.v[i] / v2.v[i]) for i in range(len(self.v))], dtype='float64'))
    def cross(self, v2):
        return Vector3D(numpy.array([self.v[1]*v2.v[2]-self.v[2]*v2.v[1],self.v[2]*v2.v[0]-self.v[0]*v2.v[2],self.v[0]*v2.v[1]-self.v[1]*v2.v[0]]))
    def copy(self):
        return self.v
    def magnitude(self):
        return pow(sum([pow(self.v[i],2) for i in range(len(self.v))]), .5)
    def square(self):
        return sum([pow(self.v[i],2) for i in range(len(self.v))])
    def dot(self,v2):
        return sum([self.v[i]*v2[i] for i in range(len(self.v))])
    def dotangle(self,v2,angle):
        self.magnitude*v2.magnitude*math.cos(angle)
    def dot(self, v2):
        return sum([self.v[i]*v2.v[i] for i in [0,1,2]])

class Normal:
    def __init__(self, array, *args):
        if type(array) is numpy.ndarray:
            self.v = array
        elif args and len(args) == 2:
            self.v = numpy.array([array,args[0],args[1]],dtype='float64')
        else:
            raise Exception("Invalid Args to Vector3D")
    def __str__(self):
        return str(self.v)
    def __neg__(self):
        return Normal(numpy.array([-self.v[i] for i in [0,1,2]],dtype='float64'))
    def __add__(self,v2):
        if isinstance(v2,Normal):
            return Normal(numpy.array([self.v[i] + v2.v[i] for i in [0,1,2]],dtype='float64'))
        elif isinstance(v2, Vector3D):
            return Vector3D(numpy.array([self.v[i] + v2.v[i] for i in [0,1,2]], dtype='float64'))
    def __mul__(self,v2):
        if isinstance(v2, Vector3D):
            return sum([self.v[i]*v2.v[i] for i in [0,1,2]])
        if isinstance(v2,float) or isinstance(v2,int):
            return Vector3D(numpy.array([self.v[i]*v2 for i in [0,1,2]],dtype='float64'))
        else:
            pass
    def dot(self,v2):
        if isinstance(v2,Vector3D):
            return sum([self.v[i]*v2.v[i] for i in [0,1,2]])

class Ray:
    def __init__(self, point, vector):
        self.origin = point
        self.direction = vector
    def copy(self):
        return Ray(self.origin, self.direction)
    def __repr__(self):
        return str([list(self.origin.v),list(self.direction.v)])

class ColorRGB:
    def __init__(self,val, *args):
        if type(val) is numpy.ndarray:
            self.colors = val
        elif args and len(args) == 2:
            self.colors = numpy.array([val,args[0],args[1]], dtype='float64')
        else:
            raise Exception("bad args to ColorRGB")

    def copy(self):
        return ColorRGB(self.colors)
    def getR(self):
        return self.colors[0]
    def getG(self):
        return self.colors[1]
    def getB(self):
        return self.colors[2]
    def __add__(self,other):
        return ColorRGB(self.colors+other.colors)
    def __mul__(self,other):
        if isinstance(other,ColorRGB):
            return ColorRGB(self.colors*other.colors)
        elif isinstance(other,int) or isinstance(other,float):
            return ColorRGB(self.colors*other)

    def __truediv__(self,other):
        return ColorRGB(self.colors / other)
    def __pow__(self,other):
        return ColorRGB(numpy.array([pow(self.colors[i],other) for i in [0,1,2]],dtype='float64'))
    def __repr__(self):
        return str([self.getR(),self.getG(),self.getB()])

class Plane:
    def __init__(self,point,normal,color=ColorRGB(1,1,1)):
        self.point = point
        self.normal = normal
        self.color = color
    def copy(self):
        return Plane(self.point,self.normal,self.color)
    def __repr__(self):
        return str([list(self.point.v),list(self.normal.v)])
    def hit(self,ray,epsilon,shadeRec=False):
        collision = False
        t = 0
        point = Point3D(0,0,0)
        color = ColorRGB(0,0,0)
        try:
            t = (self.normal*(self.point-ray.origin)) / (ray.direction.dot(self.normal))
            collision = True
            point = ray.origin + ray.direction*t
            color = self.color
        except:
            pass

        return (collision,t,point,color)

class Sphere:
     def __init__(self,point,radius,color=ColorRGB(1,1,1)):
         self.center = point
         self.radius = radius
         self.color = color

     def copy(self):
         return Sphere(self.center,self.radius,self.color)
     def __repr__(self):
         return str([list(self.center.v),self.radius])
     def hit(self,ray,epsilon,shadeRec=False):
         d = ray.direction
         o = ray.origin
         center = self.center
         collision = False
         t = 0
         point = Point3D(0,0,0)
         color = ColorRGB(0,0,0)
         a = d.dot(d)
         b = 2*(o-center).dot(d)

         c = (o-center).dot((o-center)) - self.radius**2

         discriminant = math.sqrt(b**2 - 4*a*c)
         if discriminant < 0:
             pass
         elif discriminant == 0:
             t = (-b / (2*a))
         elif discriminant > 0:
             t1 = (-b + discriminant) / 2*a
             t2 = (-b - discriminant) / 2*a

             if t1 < t2:
                 t = t1
             else:
                t = t2
         collision = True
         point = ray.origin + ray.direction*t
         color = self.color


         return (collision,t,point,color)

if __name__ == "__main__":
    s = Sphere(Point3D(0,0,0),5.0)
    v = Ray(Point3D(0,10,0),Vector3D(numpy.asarray([0.0,-1.0,0.0])))

    print(s.hit(v,0.0001))
