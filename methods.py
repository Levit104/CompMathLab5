import math

from util import equally_spaced


class InterpolationError(Exception):
    pass


class Method:
    def __init__(self, name):
        self.name = name

    def __call__(self, x_values, y_values, n, x, finite_diffs, check_t):
        pass


class Lagrange(Method):
    def __call__(self, x_values, y_values, n, x, finite_diffs=None, check_t=None):
        res = 0
        for i in range(n):
            y = y_values[i]
            for j in range(n):
                if i != j:
                    y *= (x - x_values[j]) / (x_values[i] - x_values[j])
            res += y
        return res


def gauss_left(y_values, n, finite_diffs, i_center, t):
    res = y_values[i_center]
    for i in range(1, n):
        index = (i + 1) // 2
        t_prod = 1
        # print(index)
        for j in range(-index + 1, (i // 2) + 1):
            # print('gauss_left', j)
            t_prod *= (t + j)
        delta_y = finite_diffs[i][i_center - index]
        res += t_prod * delta_y / math.factorial(i)
    return res


def gauss_right(y_values, n, finite_diffs, i_center, t):
    res = y_values[i_center]
    for i in range(1, n):
        index = i // 2
        t_prod = 1
        # print(index)
        for j in range(-index, (i + 1) // 2):
            # print('gauss_right', j)
            t_prod *= (t + j)
        delta_y = finite_diffs[i][i_center - index]
        res += t_prod * delta_y / math.factorial(i)
    return res


class Gauss(Method):
    def __call__(self, x_values, y_values, n, x, finite_diffs, check_t=None):
        if n % 2 == 0:
            raise InterpolationError('кол-во узлов должно быть нечётным')
        if not equally_spaced(x_values):
            raise InterpolationError('узлы должны быть равностоящими')

        i_center = (n - 1) // 2
        a = x_values[i_center]
        h = x_values[1] - x_values[0]
        t = (x - a) / h

        if x > a:
            return gauss_right(y_values, n, finite_diffs, i_center, t)
        elif x < a:
            return gauss_left(y_values, n, finite_diffs, i_center, t)
        else:
            return y_values[i_center]


class Stirling(Method):
    def __call__(self, x_values, y_values, n, x, finite_diffs, check_t=None):
        if n % 2 == 0:
            raise InterpolationError('кол-во узлов должно быть нечётным')
        if not equally_spaced(x_values):
            raise InterpolationError('узлы должны быть равностоящими')

        i_center = (n - 1) // 2
        a = x_values[i_center]
        h = x_values[1] - x_values[0]
        t = (x - a) / h

        if check_t and not abs(t) <= 0.25:
            raise InterpolationError(f't = {t} не входит в диапазон |t| <= 0.25')

        if x == a:
            return y_values[i_center]
        else:
            return (gauss_left(y_values, n, finite_diffs, i_center, t)
                    + gauss_right(y_values, n, finite_diffs, i_center, t)) / 2


class Bessel(Method):
    def __call__(self, x_values, y_values, n, x, finite_diffs, check_t=True):
        if n % 2 != 0:
            raise InterpolationError('кол-во узлов должно быть чётным')
        if not equally_spaced(x_values):
            raise InterpolationError('узлы должны быть равностоящими')

        i_center = (n - 1) // 2
        a = x_values[i_center]
        h = x_values[1] - x_values[0]
        t = (x - a) / h

        if check_t and not 0.25 <= abs(t) <= 0.75:
            raise InterpolationError(f't = {t} не входит в диапазон 0.25 <= |t| <= 0.75')

        res = (y_values[i_center] + y_values[i_center + 1]) / 2

        for i in range(1, n):
            index = i // 2
            if i % 2 == 1:
                t_prod = (t - 0.5) * finite_diffs[i][i_center - index]
            else:
                t_prod = (finite_diffs[i][i_center - index] + finite_diffs[i][i_center - index + 1]) / 2
            for j in range(i // 2):
                t_prod *= (t + j) * (t - j - 1)
            res += t_prod / math.factorial(i)

        return res


methods_list: list[Method] = [
    Lagrange('Лагранж'),
    Gauss('Гаусс'),
    Bessel('Бессель'),
    Stirling('Стирлинг')
]
