"""Заполнение базы данных тестовыми данными."""
from src.db_init import get_connection, create_tables

def clear_all(conn):
    for t in ("order_items", "orders", "stock_items", "products", "sizes", "users", "roles"):
        conn.execute(f"DELETE FROM {t}")
    conn.execute("DELETE FROM sqlite_sequence WHERE name IN ('order_items','orders','stock_items','products','sizes','users','roles')")
    conn.commit()

def seed_roles(conn):
    conn.executemany("INSERT INTO roles (name) VALUES (?)", [("admin",), ("manager",), ("user",)])
    conn.commit()

def seed_users(conn):
    roles = {r["name"]: r["role_id"] for r in conn.execute("SELECT role_id, name FROM roles")}
    conn.executemany(
        "INSERT INTO users (last_name, first_name, middle_name, login, role_id) VALUES (?, ?, ?, ?, ?)",
        [
            ("Админов", "Алексей", "Алексеевич", "admin", roles["admin"]),
            ("Менеджеров", "Михаил", None, "manager", roles["manager"]),
            ("Пользователев", "Пётр", None, "user", roles["user"]),
        ]
    )
    conn.commit()

def seed_products(conn):
    conn.executemany(
        "INSERT INTO products (product_name, category, subcategory, manufacturer, image_path, composition, description, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        [
            ("Nike Air Max", "мужская", "кроссовки", "Nike", "images/nike.jpg", "кожа", "Спортивные", 8990.0),
            ("Adidas Ultraboost", "мужская", "кроссовки", "Adidas", "images/adidas.jpg", "текстиль", "Бег", 12490.0),
            ("Ecco Soft 7", "женская", "кроссовки", "Ecco", "images/ecco.jpg", "кожа", "Городские", 10990.0),
            ("Ralf Ringer Classic", "мужская", "туфли", "Ralf Ringer", "images/ralf.jpg", "кожа", "Классика", 7490.0),
            ("Crocs Classic", "детская", "сандалии", "Crocs", "images/crocs.jpg", "EVA", "Лёгкие", 2990.0),
        ]
    )
    conn.commit()

def seed_sizes(conn):
    conn.executemany("INSERT INTO sizes (size_value) VALUES (?)", [(36.0,), (37.0,), (38.0,), (39.0,), (40.0,)])
    conn.commit()

def seed_stock_items(conn):
    products = {r["product_name"]: r["product_id"] for r in conn.execute("SELECT product_id, product_name FROM products")}
    sizes = {r["size_value"]: r["size_id"] for r in conn.execute("SELECT size_id, size_value FROM sizes")}
    
    data = [
        (products["Nike Air Max"], sizes[36.0], 5), (products["Nike Air Max"], sizes[37.0], 3),
        (products["Adidas Ultraboost"], sizes[37.0], 2), (products["Adidas Ultraboost"], sizes[38.0], 4),
        (products["Ecco Soft 7"], sizes[36.0], 6), (products["Ecco Soft 7"], sizes[39.0], 1),
        (products["Ralf Ringer Classic"], sizes[37.0], 3), (products["Ralf Ringer Classic"], sizes[40.0], 5),
        (products["Crocs Classic"], sizes[36.0], 10), (products["Crocs Classic"], sizes[38.0], 8),
    ]
    conn.executemany("INSERT INTO stock_items (product_id, size_id, quantity_available) VALUES (?, ?, ?)", data)
    conn.commit()

def seed_orders(conn):
    users = {r["login"]: r["user_id"] for r in conn.execute("SELECT user_id, login FROM users")}
    conn.executemany(
        "INSERT INTO orders (order_date, user_id) VALUES (?, ?)",
        [
            ("2026-10-10 10:15:00", users["user"]),
            ("2026-10-11 14:30:00", users["manager"]),
            ("2026-10-12 09:05:00", users["admin"]),
        ]
    )
    conn.commit()

def seed_order_items(conn):
    stock_items = [r["stock_item_id"] for r in conn.execute("SELECT stock_item_id FROM stock_items ORDER BY stock_item_id")]
    orders = [r["order_id"] for r in conn.execute("SELECT order_id FROM orders ORDER BY order_id")]
    
    data = [
        (orders[0], stock_items[0], 1, 8990.0), (orders[0], stock_items[2], 2, 12490.0),
        (orders[1], stock_items[4], 1, 10990.0), (orders[1], stock_items[6], 1, 7490.0),
        (orders[2], stock_items[8], 3, 2990.0), (orders[2], stock_items[9], 1, 2990.0),
    ]
    conn.executemany("INSERT INTO order_items (order_id, stock_item_id, quantity, price) VALUES (?, ?, ?, ?)", data)
    conn.commit()

def seed_all():
    create_tables()
    with get_connection() as conn:
        clear_all(conn)
        seed_roles(conn)
        seed_users(conn)
        seed_products(conn)
        seed_sizes(conn)
        seed_stock_items(conn)
        seed_orders(conn)
        seed_order_items(conn)
        print("OK: База заполнена тестовыми данными.")

if __name__ == "__main__":
    seed_all()
