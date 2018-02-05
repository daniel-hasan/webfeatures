from abc import abstractmethod
class A(object):
    def x(self):
        print("oioioi A")
    
class B(object):
    def b(self):
        pass
    
class C(object):
    def c(self):
        pass
    def x(self):
        print("oioioi C")

class D(B,A,C):
    def c(self):
        print("C")
    def b(self):
        print("B")
            
if __name__ == "__main__":
    objD = D()
    objD.c()
    objD.b()
    objD.x()