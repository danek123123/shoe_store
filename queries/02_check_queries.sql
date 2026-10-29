-- Список всех пользователей с ролями
SELECT u.user_id, u.last_name, u.first_name, u.middle_name, u.login, r.name AS role
FROM users u
JOIN roles r ON r.role_id = u.role_id
ORDER BY u.user_id;

-- Список всех товаров
SELECT product_id, name, category, subcategory, manufacturer, price, image_path
FROM products
ORDER BY product_id;

-- Список всех размеров
SELECT size_id, value
FROM sizes
ORDER BY value;

-- Список всех заказов с ФИО клиентов
SELECT o.order_id, o.order_date,
       u.last_name || ' ' || u.first_name ||
       COALESCE(' ' || u.middle_name, '') AS client_fio
FROM orders o
JOIN users u ON u.user_id = o.user_id
ORDER BY o.order_id;

-- Список всех товарных позиций с наименованием товара и размером
SELECT si.item_id, p.product_name AS product_name, s.value AS size_value, si.quantity
FROM stock_items si
JOIN products p ON p.product_id = si.product_id
JOIN sizes    s ON s.size_id    = si.size_id
ORDER BY si.item_id;
