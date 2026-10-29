"""Unit-тесты для app_functions (День 10)."""
from src.app_functions import (
    calc_discount, pluralize_items, format_full_name,
    get_client_tier, get_client_loyalty_days,
)

def test_calc_discount():
    assert calc_discount(1000, 20) == 800.0
    assert calc_discount(None, 20) == 0.0
    assert calc_discount(1000, None) == 0.0
    assert calc_discount(1000, -5) == 1000.0
    assert calc_discount(1000, 150) == 0.0
    assert calc_discount("abc", 20) == 0.0
    assert calc_discount(1000, 0) == 1000.0
    assert calc_discount(1000, 100) == 0.0
    assert calc_discount(999.99, 10) == 899.99
    print("[PASS] calc_discount")

def test_pluralize_items():
    assert pluralize_items(1) == "1 товар"
    assert pluralize_items(2) == "2 товара"
    assert pluralize_items(5) == "5 товаров"
    assert pluralize_items(0) == "0 товаров"
    assert pluralize_items(11) == "11 товаров"
    assert pluralize_items(21) == "21 товар"
    assert pluralize_items(None) == "0 товаров"
    assert pluralize_items("abc") == "0 товаров"
    print("[PASS] pluralize_items")

def test_format_full_name():
    assert format_full_name("иванов", "иван", "иванович") == "Иванов И.И."
    assert format_full_name("Петров", "Пётр", None) == "Петров П."
    assert format_full_name(None, "Иван", "Иванович") == "Аноним"
    assert format_full_name("", "Иван", None) == "Аноним"
    assert format_full_name("Сидоров", None, "Сидорович") == "Аноним"
    print("[PASS] format_full_name")

def test_get_client_tier():
    assert get_client_tier(None) == "Без статуса"
    assert get_client_tier(-100) == "Без статуса"
    assert get_client_tier(0) == "Новичок"
    assert get_client_tier(4999) == "Новичок"
    assert get_client_tier(5000) == "Бронза"
    assert get_client_tier(20000) == "Серебро"
    assert get_client_tier(50000) == "Золото"
    assert get_client_tier(100000) == "Платина"
    assert get_client_tier("abc") == "Без статуса"
    print("[PASS] get_client_tier")

def test_get_client_loyalty_days():
    assert get_client_loyalty_days(None) == 0
    assert get_client_loyalty_days("") == 0
    assert get_client_loyalty_days("не дата") == 0
    today = __import__("datetime").datetime.now().strftime("%Y-%m-%d")
    assert get_client_loyalty_days(today) == 0
    print("[PASS] get_client_loyalty_days")

if __name__ == "__main__":
    test_calc_discount()
    test_pluralize_items()
    test_format_full_name()
    test_get_client_tier()
    test_get_client_loyalty_days()
    print("\nВсе тесты пройдены.")
