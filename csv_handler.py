import csv
from typing import List, Dict, Any


def load_csv(filepath: str) -> List[Dict[str, Any]]:
    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def filter_rows(rows: List[Dict[str, Any]], field: str, op: str, value: str) -> List[Dict[str, Any]]:
    def match(row_value: str) -> bool:
        if row_value.isdigit() or row_value.replace('.', '', 1).isdigit():
            row_value_cast = float(row_value)
            value_cast = float(value)
        else:
            row_value_cast = row_value
            value_cast = value

        if op == "=":
            return row_value_cast == value_cast
        elif op == ">":
            return row_value_cast > value_cast
        elif op == "<":
            return row_value_cast < value_cast
        elif op == ">=":
            return row_value_cast >= value_cast
        elif op == "<=":
            return row_value_cast <= value_cast
        else:
            raise ValueError(f"Неизвестный оператор фильтрации: {op}")

    return [row for row in rows if match(row[field])]


def aggregate_column(rows: List[Dict[str, Any]], field: str, func: str) -> float:
    values = [float(row[field]) for row in rows]

    if func == "avg":
        return round(sum(values) / len(values), 2)
    elif func == "min":
        return min(values)
    elif func == "max":
        return max(values)
    else:
        raise ValueError(f"Неподдерживаемая функция агрегации: {func}. Допустимые: avg, min, max")