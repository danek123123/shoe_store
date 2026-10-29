"""Создание базы данных shoe_store.sqlite и всех таблиц.

DDL-скрипт, исполняемый с нуля: удаляет старые таблицы
и создаёт семь таблиц заново, с ограничениями и индексами.
"""
import sqlite3
from pathlib import Path

# Шаг 17. Путь к файлу базы данных.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_DIR = PROJECT_ROOT / "db"
DB_PATH = DB_DIR / "shoe_store.sqlite"

def get_connection():
    """Шаг 18. Возвращает соединение с SQLite.

    row_factory = sqlite3.Row позволяет обращаться к полям
    по имени: row['name'] вместо row[0].
    """
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def drop_all_tables():
    """Шаг 19. Удаляет все таблицы, если они существуют.

    Позволяет пересоздавать базу с нуля при каждом запуске.
    Порядок удаления — обратный порядку создания, чтобы
    не нарушить внешние ключи.
    """
    with get_connection() as conn:
        conn.execute("PRAGMA foreign_keys = OFF")
        for table in (
            "order_items",
            "orders",
            "stock_items",
            "users",
            "products",
            "sizes",
            "roles",
        ):
            conn.execute(f"DROP TABLE IF EXISTS {table}")
        conn.commit()

def create_tables():
    """Шаг 20. Создаёт все семь таблиц в правильном порядке.

    Шаг 21. Включает PRAGMA foreign_keys = ON.
    Шаг 22. В конце — commit и close.
    """
    conn = get_connection()

    # Шаг 21. Включаем проверку внешних ключей.
    conn.execute("PRAGMA foreign_keys = ON")

    cur = conn.cursor()

    # --- 1. Справочники ---

    cur.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL UNIQUE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sizes (
            size_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            size_value REAL NOT NULL UNIQUE
                       CHECK (size_value > 20 AND size_value < 50)
        )
    """)

    # --- 2. Основные сущности ---

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL
                         CHECK (length(product_name) > 0),
            category     TEXT NOT NULL,
            subcategory  TEXT,
            manufacturer TEXT NOT NULL,
            image_path   TEXT,
            composition  TEXT,
            description  TEXT,
            price        REAL NOT NULL
                         CHECK (price > 0 AND price < 1000000)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name   TEXT NOT NULL,
            first_name  TEXT NOT NULL,
            middle_name TEXT,
            login       TEXT NOT NULL UNIQUE
                        CHECK (length(login) >= 3
                               AND length(login) <= 20),
            role_id     INTEGER NOT NULL,
            FOREIGN KEY (role_id)
                REFERENCES roles(role_id) ON DELETE RESTRICT
        )
    """)

    # --- 3. Товарные позиции ---

    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock_items (
            stock_item_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            size_id    INTEGER NOT NULL,
            quantity_available INTEGER NOT NULL DEFAULT 0
                       CHECK (quantity_available >= 0),
            UNIQUE (product_id, size_id),
            FOREIGN KEY (product_id)
                REFERENCES products(product_id) ON DELETE RESTRICT,
            FOREIGN KEY (size_id)
                REFERENCES sizes(size_id) ON DELETE RESTRICT
        )
    """)

    # --- 4. Заказы ---

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            order_date TEXT NOT NULL DEFAULT (datetime('now'))
                       CHECK (date(order_date) IS NOT NULL),
            user_id    INTEGER NOT NULL,
            FOREIGN KEY (user_id)
                REFERENCES users(user_id) ON DELETE RESTRICT
        )
    """)

    # --- 5. Состав заказов ---

    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id      INTEGER NOT NULL,
            stock_item_id INTEGER NOT NULL,
            quantity      INTEGER NOT NULL CHECK (quantity > 0),
            price         REAL NOT NULL CHECK (price > 0),
            FOREIGN KEY (order_id)
                REFERENCES orders(order_id) ON DELETE CASCADE,
            FOREIGN KEY (stock_item_id)
                REFERENCES stock_items(stock_item_id) ON DELETE RESTRICT
        )
    """)

    # --- 6. Индексы ---

    cur.execute("CREATE INDEX IF NOT EXISTS idx_users_role_id "
                "ON users(role_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_user_id "
                "ON orders(user_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_order_date "
                "ON orders(order_date)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_products_category "
                "ON products(category)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_products_manufacturer "
                "ON products(manufacturer)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_products_price "
                "ON products(price)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_stock_items_product "
                "ON stock_items(product_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_stock_items_size "
                "ON stock_items(size_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order "
                "ON order_items(order_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_order_items_stock_item "
                "ON order_items(stock_item_id)")

    # Шаг 22. Фиксируем изменения и закрываем соединение.
    conn.commit()
    conn.close()

def main():
    """Шаг 23. Точка входа: пересоздаёт базу с нуля."""
    print("Пересоздание базы данных...")
    drop_all_tables()
    create_tables()
    print(f"База данных готова: {DB_PATH}")

# Шаг 24. Запуск при выполнении скрипта напрямую.
if __name__ == "__main__":
    main()
