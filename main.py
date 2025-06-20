import argparse
from csv_handler import load_csv, filter_rows, aggregate_column
from tabulate import tabulate
import sys


def parse_condition(condition: str):
    for op in ('>=', '<=', '>', '<', '='):
        if op in condition:
            field, value = condition.split(op)
            return field.strip(), op, value.strip()
    raise ValueError("Некорректное условие фильтрации")


def parse_aggregation(aggregation: str):
    if '=' not in aggregation:
        raise ValueError("Некорректный формат агрегации")
    column, func = aggregation.split('=')
    return column.strip(), func.strip()


def _cast_sort_key(value):
    try:
        return float(value)
    except ValueError:
        return value.lower()


def main():
    parser = argparse.ArgumentParser(description="Обработка CSV-файла")
    parser.add_argument("--file", required=True, help="Путь к CSV-файлу")
    parser.add_argument("--where", help="Условие фильтрации, например rating>4.5")
    parser.add_argument("--aggregate", help="Агрегация, например rating=avg")
    parser.add_argument("--order-by", help="Сортировка, например rating=desc")

    args = parser.parse_args()

    try:
        rows = load_csv(args.file)

        if args.where:
            field, op, value = parse_condition(args.where)
            rows = filter_rows(rows, field, op, value)

        if args.order_by:
            if '=' not in args.order_by:
                raise ValueError("Неверный формат сортировки. Ожидается: колонка=asc|desc")
            field, direction = args.order_by.split('=')
            field, direction = field.strip(), direction.strip().lower()
            if direction not in ('asc', 'desc'):
                raise ValueError("Сортировка поддерживает только 'asc' или 'desc'")
            rows.sort(key=lambda row: _cast_sort_key(row[field]), reverse=(direction == 'desc'))

        if args.aggregate:
            column, func = parse_aggregation(args.aggregate)
            if not rows:
                raise ValueError("Нет данных для агрегации после фильтрации")
            result = aggregate_column(rows, column, func)
            print(tabulate([[result]], headers=[func], tablefmt="grid"))
        else:
            print(tabulate(rows, headers="keys", tablefmt="grid"))

    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
