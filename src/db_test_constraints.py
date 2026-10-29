"""Проверка ограничений целостности."""
import sqlite3
from src.db_init import get_connection

def expect_error(label, sql, params=()):
    try:
        with get_connection() as conn:
            conn.execute(sql, params)
            conn.commit()
        print(f"| {label} | ошибка | ошибки не было | не пройден |")
    except sqlite3.Error as e:
        print(f"| {label} | ошибка | {e} | пройден |")

def test_check_price():
    expect_error("CHECK на price", "INSERT INTO products (product_name, category, manufacturer, price) VALUES ('X', 'x', 'x', -100)")

def test_check_quantity():
    expect_error("CHECK на quantity", "INSERT INTO stock_items (product_id, size_id, quantity_available) VALUES (1, 1, -5)")

def test_foreign_key():
    expect_error("FOREIGN KEY на role_id", "INSERT INTO users (last_name, first_name, login, role_id) VALUES ('X', 'Y', 'fktest', 999)")

def test_on_delete_restrict():
    expect_error("ON DELETE RESTRICT", "DELETE FROM roles WHERE role_id = 1")

def test_on_delete_cascade():
    with get_connection() as conn:
        conn.execute("INSERT INTO orders (order_date, user_id) VALUES ('2026-10-20', 1)")
        oid = conn.execute("SELECT MAX(order_id) AS m FROM orders").fetchone()["m"]
        conn.execute("INSERT INTO order_items (order_id, stock_item_id, quantity, price) VALUES (?, 1, 1, 100)", (oid,))
        conn.commit()
        conn.execute("DELETE FROM orders WHERE order_id = ?", (oid,))
        conn.commit()
        left = conn.execute("SELECT COUNT(*) AS c FROM order_items WHERE order_id = ?", (oid,)).fetchone()["c"]
        if left == 0:
            print(f"| ON DELETE CASCADE | каскадное удаление | позиции удалены | пройден |")
        else:
            print(f"| ON DELETE CASCADE | каскадное удаление | позиции остались | не пройден |")

if __name__ == "__main__":
    print("| Ограничение | Ожидаемый результат | Фактический результат | Статус |")
    print("|---|---|---|---|")
    test_check_price()
    test_check_quantity()
    test_foreign_key()
    test_on_delete_restrict()
    test_on_delete_cascade()
