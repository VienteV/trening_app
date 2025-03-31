class New_class():
    def __init__(self, a):
        self.a = a

    def __iter__(self):
        return self
    def __next__(self):
        return self.a
