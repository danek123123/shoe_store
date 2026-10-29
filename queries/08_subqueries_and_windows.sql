-- Запрос 1. Товары дороже средней цены
SELECT product_name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- Запрос 2. Клиент с самым дорогим заказом
SELECT u.last_name || ' ' || u.first_name AS client_fio
FROM users u
WHERE u.user_id = (
    SELECT o.user_id
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY o.order_id
    ORDER BY SUM(oi.quantity * oi.price) DESC
    LIMIT 1
);

-- Запрос 3. Клиенты, у которых есть хотя бы один заказ (IN)
SELECT last_name
FROM users
WHERE user_id IN (SELECT DISTINCT user_id FROM orders);

-- Запрос 4. Пользователи без заказов (NOT EXISTS)
SELECT last_name || ' ' || first_name AS client_fio
FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.user_id
);

-- Запрос 5. Товары, которые ни разу не заказывали (NOT IN)
SELECT product_name
FROM products
WHERE product_id NOT IN (
    SELECT DISTINCT si.product_id
    FROM order_items oi
    JOIN stock_items si ON si.stock_item_id = oi.stock_item_id
);

-- Запрос 6. Клиенты и суммы их заказов с рангом (RANK)
SELECT
    u.last_name || ' ' || u.first_name AS client_fio,
    SUM(oi.quantity * oi.price) AS total_spent,
    RANK() OVER (ORDER BY SUM(oi.quantity * oi.price) DESC) AS spent_rank
FROM users u
JOIN orders o ON o.user_id = u.user_id
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY u.user_id;

-- Запрос 7. Порядковый номер заказа каждого клиента (ROW_NUMBER)
SELECT
    o.order_id,
    u.last_name || ' ' || u.first_name AS client_fio,
    ROW_NUMBER() OVER (
        PARTITION BY u.user_id
        ORDER BY o.order_date ASC, o.order_id ASC
    ) AS order_sequence
FROM orders o
JOIN users u ON u.user_id = o.user_id
ORDER BY u.user_id, order_sequence;

-- Запрос 8. Нумерация товаров внутри категории по убыванию цены
SELECT
    product_name,
    category,
    price,
    ROW_NUMBER() OVER (
        PARTITION BY category
        ORDER BY price DESC
    ) AS price_rank
FROM products
ORDER BY category, price_rank;

-- Запрос 9. Самый дорогой товар в каждой категории
SELECT product_name, category, price
FROM (
    SELECT
        product_name,
        category,
        price,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY price DESC
        ) AS rn
    FROM products
) AS ranked
WHERE rn = 1;

-- Запрос 10. Нарастающий итог выручки по датам
SELECT
    o.order_date,
    SUM(oi.quantity * oi.price) AS daily_revenue,
    SUM(SUM(oi.quantity * oi.price))
        OVER (ORDER BY o.order_date) AS cumulative_revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_date
ORDER BY o.order_date;

-- Запрос 11. Дата предыдущего заказа клиента и разница в днях (LAG)
SELECT
    u.last_name || ' ' || u.first_name AS client_fio,
    o.order_date,
    LAG(o.order_date) OVER (
        PARTITION BY u.user_id
        ORDER BY o.order_date
    ) AS previous_order_date,
    julianday(o.order_date) -
        LAG(julianday(o.order_date)) OVER (
            PARTITION BY u.user_id
            ORDER BY o.order_date
        ) AS days_since_last
FROM orders o
JOIN users u ON u.user_id = o.user_id
ORDER BY u.user_id, o.order_date;
