from math import acos,degrees,cos,sin,radians,atan,inf,pi

class vector:
    def __init__(self,*x):
        x = list(x)
            
        if type(x[0]) == list or type(x[0]) == tuple:
            x[0] = list(x[0])
            x = x[0]
        self.dim = len(x)
        self.v = x #+ [0]*(3-len(x))
    
    def mag(self):
        mag_ = 0
        for v_ in self.v:
            mag_ += v_**2
        return mag_**0.5

    def unit(self):
        if self.mag()!=0:
            return self/self.mag()
        return vector([0]*self.dim)

    def __lshift__(self,v2=False):
        try:
            if not v2:
                v2 = vector(1,0)
            try:
                if self[1] == 0:
                    t1 = 0
                else:
                    t1 = self[1]/self[0]
            except:
                t1 = inf
            try:
                if v2[1] == 0:
                    t2 = 0
                else:
                    t2 = v2[1]/v2[0]
            except:
                t2 = inf
            t1 = atan(t1)
            if self[0]<0:
                t1 += pi
            t2 = atan(t2)
            if v2[0]<0:
                t2 += pi
            theta = t1 - t2
            theta = degrees(theta)
            return round(theta,3)
        except:
            return 0 
        
    def theta(self,v2=False):
        try:
            if not v2:
                v2 = vector(1,0)
            try:
                if self[1] == 0:
                    t1 = 0
                else:
                    t1 = self[1]/self[0]
            except:
                t1 = inf
            try:
                if v2[1] == 0:
                    t2 = 0
                else:
                    t2 = v2[1]/v2[0]
            except:
                t2 = inf
            t1 = atan(t1)
            if self[0]<0:
                t1 += pi
            t2 = atan(t2)
            if v2[0]<0:
                t2 += pi
            theta = t1 - t2
            theta = degrees(theta)
            return round(theta,3)
        except:
            return 0 
    
    def __repr__(self):
        return str(self.v)

    def __add__(self,v2):
        v3 = []
        for i,j in zip(self.v,v2.v):
            v3.append(i+j)
        return vector(v3)

    def __sub__(self,v2):
        v3 = []
        for i,j in zip(self.v,v2.v):
            v3.append(i-j)
        return vector(v3)
    
    def __neg__(self):
        v2 = []
        for i in self.v:
            v2.append(-1*i)
        return vector(v2)

    def __mul__(self,v2):            
        if type(v2) != vector:
            v3 = []
            for i in self.v:
                v3.append(i*v2)
            return vector(v3)

        v3 = 0
        for i,j in zip(self.v,v2.v):
            v3 += i*j
        return v3

    def __truediv__(self,v2):
        assert type(v2) != vector,  "Division Of Vectors Not Alowed"
##        if type(v2) != vector:
        v3 = []
        for i in self.v:
            v3.append(round(i/v2,5))
        return vector(v3)

    
    def __floordiv__(self,v2):
        assert type(v2) != vector,  "Division Of Vectors Not Alowed"
##        if type(v2) != vector:
        v3 = []
        for i in self.v:
            v3.append(i//v2)
        return vector(v3)
    
    def __pow__(self,v2):
        v3 = [self.v[1]*v2.v[2] -self.v[2]*v2.v[1], 
              self.v[2]*v2.v[0] -self.v[0]*v2.v[2], 
              self.v[0]*v2.v[1] -self.v[1]*v2.v[0]]
        return vector(v3) 

    def __lt__(self,v2):
        if self.v < v2.v:
            return True
        return False
   
    def __gt__(self,v2):
        if self.v > v2.v:
            return True
        return False
    
    def __le__(self,v2):
        if self.v <= v2.v:
            return True
        return False
   
    def __ge__(self,v2):
        if self.v >= v2.v:
            return True
        return False
   
    def __eq__(self,v2):
        if self.v == v2.v:
            return True
        return False

    def __getitem__(self,i):
        return self.v[i]

    def __setitem__(self,i,val):
        self.v[i] = val
        
    def __or__(self,v2):
        distance = 0
        for i,j in zip(self.v,v2.v):
            distance += (j-i)**2
        return distance**0.5
    
    def dis(self,v2):
        distance = 0
        for i,j in zip(self.v,v2.v):
            distance += (j-i)**2
        return distance**0.5
    
    def pointLineDis(self,ipos,fpos):
        ''' ipos = Initial Point of the line
            fpos = final Point of the Line'''
        x0 = self
        x1 = ipos
        x2 = fpos
        n=0
        d=0
        x = []
        dim = max(x0.dim,x1.dim,x2.dim)
        x0.v += (dim-x0.dim) * [0]
        x1.v += (dim-x1.dim) * [0]
        x2.v += (dim-x2.dim) * [0]
        for i in range(dim):
            a = x2[i]-x1[i]
            n -= ((x1[i]-x0[i])*a)
            d +=  a**2
        t = (n/d)
        for i in range(x0.dim):
              x.append((x2[i]-x1[i]) * t + x1[i])
        return round(vector(x)|x0,3)

    def reflect(self,v2):
        alpha = self.theta()
        theta = v2.theta()
        angle = radians((2*theta - alpha)-90)
        v3 = vector(round(cos(angle),3),round(sin(angle),3))
        v3 *= self.mag()
        return 
