"""Полная проверка ограничений: CHECK, FOREIGN KEY, CASCADE."""
from src.db_init import get_connection

def try_sql(label, sql, params=()):
    try:
        with get_connection() as conn:
            conn.execute(sql, params)
            conn.commit()
        print(f"[FAIL] {label}: прошло без ошибки")
        return False
    except Exception as e:
        print(f"[PASS] {label}: {e}")
        return True

def check_check_constraints():
    print("--- CHECK ---")
    try_sql("товар с ценой -100",
        "INSERT INTO products (name, category, subcategory, manufacturer, price) "
        "VALUES ('X', 'x', 'x', 'x', -100)")
    try_sql("товарная позиция с quantity -5",
        "INSERT INTO stock_items (product_id, size_id, quantity) "
        "VALUES (1, 1, -5)")
    try_sql("позиция заказа с quantity 0",
        "INSERT INTO order_items (order_id, item_id, quantity, price) "
        "VALUES (1, 1, 0, 100)")
    try_sql("пользователь с логином 'ab'",
        "INSERT INTO users (last_name, first_name, login, role_id) "
        "VALUES ('X', 'Y', 'ab', 1)")
    try_sql("размер 100",
        "INSERT INTO sizes (value) VALUES (100)")

def check_foreign_keys():
    print("\n--- FOREIGN KEY ---")
    try_sql("удалить роль с пользователями",
        "DELETE FROM roles WHERE role_id = 1")
    try_sql("удалить пользователя с заказами",
        "DELETE FROM users WHERE user_id = 1")
    try_sql("удалить товар с позициями",
        "DELETE FROM products WHERE product_id = 1")

def check_cascade():
    print("\n--- CASCADE ---")
    with get_connection() as conn:
        conn.execute("INSERT INTO orders (user_id) VALUES (1)")
        oid = conn.execute("SELECT MAX(order_id) AS m FROM orders").fetchone()["m"]
        conn.execute(
            "INSERT INTO order_items (order_id, item_id, quantity, price) "
            "VALUES (?, 1, 1, 100)", (oid,)
        )
        conn.commit()

        before = conn.execute(
            "SELECT COUNT(*) AS c FROM order_items WHERE order_id = ?", (oid,)
        ).fetchone()["c"]
        conn.execute("DELETE FROM orders WHERE order_id = ?", (oid,))
        conn.commit()
        after = conn.execute(
            "SELECT COUNT(*) AS c FROM order_items WHERE order_id = ?", (oid,)
        ).fetchone()["c"]

        if before == 1 and after == 0:
            print("[PASS] каскадное удаление: позиции удалены автоматически")
        else:
            print(f"[FAIL] каскад: было {before}, стало {after}")

if __name__ == "__main__":
    check_check_constraints()
    check_foreign_keys()
    check_cascade()
