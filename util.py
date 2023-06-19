import math
from itertools import zip_longest
from typing import Any
from tabulate import tabulate


def calculate_finite_diffs(y_values: list[float], n: int) -> list[list[float]]:
    diffs: list[list[float]] = [[y for y in y_values]]
    for i in range(1, n):
        row: list[float] = []
        for j in range(n - i):
            row.append(diffs[i - 1][j + 1] - diffs[i - 1][j])
        diffs.append(row)
    return diffs


def print_finite_diffs(x_values: list[float],
                       finite_diffs: list[list[float]],
                       points_number: int,
                       table_format: str = 'fancy_grid',
                       float_format: str = '.5f',
                       align: str = 'decimal',
                       show_index: bool = True) -> None:
    table: list[list[float]] = transpose([x_values] + finite_diffs)
    headers: list[str] = ['i', 'x', 'y', 'Δy'] + [f'Δy^{i}' for i in range(2, points_number)]
    print(f'\nКонечные разности:'
          f'\n{table_to_string(table, headers, table_format, float_format, align, show_index)}')


def print_methods_diffs(diffs_dict: dict[str, float], float_format: str) -> None:
    if len(diffs_dict) < 2:
        return
    print()  # отступ
    printed: list[str] = []
    for name1, value1 in diffs_dict.items():
        for name2, value2 in diffs_dict.items():
            if name1 != name2 and f'({name2}) и ({name1})' not in printed:
                printed.append(f'({name1}) и ({name2})')
                print(f'Разница между ({name1}) и ({name2}): {abs(value1 - value2):{float_format}}')


def has_duplicates(lst: list[Any]) -> bool:
    return len(lst) != len(set(lst))


def linspace(a: float, b: float, n: int) -> list[float]:
    delta: float = (b - a) / (n - 1)
    return [a + i * delta for i in range(n)]


def sort_by_column(table: list[list[Any]], col: int) -> None:
    table.sort(key=lambda x: x[col])


def transpose(table: list[list[Any]]) -> list[list[Any]]:
    return [list(row) for row in zip_longest(*table)]


def equally_spaced(lst):
    diff = lst[1] - lst[0]
    return all(math.isclose(lst[i] - lst[i - 1], diff) for i in range(2, len(lst)))


def table_to_string(data: list[Any],
                    headers: list[Any],
                    table_format: str = 'fancy_grid',
                    float_format: str = '.5f',
                    align: str = 'decimal',
                    show_index: bool = True) -> str:
    table: str = tabulate(data,
                          headers=headers,
                          tablefmt=table_format,
                          floatfmt=float_format,
                          numalign=align,
                          showindex=show_index)
    return table
