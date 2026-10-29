"""Функции и эмуляция процедур для shoe_store (День 10)."""
import re
from datetime import datetime


def calc_order_total(price, quantity):
    """Сумма заказа: цена * количество. Если quantity <= 0 — 0."""
    if price is None or quantity is None:
        return 0
    try:
        price = float(price)
        quantity = int(quantity)
    except (TypeError, ValueError):
        return 0
    if quantity <= 0:
        return 0
    return round(price * quantity, 2)


def get_category_count(conn, category_name):
    """Количество товаров в категории."""
    try:
        cur = conn.execute(
            "SELECT COUNT(*) FROM products WHERE category = ?",
            (category_name,),
        )
        return cur.fetchone()[0]
    except Exception as e:
        print(f"Ошибка get_category_count: {e}")
        return 0


def format_phone(phone):
    """89991234567 -> +7 (999) 123-45-67."""
    if not phone:
        return phone if phone is not None else ""
    s = str(phone).strip()
    digits = re.sub(r"\D", "", s)
    if len(digits) == 11 and digits[0] in ("7", "8"):
        return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    return s


def create_order(conn, user_id, stock_item_id, quantity):
    """Создаёт заказ, если остатка хватает."""
    cur = conn.cursor()
    try:
        row = cur.execute(
            "SELECT quantity_available, product_id FROM stock_items "
            "WHERE stock_item_id = ?",
            (stock_item_id,),
        ).fetchone()
        if row is None:
            print(f"Ошибка: stock_item_id={stock_item_id} не найден")
            return False
        if row["quantity_available"] < quantity:
            print(f"Ошибка: остаток {row['quantity_available']}, запрошено {quantity}")
            return False
        price = cur.execute(
            "SELECT price FROM products WHERE product_id = ?",
            (row["product_id"],),
        ).fetchone()["price"]
        cur.execute(
            "INSERT INTO orders (order_date, user_id) VALUES (?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id),
        )
        order_id = cur.lastrowid
        cur.execute(
            "INSERT INTO order_items (order_id, stock_item_id, quantity, price) "
            "VALUES (?, ?, ?, ?)",
            (order_id, stock_item_id, quantity, price),
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка create_order: {e}")
        conn.rollback()
        return False


def update_stock(conn, stock_item_id, quantity_sold):
    """Списывает количество со склада. При отрицательном остатке — rollback."""
    try:
        cur = conn.cursor()
        current = cur.execute(
            "SELECT quantity_available FROM stock_items WHERE stock_item_id = ?",
            (stock_item_id,),
        ).fetchone()
        if current is None:
            raise ValueError(f"stock_item_id={stock_item_id} не найден")
        new_value = current["quantity_available"] - quantity_sold
        if new_value < 0:
            raise ValueError(
                f"Недостаточно товара: остаток {current['quantity_available']}, "
                f"списание {quantity_sold}"
            )
        cur.execute(
            "UPDATE stock_items SET quantity_available = ? WHERE stock_item_id = ?",
            (new_value, stock_item_id),
        )
        conn.commit()
        return True
    except ValueError as e:
        print(f"ValueError: {e}")
        conn.rollback()
        return False


def get_sales_report(conn, start_date, end_date):
    """Возвращает строку с суммой продаж за период."""
    try:
        cur = conn.execute(
            "SELECT SUM(oi.quantity * oi.price) AS total "
            "FROM orders o JOIN order_items oi ON oi.order_id = o.order_id "
            "WHERE o.order_date BETWEEN ? AND ?",
            (start_date, end_date + " 23:59:59"),
        )
        total = cur.fetchone()["total"] or 0
        return f"С {start_date} по {end_date} продано товаров на сумму {total:.2f} руб."
    except Exception as e:
        print(f"Ошибка get_sales_report: {e}")
        return f"С {start_date} по {end_date} продано товаров на сумму 0.00 руб."


def register_functions(conn):
    conn.create_function("calculate_total", 2, calc_order_total)
    conn.create_function("format_phone", 1, format_phone)


if __name__ == "__main__":
    import sqlite3
    c = sqlite3.connect("db/shoe_store.sqlite")
    c.row_factory = sqlite3.Row
    register_functions(c)
    print("=== Блок 1: функции ===")
    print("calc_order_total(1000, 3) =", calc_order_total(1000, 3))
    print("calc_order_total(1000, 0) =", calc_order_total(1000, 0))
    print("format_phone('89991234567') =", format_phone("89991234567"))
    print("format_phone('123') =", format_phone("123"))
    print("get_category_count('мужская') =", get_category_count(c, "мужская"))
    print("\n=== Блок 2: процедуры ===")
    print("create_order(c, 1, 1, 2) =", create_order(c, 1, 1, 2))
    print("update_stock(c, 1, 999) =", update_stock(c, 1, 999))
    print(get_sales_report(c, "2026-01-01", "2026-12-31"))
