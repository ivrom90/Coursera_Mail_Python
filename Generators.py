def fibonacci(number):
    a = b = 1
    for _ in range(number):
        yield a
        a, b = b, a + b


for num in fibonacci(10):
    print(num)


def accumulator():
    total = 0
    while True:
        value = yield total
        print("Got: {}".format(value))

        if not value:
            break
        total += value


generator = accumulator()
next(generator)
print("Accumulated: {}".format(generator.send(1)))
print("Accumulated: {}".format(generator.send(1)))
print("Accumulated: {}".format(generator.send(1)))

# Next line will give 'StopIteration' error

next(generator)
