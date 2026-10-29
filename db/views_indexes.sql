-- Представления и индексы (День 9)

-- =========================================
-- VIEW 1: v_orders_full — полная информация о заказах
-- =========================================
CREATE VIEW IF NOT EXISTS v_orders_full AS
SELECT
    o.order_id,
    o.order_date,
    u.last_name || ' ' || u.first_name ||
        COALESCE(' ' || u.middle_name, '') AS client_fio,
    SUM(oi.quantity * oi.price) AS total_sum
FROM orders o
JOIN users u ON u.user_id = o.user_id
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_id;

-- =========================================
-- VIEW 2: v_products_with_stock — товары с остатками
-- =========================================
CREATE VIEW IF NOT EXISTS v_products_with_stock AS
SELECT
    p.product_name,
    p.price,
    s.size_value,
    si.quantity_available
FROM products p
JOIN stock_items si ON si.product_id = p.product_id
JOIN sizes s ON s.size_id = si.size_id;

-- =========================================
-- VIEW 3: v_user_stats — статистика по клиентам
-- =========================================
CREATE VIEW IF NOT EXISTS v_user_stats AS
SELECT
    u.last_name || ' ' || u.first_name ||
        COALESCE(' ' || u.middle_name, '') AS client_fio,
    u.login,
    COUNT(o.order_id) AS orders_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.user_id
GROUP BY u.user_id;

-- =========================================
-- Индексы
-- =========================================

-- Шаг 5. Индекс на products.category
CREATE INDEX IF NOT EXISTS idx_products_category
    ON products(category);

-- Шаг 6. Индекс на orders.order_date
CREATE INDEX IF NOT EXISTS idx_orders_order_date
    ON orders(order_date);

-- Шаг 7. Индексы на внешние ключи
CREATE INDEX IF NOT EXISTS idx_orders_user_id
    ON orders(user_id);

CREATE INDEX IF NOT EXISTS idx_stock_items_product
    ON stock_items(product_id);

CREATE INDEX IF NOT EXISTS idx_stock_items_size
    ON stock_items(size_id);

-- Шаг 8. Составной индекс manufacturer + category
CREATE INDEX IF NOT EXISTS idx_products_manufacturer_category
    ON products(manufacturer, category);
