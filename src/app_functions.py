"""Пользовательские функции и процедуры для shoe_store (День 10)."""
from datetime import datetime


# ---------- БЛОК 1. Обработка данных ----------

def calc_discount(price, discount_percent):
    """Считает цену со скидкой. Возвращает float, округлённый до 2 знаков."""
    if price is None or discount_percent is None:
        return 0.0
    try:
        price = float(price)
        discount_percent = float(discount_percent)
    except (TypeError, ValueError):
        return 0.0

    if discount_percent < 0:
        discount_percent = 0
    if discount_percent > 100:
        discount_percent = 100

    result = price * (1 - discount_percent / 100)
    return round(result, 2)

def pluralize_items(count):
    """Склонение слова «товар»: 1 товар, 2 товара, 5 товаров."""
    if count is None:
        return "0 товаров"
    try:
        n = int(count)
    except (TypeError, ValueError):
        return "0 товаров"

    n = abs(n) % 100
    last = n % 10

    if 11 <= n <= 19:
        return f"{count} товаров"
    if last == 1:
        return f"{count} товар"
    if 2 <= last <= 4:
        return f"{count} товара"
    return f"{count} товаров"

def format_full_name(last, first, middle):
    """Возвращает «Фамилия И.О.». Если last или first пусты — «Аноним»."""
    if not last or not first:
        return "Аноним"

    last = str(last).strip().capitalize()
    first = str(first).strip()
    middle = str(middle).strip() if middle else ""

    initials = first[0].upper() + "."
    if middle:
        initials += middle[0].upper() + "."

    return f"{last} {initials}"


# ---------- БЛОК 2. Процедуры: заказы и транзакции ----------

def place_order(conn, user_id, product_id, size_id, quantity):
    """Создаёт заказ: проверяет пользователя, наличие, списывает остаток.
    Возвращает True при успехе, False — при ошибке (с откатом)."""
    cur = conn.cursor()
    try:
        # 1. Пользователь существует?
        row = cur.execute(
            "SELECT user_id FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        if row is None:
            return False

        # 2. Найти stock_item_id
        row = cur.execute(
            "SELECT stock_item_id, quantity_available "
            "FROM stock_items WHERE product_id = ? AND size_id = ?",
            (product_id, size_id),
        ).fetchone()
        if row is None:
            return False
        stock_item_id = row["stock_item_id"]
        available = row["quantity_available"]

        # 3. Хватает ли остатка?
        if available < quantity:
            print(f"Ошибка: остаток {available}, запрошено {quantity}")
            return False

        # 4. Цена товара
        price = cur.execute(
            "SELECT price FROM products WHERE product_id = ?", (product_id,)
        ).fetchone()["price"]

        # 5. Вставить заказ
        cur.execute(
            "INSERT INTO orders (order_date, user_id) VALUES (?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id),
        )
        order_id = cur.lastrowid

        # 6. Вставить позицию
        cur.execute(
            "INSERT INTO order_items (order_id, stock_item_id, quantity, price) "
            "VALUES (?, ?, ?, ?)",
            (order_id, stock_item_id, quantity, price),
        )

        # 7. Списать остаток
        cur.execute(
            "UPDATE stock_items SET quantity_available = quantity_available - ? "
            "WHERE stock_item_id = ?",
            (quantity, stock_item_id),
        )

        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка в place_order: {e}")
        conn.rollback()
        return False

def cancel_order(conn, order_id):
    """Отменяет заказ: возвращает остатки, удаляет позиции и заказ."""
    cur = conn.cursor()
    try:
        row = cur.execute(
            "SELECT order_id FROM orders WHERE order_id = ?", (order_id,)
        ).fetchone()
        if row is None:
            return False

        # Возврат остатков
        items = cur.execute(
            "SELECT stock_item_id, quantity FROM order_items WHERE order_id = ?",
            (order_id,),
        ).fetchall()

        for it in items:
            cur.execute(
                "UPDATE stock_items SET quantity_available = quantity_available + ? "
                "WHERE stock_item_id = ?",
                (it["quantity"], it["stock_item_id"]),
            )

        cur.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
        cur.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))

        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка в cancel_order: {e}")
        conn.rollback()
        return False


# ---------- БЛОК 3. Аналитика ----------

def get_client_tier(total_spent):
    """Определяет уровень клиента по сумме покупок."""
    if total_spent is None:
        return "Без статуса"
    try:
        total = float(total_spent)
    except (TypeError, ValueError):
        return "Без статуса"

    if total < 0:
        return "Без статуса"
    if total < 5000:
        return "Новичок"
    if total < 20000:
        return "Бронза"
    if total < 50000:
        return "Серебро"
    if total < 100000:
        return "Золото"
    return "Платина"

def get_client_loyalty_days(first_order_date_str):
    """Считает дни с первого заказа. Принимает 'YYYY-MM-DD' или 'YYYY-MM-DD HH:MM:SS'."""
    if not first_order_date_str:
        return 0
    try:
        s = str(first_order_date_str)
        date_part = s.split(" ")[0]
        first = datetime.strptime(date_part, "%Y-%m-%d")
        return (datetime.now() - first).days
    except (ValueError, TypeError):
        return 0

def register_functions(conn):
    """Регистрирует все функции в SQLite."""
    conn.create_function("calc_discount", 2, calc_discount)
    conn.create_function("pluralize_items", 1, pluralize_items)
    conn.create_function("format_full_name", 3, format_full_name)
    conn.create_function("get_client_tier", 1, get_client_tier)
    conn.create_function("get_client_loyalty_days", 1, get_client_loyalty_days)
