import math


class Function:
    def __call__(self, x: float) -> float:
        pass


class Function1(Function):
    def __call__(self, x):
        return x ** 3 - 0.77 * x ** 2 - 1.251 * x + 0.43

    def __str__(self):
        return 'x^3 - 0.77 * x^2 - 1.251 * x + 0.43'


class Function2(Function):
    def __call__(self, x):
        return x ** 3 - x + 4

    def __str__(self):
        return 'x^3 - x + 4'


class Function3(Function):
    def __call__(self, x):
        return 20 * math.cos(x) + x ** 2

    def __str__(self):
        return '20 * cos(x) + x^2'


functions_dict: dict[int, Function] = {
    1: Function1(),
    2: Function2(),
    3: Function3()
}
