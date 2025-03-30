def new_func():
    a = 1
    while True:
        a += 1
        yield a

a = new_func()

for i in range(10):
    print(next(a))