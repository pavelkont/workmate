# CSV Processor

Скрипт для обработки CSV-файла с поддержкой фильтрации и агрегации.

## Функциональность

✔ Фильтрация по колонке с операторами `=`, `<`, `>`, `<=`, `>=`  
✔ Агрегация с вычислением `avg`, `min`, `max`  
✔ Табличный вывод в консоль через `tabulate`

## Установка

Установите зависимости:

```bash
pip install tabulate
```

## Примеры запуска

```bash
python main.py --file products.csv
python main.py --file products.csv --where "rating>4.7"
python main.py --file products.csv --where "brand=apple"
python main.py --file products.csv --aggregate "rating=avg"
python main.py --file products.csv --where "brand=xiaomi" --aggregate "rating=min"
python main.py --file products.csv --where "rating>4.5" --order-by "rating=desc"
```

## Тесты

Запуск тестов:

```bash
pytest
```

## Автор

Конторин Павел Леонидович