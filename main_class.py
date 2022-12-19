from sub_class import A

class B(A):
    def __init__(self):
        self.test_b = "test_b"
        super().__init__()

    def y(self):
        print('Child B behavior')

class C(A):
    def z(self):
        pass

print(B().test)