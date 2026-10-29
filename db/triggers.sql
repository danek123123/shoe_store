-- Триггеры и аудит-лог (День 11)

-- =========================================
-- Таблица audit_log
-- =========================================
CREATE TABLE IF NOT EXISTS audit_log (
    log_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name  TEXT NOT NULL,
    operation   TEXT NOT NULL,
    record_id   INTEGER,
    old_value   TEXT,
    new_value   TEXT,
    changed_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- =========================================
-- Задание 1.1. Аудит изменения цен в products
-- =========================================
CREATE TRIGGER IF NOT EXISTS trg_products_price_update
AFTER UPDATE ON products
FOR EACH ROW
WHEN OLD.price != NEW.price
BEGIN
    INSERT INTO audit_log
        (table_name, operation, record_id, old_value, new_value, changed_at)
    VALUES
        ('products', 'UPDATE', OLD.product_id,
         CAST(OLD.price AS TEXT), CAST(NEW.price AS TEXT),
         datetime('now'));
END;

-- =========================================
-- Задание 1.2. Аудит удаления заказов
-- =========================================
CREATE TRIGGER IF NOT EXISTS trg_orders_delete
AFTER DELETE ON orders
FOR EACH ROW
BEGIN
    INSERT INTO audit_log
        (table_name, operation, record_id, old_value, new_value, changed_at)
    VALUES
        ('orders', 'DELETE', OLD.order_id, NULL, NULL, datetime('now'));
END;

-- =========================================
-- Задание 1.3. updated_at в users
-- =========================================
ALTER TABLE users ADD COLUMN updated_at TEXT;

CREATE TRIGGER IF NOT EXISTS trg_users_updated_at
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users
    SET updated_at = datetime('now')
    WHERE user_id = OLD.user_id;
END;

-- =========================================
-- Задание 2.1. Автосписание остатков при добавлении в order_items
-- =========================================
CREATE TRIGGER IF NOT EXISTS trg_order_items_insert
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE stock_items
    SET quantity_available = quantity_available - NEW.quantity
    WHERE stock_item_id = NEW.stock_item_id;
END;

-- =========================================
-- Задание 2.2. Запрет удаления пользователя с заказами
-- =========================================
CREATE TRIGGER IF NOT EXISTS trg_users_before_delete
BEFORE DELETE ON users
FOR EACH ROW
WHEN (SELECT COUNT(*) FROM orders WHERE user_id = OLD.user_id) > 0
BEGIN
    SELECT RAISE(ABORT, 'Нельзя удалить пользователя с активными заказами');
END;

-- =========================================
-- Задание 2.3. Проверка на отрицательное количество
-- =========================================
CREATE TRIGGER IF NOT EXISTS trg_stock_items_insert
BEFORE INSERT ON stock_items
FOR EACH ROW
WHEN NEW.quantity_available < 0
BEGIN
    SELECT RAISE(ABORT, 'Количество не может быть отрицательным');
END;
