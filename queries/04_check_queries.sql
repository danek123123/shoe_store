-- 1. Список всех ролей
SELECT * FROM roles;

-- 2. Список всех пользователей с ролями
SELECT u.user_id, u.last_name, u.first_name, r.name AS role
FROM users u JOIN roles r ON r.role_id = u.role_id;

-- 3. Список всех товаров
SELECT product_id, product_name, category, price FROM products;

-- 4. Список всех размеров
SELECT * FROM sizes;

-- 5. Список всех заказов с ФИО клиентов
SELECT o.order_id, o.order_date, u.last_name, u.first_name
FROM orders o JOIN users u ON u.user_id = o.user_id;

-- 6. Список всех товарных позиций с наименованием и размером
SELECT si.stock_item_id, p.product_name, s.size_value, si.quantity_available
FROM stock_items si
JOIN products p ON p.product_id = si.product_id
JOIN sizes s ON s.size_id = si.size_id;
