"""
This program calculates S(x) at the point x with precision eps (variant 52)
Coded by Nazarenko Andriy
Domain of x: [a; b], a = -1, b = 1
a <= x <= b
"""


def s(x0, eps0):
    """
    Calculating S(x) at the point x with precision eps.
    :param x0: value x of float type
    :param eps0: precision eps of float type
    :return sum0: result of float type
    """
    xn = (x0 * x0 * x0) / 6
    sum0 = xn
    n = 1
    while xn >= eps0 or xn <= -eps0:
        xn = xn * ((n * (n + 1)) / ((2 * n + 2) * (2 * n + 3)) * x0 * x0)
        n += 1
        sum0 += xn
    return sum0


def _check_error(x0, eps0, a0, b0):
    """
    Checks for errors of type, precision and belonging parm x to the domain.
    :param x0: value x of float type
    :param eps0: precision eps of float type
    :param a0: value a that determines the domain S(x), a <= x <= b
    :param b0: value b that determines the domain S(x), a <= x <= b
    """
    try:
        x0 = float(x0)
        eps0 = float(eps0)
        if eps0 <= 0:
            print('***** Error')
            print('Reason: Precision <= 0')
        elif a0 <= x0 <= b0:
            print('***** do calculations ...', end='')
            y0 = s(x0, eps0)
            _result_print(x0, eps0, y0)
        else:
            print('***** Error')
            print('Reason: Value x is out of the domain of the function S(x)')

    except ValueError:
        print('***** Error')
        print('Reason: Input value could not be converted to float')


def _result_print(x0, eps0, y0):
    """
    Printing the results, if there is no Error.
    :param x0:
    :param eps0:
    :param y0:
    :return:
    """
    print('done')
    print(f'for x = {x0:.5f}')
    print(f'for eps = {eps0:.4e}')
    print(f'result = {y0:.9f}')


print('This program is coded by Nazarenko Andriy (K-11 group)')
print('This program calculates S(x) at the point x with precision eps (variant 52)')
a = -1
b = 1
try:
    x = input('Enter x of real type, -1 <= x <= 1: ')
    eps = input('Enter precision of real type:')
    _check_error(x, eps, a, b)
except EOFError or KeyboardInterrupt:
    print('***** Error')
    print('Reason: You have forcibly stopped the program. ')
