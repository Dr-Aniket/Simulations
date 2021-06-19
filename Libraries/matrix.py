class matrix:
    def __init__(self, *x) -> None:
        if len(x) < 2:
            x = list(x[0])
        if not hasattr(x[0], '__iter__'):
            x = [x]

        self.r = len(x)
        self.c = 0
        for i in range(self.r):
            if len(x[i]) > self.c:
                self.c = len(x[i])
        self.mat = list(x)
        self.init()

    def __str__(self) -> str:
        mat = '['
        for i in self.mat:
            for  j in i:
                mat += str(j) + '\t'
            mat += '\n'
        mat = mat.strip() 
        return mat+']'

    def __repr__(self) -> str:
        return f'Matrix : {self.__str__()} | Rows : {self.r} | Coloums : {self.c}'

    def __getitem__(self,i):
        return self.mat[i]
    def __setitem__(self,i,val):
        self.mat[i] = val
        self.init()

    def __add__(self,m2):
        error = 'Only Matrix Addition Allowed'
        assert type(m2) == matrix, error
        if self.r == m2.r and self.c == m2.r:
            m3 = []
            for i in range(self.r):
                temp = []
                for j in range(self.c):
                    temp.append(self[i][j] + m2[i][j])
                m3.append(temp)
            return matrix(m3)
        else:
            raise error

    def __sub__(self,m2):
        error = 'Only Matrix Subtraction Allowed'
        assert type(m2) == matrix, error
        if self.r == m2.r and self.c == m2.r:
            m3 = []
            for i in range(self.r):
                temp = []
                for j in range(self.c):
                    temp.append(self[i][j] - m2[i][j])
                m3.append(temp)
            return matrix(m3)
        else:
            raise error

    def __truediv__(self,m2):
        error = 'Matrix Division Not Allowed'
        assert type(m2) != matrix, error
        m3 = []
        for i in range(self.r):
            temp = []
            for j in range(self.c):
                temp.append(self[i][j]/m2)
            m3.append(temp)
        return matrix(m3)

    def __floordiv__(self,m2):
        error = 'Matrix Division Not Allowed'
        assert type(m2) != matrix, error
        m3 = []
        for i in range(self.r):
            temp = []
            for j in range(self.c):
                temp.append(self[i][j]//m2)
            m3.append(temp)
        return matrix(m3)

    def __mul__(self,m2):
        if type(m2) != matrix:
            return self.mul(m2)
        m3 = []
        for i in range(self.r):
            temp = []
            for j in range(m2.c):
                t = 0
                for x in range(m2.r):
                    t += self[i][x] * m2[x][j] 
                temp.append(t)
            m3.append(temp)
        return matrix(m3)

    def mul(self,m2):
        m3 = []
        for i in range(self.r):
            temp = []
            for j in range(self.c):
                temp.append(self[i][j] * m2)
            m3.append(temp)
        return matrix(m3)
            
    def init(self):
        m = []
        for x in self.mat:
            m.append(list(x) + [0]*(self.c - len(x)))
        self.mat = m
        self.square = ( self.r == self.c )

    def toVector(self):
        v = []
        for i in self:
            v.append(i)
        return v

def identity(r,c=False):
    if not c:
        c = r
    m1 = []
    for i in range(r):
        m2 = []
        for j in range(c):
            val = 0
            if i == j:
                val = 1
            m2.append(val)
        m1.append(m2)
    return matrix(m1)
