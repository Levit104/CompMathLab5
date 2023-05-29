import os


def valid_value(value, min_value, max_value, is_strict):
    if value == 'exit':
        raise KeyboardInterrupt
    try:
        return (min_value < float(value) < max_value) if is_strict else (min_value <= float(value) <= max_value)
    except ValueError:
        return False


def valid_matrix_row(row, row_size, *valid_row_value_params):
    if len(row) != row_size:
        return False
    return all(valid_value(val, *valid_row_value_params) for val in row)


def valid_file(path):
    return os.path.isfile(path) and os.path.getsize(path) > 0
