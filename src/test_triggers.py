"""Проверка работы триггеров (День 11)."""
import sqlite3
from datetime import datetime


def main():
    c = sqlite3.connect('db/shoe_store.sqlite')
    c.row_factory = sqlite3.Row

    print("=== 1. Проверка автосписания остатков ===")
    # остаток до
    before = c.execute(
        "SELECT quantity_available FROM stock_items WHERE stock_item_id = 1"
    ).fetchone()["quantity_available"]
    print(f"Остаток до: {before}")

    # создаём заказ и позицию
    c.execute(
        "INSERT INTO orders (order_date, user_id) VALUES (?, 1)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),),
    )
    oid = c.execute("SELECT last_insert_rowid()").fetchone()[0]
    c.execute(
        "INSERT INTO order_items (order_id, stock_item_id, quantity, price) "
        "VALUES (?, 1, 2, 8990)",
        (oid,),
    )
    c.commit()

    after = c.execute(
        "SELECT quantity_available FROM stock_items WHERE stock_item_id = 1"
    ).fetchone()["quantity_available"]
    print(f"Остаток после: {after}")
    if after == before - 2:
        print("[PASS] триггер автосписания работает")
    else:
        print("[FAIL] триггер автосписания НЕ работает")

    print("\n=== 2. Проверка запрета удаления пользователя с заказами ===")
    try:
        c.execute("DELETE FROM users WHERE user_id = 1")
        print("[FAIL] удаление прошло без ошибки")
    except sqlite3.IntegrityError as e:
        print(f"[PASS] удаление запрещено: {e}")
    except Exception as e:
        print(f"[PASS] ошибка: {e}")

    print("\n=== 3. Проверка триггера аудита цен ===")
    c.execute("UPDATE products SET price = price + 100 WHERE product_id = 1")
    c.commit()
    log = c.execute(
        "SELECT * FROM audit_log WHERE table_name = 'products' ORDER BY log_id DESC LIMIT 1"
    ).fetchone()
    if log:
        print(f"[PASS] запись в audit_log: {dict(log)}")
    else:
        print("[FAIL] запись в audit_log не создана")

    print("\n=== 4. audit_log — первые 5 записей ===")
    for r in c.execute("SELECT * FROM audit_log ORDER BY log_id LIMIT 5"):
        print(dict(r))

    c.close()


if __name__ == "__main__":
    main()
