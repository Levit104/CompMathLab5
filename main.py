import matplotlib.pyplot as plt

from io_handler import get_data
from methods import methods_list, InterpolationError
from util import linspace, print_methods_diffs

if __name__ == '__main__':
    while True:
        try:
            float_format = '.5f'
            data = get_data(float_format)

            if data is None:
                continue

            x_values, y_values, points_number, x, finite_diffs = data
            methods_diffs_dict = {}

            plt.scatter(x_values, y_values, label='Исходные данные')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.grid()
            plt.title('Интерполяция функции')

            print()  # отступ
            for method in methods_list:
                try:
                    result = method(x_values, y_values, points_number, x, finite_diffs,
                                    validate_t=True, float_format=float_format)
                    print(f'Результат интерполяции ({method.name}): {result:{float_format}}')
                    methods_diffs_dict[method.name] = result
                    x_graph = linspace(min(x_values), max(x_values), 1000)
                    y_graph = [method(x_values, y_values, points_number, x, finite_diffs,
                                      validate_t=False, float_format=float_format) for x in x_graph]
                    plt.plot(x_graph, y_graph, label=method.name)
                except InterpolationError as error:
                    print(f'Ошибка интерполяции ({method.name}): {error}')

            plt.legend()
            plt.show()

            print_methods_diffs(methods_diffs_dict, float_format=float_format)

        except (EOFError, KeyboardInterrupt):
            print("\nВыход из программы")
            break
