from functions import functions_dict
from validation import valid_file, valid_value, valid_matrix_row


def get_value(description, *valid_params, add_validation=lambda x: True, add_message=''):
    value = input(f'\n{description}: ').strip()
    while not (valid_value(value, *valid_params) and add_validation(value)):
        print(f'Невалидное значение'
              f'{add_message}')
        value = input('Повторите ввод: ').strip()

    return value


def get_matrix_row(description, row_size, *valid_row_value_params):
    row = input(f'\n{description}: ').split()

    while not valid_matrix_row(row, row_size, *valid_row_value_params):
        print('Невалидные значения или размер ряда')
        row = input('Повторите ввод: ').split()

    return [float(val) for val in row]


def get_matrix(matrix_size, description, row_size, *valid_row_value_params):
    matrix = [get_matrix_row(description.format(i + 1), row_size, *valid_row_value_params)
              for i in range(matrix_size)]
    return matrix


def get_file(validate=True):
    path = input('\nВведите путь до файла: ').strip()

    if validate:
        while not valid_file(path):
            print('Файла не существует или он пустой')
            path = input('Повторите ввод: ').strip()

    return path


def print_dictionary(name, dictionary):
    print(f'\n{name}:', end='')
    for key, value in dictionary.items():
        print(f'\n\t{key}. {value}', end='')
    print()


def print_matrix(matrix, name):
    print(f'\n{name}:')
    for row in matrix:
        for val in row:
            if type(val) is str:
                if val == 'i':
                    print(f'{val}', end='\t')
                else:
                    print(f'{val:^8}', end='\t')
            elif val is not None:
                if type(val) is int:
                    print(f'{val}', end='\t')
                else:
                    print(f'{val:=8.5f}', end='\t')
        print()


CONSOLE = 1
FILE = 2
FUNCTION = 3

valid_input_id_params = (CONSOLE, FUNCTION, False)
valid_x_params = (1, 1, False)
valid_points_number_params = (2, float('inf'), False)
valid_points_values_params = (float('-inf'), float('inf'), True)
valid_function_id_params = (1, len(functions_dict), False)
valid_interval_params = (float('-inf'), float('inf'), True)

input_modes = {
    CONSOLE: 'Консоль',
    FILE: 'Файл',
    FUNCTION: 'Функция'
}


def print_input_modes():
    print_dictionary('Режимы ввода', input_modes)


def get_input_id():
    return int(get_value('Выберите режим ввода', *valid_input_id_params))


def get_points_number():
    return int(get_value('Введите кол-во точек',
                         *valid_points_number_params,
                         add_message='\nКол-во точек должно быть от 2'))


def get_points(points_number):
    return get_matrix(points_number, 'Введите через пробел значения x и y точки {}', 2, *valid_points_values_params)


def get_x(min_val, max_val):
    return float(get_value('Введите значение X, при котором нужно найти приближенное значение функции',
                           min_val, max_val, False,
                           add_message='\nЗначение X должно быть в интервале'))


def get_interval():
    left_bound = float(get_value('Введите левую границу интервала',
                                 *valid_interval_params))
    right_bound = float(get_value('Введите правую границу интервала',
                                  *valid_interval_params,
                                  add_validation=lambda r: float(r) > left_bound,
                                  add_message='\nПравая граница должна быть больше нижней'))
    return left_bound, right_bound


def get_function_id():
    return int(get_value('Выберите функцию', *valid_function_id_params))


def get_data_from_console():
    n = get_points_number()
    return n, get_points(n)


def get_data_from_file():
    path = get_file()
    with open(path, 'r') as file:
        data = [line for line in file.read().splitlines() if line != '']
        matrix_size = data.pop(0)

        if not valid_value(matrix_size, *valid_points_number_params):
            print('Невалидное число точек. Убедитесь, что данное значение находится в начале файла')
            return get_data_from_file()

        matrix_size = int(matrix_size)

        if len(data) != matrix_size:
            print('Неверное кол-во строк в файле')
            print('Невалидное число точек. Кол-во точек в файле не совпадает')
            return get_data_from_file()

        matrix = [line.split() for line in data]
        row_size = 2

        if any(not valid_matrix_row(row, row_size, *valid_points_values_params) for row in matrix):
            print('Невалидные значения в одной или в нескольких строках')
            return get_data_from_file()

        return matrix_size, [[float(val) for val in row] for row in matrix]


def get_data_from_function():
    print_dictionary('Функции', functions_dict)
    function_id = get_function_id()
    function = functions_dict[function_id]
    a, b = get_interval()
    n = get_points_number()
    h = (b - a) / n
    points = [[a + i * h, function(a + i * h)] for i in range(n)]
    return n, points


get_data_dict = {
    CONSOLE: get_data_from_console,
    FILE: get_data_from_file,
    FUNCTION: get_data_from_function
}


def get_data(input_mode_id):
    return get_data_dict[input_mode_id]()
