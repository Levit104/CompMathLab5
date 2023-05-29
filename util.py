import itertools
import math


def get_finite_diffs(y, n):
    diff = [[yi for yi in y]]
    for i in range(1, n):
        row = []
        for j in range(n - i):
            row.append(diff[i - 1][j + 1] - diff[i - 1][j])
        diff.append(row)
    return diff


def transpose_matrix(matrix):
    return [list(row) for row in itertools.zip_longest(*matrix)]


def separate_columns(matrix):
    return [list(row) for row in zip(*matrix)]


def has_duplicates(lst):
    return len(lst) != len(set(lst))


def linspace(a, b, n):
    delta = (b - a) / (n - 1)
    return [a + i * delta for i in range(n)]


def sort_by_column(matrix, col):
    matrix.sort(key=lambda x: x[col])


def equally_spaced(lst):
    diff = lst[1] - lst[0]
    return all(math.isclose(lst[i] - lst[i - 1], diff) for i in range(2, len(lst)))


def print_methods_diffs(diffs_dict):
    if len(diffs_dict) < 2:
        return
    was = []
    print()
    for key1 in diffs_dict:
        for key2 in diffs_dict:
            diff = diffs_dict[key1] - diffs_dict[key2]
            if key1 != key2 and f'({key2}) и ({key1})' not in was:
                was.append(f'({key1}) и ({key2})')
                print(f"Разница между ({key1}) и ({key2}): {abs(diff)}")


def extend_finite_diffs(matrix, x_values):
    extended_finite_diffs = []

    for i, row in enumerate(matrix):
        new_row = [i] + [x_values[i]] + row
        extended_finite_diffs.append(new_row)

    labels = ['i', 'x']
    for i in range(len(matrix)):
        if i == 0:
            labels.append('y')
        elif i == 1:
            labels.append('Δy')
        else:
            labels.append(f'Δy^{i}')

    extended_finite_diffs.insert(0, labels)

    return extended_finite_diffs
