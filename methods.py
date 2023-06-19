import math

from util import equally_spaced


class InterpolationError(Exception):
    pass


class Method:
    name: str

    def solve(self,
              x_values: list[float],
              y_values: list[float],
              n: int,
              x: float,
              finite_diffs: list[list[float]],
              validate_t: bool,
              float_format: str) -> float:
        pass

    def __call__(self,
                 x_values: list[float],
                 y_values: list[float],
                 n: int,
                 x: float,
                 finite_diffs: list[list[float]],
                 validate_t: bool,
                 float_format: str) -> float:
        return self.solve(x_values, y_values, n, x, finite_diffs, validate_t, float_format)


class Lagrange(Method):
    name = 'Лагранж'

    def solve(self, x_values, y_values, n, x, finite_diffs, validate_t, float_format):
        res = 0
        for i in range(n):
            y = y_values[i]
            for j in range(n):
                y *= (x - x_values[j]) / (x_values[i] - x_values[j]) if i != j else 1
            res += y
        return res


class Gauss(Method):
    name = 'Гаусс'

    @staticmethod
    def validate(points_number: int, x_values: list[float], odd: bool = True) -> None:
        if odd and points_number % 2 == 0:
            raise InterpolationError('кол-во узлов должно быть нечётным')
        if not odd and points_number % 2 != 0:
            raise InterpolationError('кол-во узлов должно быть чётным')
        if not equally_spaced(x_values):
            raise InterpolationError('узлы должны быть равностоящими')

    @staticmethod
    def get_initial_values(x_values: list[float], n: int, x: float) -> tuple[int, float, float]:
        i_center: int = (n - 1) // 2
        a: float = x_values[i_center]
        h: float = x_values[1] - x_values[0]
        t: float = (x - a) / h
        return i_center, a, t

    @staticmethod
    def gauss_first(y_values: list[float], n: int, finite_diffs: list[list[float]], i_center: int, t: float) -> float:
        res = y_values[i_center]
        for i in range(1, n):
            index = i // 2
            t_prod = 1
            for j in range(-index, (i + 1) // 2):
                t_prod *= (t + j)
            delta_y = finite_diffs[i][i_center - index]
            res += t_prod * delta_y / math.factorial(i)
        return res

    @staticmethod
    def gauss_second(y_values: list[float], n: int, finite_diffs: list[list[float]], i_center: int, t: float) -> float:
        res = y_values[i_center]
        for i in range(1, n):
            index = (i + 1) // 2
            t_prod = 1
            for j in range(-index + 1, (i // 2) + 1):
                t_prod *= (t + j)
            delta_y = finite_diffs[i][i_center - index]
            res += t_prod * delta_y / math.factorial(i)
        return res

    def solve(self, x_values, y_values, n, x, finite_diffs, validate_t, float_format):
        self.validate(n, x_values)

        i_center, a, t = self.get_initial_values(x_values, n, x)

        if x > a:
            return self.gauss_first(y_values, n, finite_diffs, i_center, t)
        elif x < a:
            return self.gauss_second(y_values, n, finite_diffs, i_center, t)
        else:
            return y_values[i_center]


class Stirling(Gauss):
    name = 'Стирлинг'

    def solve(self, x_values, y_values, n, x, finite_diffs, validate_t, float_format):
        self.validate(n, x_values)

        i_center, a, t = self.get_initial_values(x_values, n, x)

        if validate_t and not abs(t) <= 0.25:
            raise InterpolationError(f't = {t:{float_format}} не входит в диапазон |t| <= 0.25')

        if x == a:
            return y_values[i_center]

        right = self.gauss_first(y_values, n, finite_diffs, i_center, t)
        left = self.gauss_second(y_values, n, finite_diffs, i_center, t)

        return (right + left) / 2


class Bessel(Gauss):
    name = 'Бессель'

    def solve(self, x_values, y_values, n, x, finite_diffs, validate_t, float_format):
        self.validate(n, x_values, odd=False)

        i_center, a, t = self.get_initial_values(x_values, n, x)

        if validate_t and not 0.25 <= abs(t) <= 0.75:
            raise InterpolationError(f't = {t:{float_format}} не входит в диапазон 0.25 <= |t| <= 0.75')

        if x == a:
            return y_values[i_center]

        res = (y_values[i_center] + y_values[i_center + 1]) / 2
        for i in range(1, n):
            index = i // 2
            if i % 2 == 1:
                t_prod = (t - 0.5) * finite_diffs[i][i_center - index]
            else:
                t_prod = (finite_diffs[i][i_center - index] + finite_diffs[i][i_center - index + 1]) / 2
            for j in range(i // 2):
                t_prod *= (t - j) * (t + j - 1)
            res += t_prod / math.factorial(i)

        return res


methods_list: list[Method] = [
    Lagrange(),
    Gauss(),
    Stirling(),
    Bessel()
]
