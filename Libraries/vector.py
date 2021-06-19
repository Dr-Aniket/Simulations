from math import *
from matrix import matrix

class vector:
    def __init__(self,*x) -> None:
        if type(x[0]) == list or type(x[0]) == tuple:
            x = x[0]
        self.dim = len(x)
        self.vector = list(x) + [0]*(3-self.dim)
        self.init()

    def init(self):
        self.x = self.vector[0]
        self.y = self.vector[1]
        self.z = self.vector[2]
        self.mag = self.value()

    def __str__(self) -> str:
        return f'({self.x})i + ({self.y})j + ({self.z})k'

    def __repr__(self) -> str:
        return f'x : {self.x} | y : {self.y} | z : {self.z}\nMag : {round(self.mag,3)} | Theta : {self.theta()}'

    def __getitem__(self,i):
        return self.vector[i]

    def __setitem__(self,i,val):
        self.vector[i] = val
        self.init()

    def __add__(self,v2):
        assert type(v2) == vector, "Only Vector Addition Allowed"
        v3 = []
        for i in range(max(self.dim,v2.dim)):
            v3.append(self[i] + v2[i])
        return vector(v3) 

    def __sub__(self,v2):
        assert type(v2) == vector, "Only Vector Subtraction Allowed"
        v3 = []
        for i in range(max(self.dim,v2.dim)):
            v3.append(self[i] - v2[i])
        return vector(v3)

    def __mul__(self,v2):
        if type(v2) == vector:
            return self.dot(v2)
        v3 = []
        for i in range(self.dim):
            v3.append(self[i] * v2)
        return vector(v3) 

    def __truediv__(self,v2):
        assert type(v2) != vector, "Vector Division Not Allowed"
        v3 = []
        for i in range(self.dim):
            v3.append(self[i] / v2)
        return vector(v3) 

    def __floordiv__(self,v2):
        assert type(v2) != vector, "Vector Division Not Allowed"
        v3 = []
        for i in range(self.dim):
            v3.append(self[i] // v2)
        return vector(v3) 
    
    def __eq__(self, v2) -> bool:
        return self.vector == v2.vector
    def __ne__(self, v2) -> bool:
        return self.vector != v2.vector
    def __gt__(self,v2) -> bool:
        return self.mag > v2.mag
    def __ge__(self,v2) -> bool:
        return self.mag >= v2.mag
    def __lt__(self,v2) -> bool:
        return self.mag < v2.mag
    def __le__(self,v2) -> bool:
        return self.mag <= v2.mag

    def __neg__(self):
        return self*-1

    def __len__(self):
        return self.dim

    def __round__(self,n=0):
        for i in range(self.dim):
            self[i] = round(self[i],n)
        self.init()
        return self

    def __pow__(self,n:int):
        v2 = self
        for i in range(n-1):
            v2 = self * v2  
        return v2

    def __abs__(self):
        v2 = []
        for i in self:
            v2.append(abs(i))
        return vector(v2)
    
    def value(self) -> float:
        mag = 0
        for i in range(self.dim):
            mag += self.vector[i]**2
        return mag**0.5
    
    def unit(self):
        return self/self.mag

    def dot(self,v2) -> float:
        assert type(v2) == vector, "Dot Product is Operated Only Between Two Vectors"
        till = min(self.dim,v2.dim)
        v3 = 0
        for i in range(till):
            v3 += round(self[i]*v2[i],4)
        return v3

    def cross(self,v2):
        assert type(v2) == vector, "Cross Product is Operated Only Between Two Vectors"
        return vector(self.y*v2.z -self.z*v2.y, 
                self.z*v2.x -self.x*v2.z, 
                self.x*v2.y -self.y*v2.x)

    def theta(self,v2 = False, deg = True):
        if not v2 :
            v2 = vector(1)
        m1 = self.mag
        m2 = v2.mag
        theta = acos((self.dot(v2))/(m1*m2))
        if self.y < 0:
            theta = 2*pi - theta
        if deg:
            return round(degrees(theta),3)
        return round(theta,5)

    def dis(self,v2):
        d = 0
        for i in range(self.dim):
            d += (v2[i] - self[i])**2
        return d**0.5

    def pointLineDis(self,ipos,fpos=False):
        ''' ipos = Initial Point of the line
            fpos = final Point of the Line'''
        if not fpos:
            fpos = ipos
            ipos = vector(0)
        x0 = self
        x1 = ipos
        x2 = fpos
        n=0
        d=0
        x = []
        dim = 3
        # dim = max(x0.dim,x1.dim,x2.dim)
        # x0.v += (dim-x0.dim) * [0]
        # x1.v += (dim-x1.dim) * [0]
        # x2.v += (dim-x2.dim) * [0]
        for i in range(dim):
            a = x2[i]-x1[i]
            n -= ((x1[i]-x0[i])*a)
            d +=  a**2
        t = (n/d)
        for i in range(x0.dim):
              x.append((x2[i]-x1[i]) * t + x1[i])
        return round(vector(x).dis(x0),3)

    def reflect(self,v2):
        alpha = self.theta()
        theta = v2.theta()
        angle = radians(2*theta - alpha)
        v3 = vector(cos(angle),sin(angle))
        v3 *= self.mag
        return round(v3,3)

    def toMatrix(self,vertical = True):
        mat = []
        for x in self:
            if vertical:
                mat.append([x])
            else:
                mat.append(x)
        return matrix(mat)

    def vecMatMul(self,mat,inverse = False):
        m1 = self.toMatrix()
        m2 = mat
        if inverse:
            m1,m2 = m2,m1
        v = []
        for i in ( m2 * m1 ).toVector():
            v.append(i[0])
        return vector(v)
