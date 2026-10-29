-- 1. Товары с ценой и ценой со скидкой 20%
SELECT product_id, product_name, price,
       calc_discount(price, 20) AS price_with_discount
FROM products;

-- 2. ФИО клиентов, у которых отчество не указано
SELECT user_id, format_full_name(last_name, first_name, middle_name) AS fio
FROM users
WHERE middle_name IS NULL OR middle_name = '';

-- 3. Количество проданных единиц товара в каждом заказе
SELECT oi.order_id, pluralize_items(oi.quantity) AS items_text
FROM order_items oi;

-- 4. Сумма заказа клиента со скидкой 10%
SELECT
    format_full_name(u.last_name, u.first_name, u.middle_name) AS fio,
    SUM(oi.quantity * oi.price) AS total,
    calc_discount(SUM(oi.quantity * oi.price), 10) AS total_with_discount
FROM users u
JOIN orders o ON o.user_id = u.user_id
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY u.user_id;

-- 5. Аналитика: ФИО, общая сумма, уровень клиента, дни с первого заказа
SELECT
    format_full_name(u.last_name, u.first_name, u.middle_name) AS fio,
    SUM(oi.quantity * oi.price) AS total_spent,
    get_client_tier(SUM(oi.quantity * oi.price)) AS tier,
    get_client_loyalty_days(MIN(o.order_date)) AS loyalty_days
FROM users u
JOIN orders o ON o.user_id = u.user_id
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY u.user_id;
