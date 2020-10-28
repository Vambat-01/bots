"""
1) privet
2) privet n times
3) sum 1+2+3+4+5
4) factorial 5! = 1*2*3*4*5 = 120
5) fibonacci 0,1,1,2,3,4,8,13,21,34,55,89

"""


# 1) Будет выполняться пока не достигнет придела в python (бесконечно)


def privet():
    print("Hello world")
    privet()


# privet()


# 2) privet n times


def privet_n_times(x):
    if x == 0:
        return 0
    else:
        print("Hello world")
        privet_n_times(x - 1)


privet_n_times(3)


# 3) sum 1+2+3+4+5

def sum(x):
    if x == 0:
        return 0
    else:
        return x + sum(x-1)


y = sum(5)
print(y)


# 4) factorial 5! = 1*2*3*4*5 = 120

def factorial(x):
    if x == 0:
        return 1
    else:
        return x * factorial(x - 1)


y = factorial(5)
print(y)


# 5) fibonacci 0,1,1,2,3,4,8,13,21,34,55,89


def fibon(x):
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        return fibon(x - 1) + fibon(x - 2)


y = fibon(10)
print(y)


