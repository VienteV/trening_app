class New_class():
    def __init__(self, a):
        self.a = a
        self.n = 0
    def __iter__(self):
        return self

    def __next__(self):
        b = self.a ** self.n
        self.n += 1
        return b

n = New_class(2)

i = 10
while i > 0:
    print(next(n))
    i -= 1
