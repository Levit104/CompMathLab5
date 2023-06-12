from console import print_input_modes, get_input_id, get_data, print_matrix, get_x
from methods import methods_list, InterpolationError
from util import *

import matplotlib.pyplot as plt

if __name__ == '__main__':
    while True:
        try:
            print('\nЧтобы выйти из программы введите exit на любом этапе')

            print_input_modes()
            input_id = get_input_id()

            points_number, points = get_data(input_id)
            sort_by_column(points, col=0)
            print(f'\nКол-во точек: {points_number}')
            print_matrix(points, 'Значения X и Y')

            x_values, y_values = separate_columns(points)

            if has_duplicates(x_values):
                print('\nЗначения X должны быть уникальными. Повторите ввод')
                continue

            plt.scatter(x_values, y_values, label='Исходные данные')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.grid()
            plt.title('Интерполяция функции')

            finite_diffs = get_finite_diffs(y_values, points_number)
            print_matrix(extend_finite_diffs(transpose_matrix(finite_diffs), x_values), 'Конечные разности')

            x = get_x(min_val=min(x_values), max_val=max(x_values))

            methods_diffs_dict = {}

            for method in methods_list:
                try:
                    result = method(x_values, y_values, points_number, x, finite_diffs, True)
                    print(f'\nРезультат интерполяции ({method.name}): {result}')
                    methods_diffs_dict[method.name] = result
                    x_graph = linspace(min(x_values), max(x_values), 1000)
                    y_graph = [method(x_values, y_values, points_number, xg, finite_diffs, False) for xg in x_graph]
                    plt.plot(x_graph, y_graph, label=method.name)
                except InterpolationError as error:
                    print(f'\nОшибка интерполяции ({method.name}): {error}')

            plt.legend()
            plt.show()

            print_methods_diffs(methods_diffs_dict)

        except (EOFError, KeyboardInterrupt):
            print("\nВыход из программы")
            break
