import math


def f(x1):
    """
    Calculates y = f(x) and returns it.
    :param x1: Value of float type
    :return y1: Value of float type
    """
    a = math.cos(20 / 54) + 9 * math.pi
    b = 48 * math.e * (10 / ((x1 + 11) * (x1 - 15)))
    c = 14 * math.cos(x1 + 6)
    d = 1 / (math.sqrt(x1 - 13))
    y1 = a - b - c + d
    return y1


def _define_res(x1):
    """
    Checks all possible exceptions and returns the result.
    :param x1: Value of float type
    :return res1: Value of float type or None
    """
    try:
        res1 = f(x1)
    except BaseException:
        return None
    else:
        return res1


def _result_print(x1, y1):
    """
    Prints out calculation results of f(x) at the point x.
    :param x1: Value of float type
    :param y1: Value of float type checked for None
    :return: None
    """
    print('done')
    print(f'for x = {x1:.8f}')
    if y1 is None:
        print(f'result = undefined')
    else:
        print(f'result = {y1:.8f}')


print('This program is coded by Andriy Nazarenko (K-11 group) ')
print('This program calculates f(x) at the point x (variant 52)')
try:
    x = float(input('Enter something (x) of real type: '))
    print('***** do calculations ...', end=' ')
    y = _define_res(x)
    _result_print(x, y)

except BaseException:
    print('wrong input')
