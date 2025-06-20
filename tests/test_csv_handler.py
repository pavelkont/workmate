import pytest
from workmate.csv_handler import load_csv, filter_rows, aggregate_column
import tempfile
import os

CSV_CONTENT = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
poco x5 pro,xiaomi,299,4.4
"""

@pytest.fixture
def csv_file():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".csv", encoding="utf-8") as f:
        f.write(CSV_CONTENT)
        f.seek(0)
    yield f.name
    os.unlink(f.name)

def test_load_csv(csv_file):
    data = load_csv(csv_file)
    assert len(data) == 4
    assert data[0]["name"] == "iphone 15 pro"

def test_filter_equals(csv_file):
    data = load_csv(csv_file)
    filtered = filter_rows(data, "brand", "=", "apple")
    assert len(filtered) == 1
    assert filtered[0]["name"] == "iphone 15 pro"

def test_filter_greater_than(csv_file):
    data = load_csv(csv_file)
    filtered = filter_rows(data, "rating", ">", "4.7")
    assert len(filtered) == 2
    assert all(float(row["rating"]) > 4.7 for row in filtered)

def test_filter_less_than(csv_file):
    data = load_csv(csv_file)
    filtered = filter_rows(data, "price", "<", "300")
    assert len(filtered) == 2
    assert all(float(row["price"]) < 300 for row in filtered)

def test_filter_greater_equal(csv_file):
    data = load_csv(csv_file)
    filtered = filter_rows(data, "rating", ">=", "4.6")
    assert len(filtered) == 3
    assert all(float(row["rating"]) >= 4.6 for row in filtered)

def test_filter_less_equal(csv_file):
    data = load_csv(csv_file)
    filtered = filter_rows(data, "price", "<=", "299")
    assert len(filtered) == 2
    assert all(float(row["price"]) <= 299 for row in filtered)

def test_filter_unknown_operator(csv_file):
    data = load_csv(csv_file)
    with pytest.raises(ValueError):
        filter_rows(data, "price", "!!", "100")

def test_aggregate_avg(csv_file):
    data = load_csv(csv_file)
    result = aggregate_column(data, "rating", "avg")
    assert abs(result - 4.68) < 0.01  # округление до 2 знаков

def test_aggregate_min(csv_file):
    data = load_csv(csv_file)
    result = aggregate_column(data, "price", "min")
    assert result == 199

def test_aggregate_max(csv_file):
    data = load_csv(csv_file)
    result = aggregate_column(data, "price", "max")
    assert result == 1199

def test_aggregate_unknown_function(csv_file):
    data = load_csv(csv_file)
    with pytest.raises(ValueError):
        aggregate_column(data, "price", "median")
