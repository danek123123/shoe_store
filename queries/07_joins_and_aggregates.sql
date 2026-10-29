-- Запрос 1. Вывести список всех заказов с указанием даты и ФИО клиента
-- (INNER JOIN между orders и users)
SELECT 
    o.order_id,
    o.order_date,
    u.full_name
FROM orders o
INNER JOIN users u ON o.user_id = u.user_id;

-- Запрос 2. Вывести список всех товарных позиций (stock_items) 
-- с названием модели (product_name) и значением размера (size_value)
-- (соединение трех таблиц: stock_items, products и sizes)
SELECT 
    si.stock_item_id,
    p.product_name,
    s.size_value
FROM stock_items si
INNER JOIN products p ON si.product_id = p.product_id
INNER JOIN sizes s ON si.size_id = s.size_id;

-- Запрос 3. Вывести список всех заказов, в которых есть товары, 
-- с указанием ФИО клиента и названия купленного товара
-- (соединение пяти таблиц: orders, users, order_items, stock_items, products)
SELECT 
    o.order_id,
    u.full_name,
    p.product_name
FROM orders o
INNER JOIN users u ON o.user_id = u.user_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products p ON si.product_id = p.product_id;

-- Запрос 4. Список всех пользователей и количество сделанных ими заказов
-- (LEFT JOIN). Если заказов нет, COUNT вернет 0.
SELECT 
    u.full_name,
    COUNT(o.order_id) AS orders_count
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.full_name;
-- Запрос 5. Посчитать общее количество пользователей в системе
SELECT COUNT(*) AS total_users FROM users;

-- Запрос 6. Найти среднюю цену всех товаров в каталоге
SELECT AVG(price) AS avg_price FROM products;

-- Запрос 7. Найти самый дорогой и самый дешевый товар в базе
SELECT 
    MIN(price) AS cheapest_price,
    MAX(price) AS most_expensive_price
FROM products;

-- Запрос 8. Посчитать общую сумму всех проданных товаров (выручку)
-- Умножаем количество на цену продажи в момент заказа и суммируем
SELECT 
    SUM(quantity * price) AS total_revenue 
FROM order_items;
-- Запрос 9. Количество товаров в каждой категории
SELECT 
    category,
    COUNT(*) AS models_count
FROM products
GROUP BY category;

-- Запрос 10. Список производителей и средняя цена их товаров
SELECT 
    manufacturer,
    AVG(price) AS avg_price
FROM products
GROUP BY manufacturer;

-- Запрос 11. Для каждого пользователя ФИО и общая сумма заказов
SELECT 
    u.full_name,
    SUM(oi.quantity * oi.price) AS total_spent
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY u.user_id, u.full_name;

-- Запрос 12. Статистика продаж для каждой модели обуви
SELECT 
    p.product_name,
    SUM(oi.quantity) AS total_sold_pairs
FROM order_items oi
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN products p ON si.product_id = p.product_id
GROUP BY p.product_id, p.product_name;

-- Запрос 13. Список размеров и количество товарных позиций в наличии
SELECT 
    s.size_value,
    COUNT(si.stock_item_id) AS items_available
FROM sizes s
LEFT JOIN stock_items si ON s.size_id = si.size_id
GROUP BY s.size_id, s.size_value;
-- Запрос 14. Категории, в которых больше 3 моделей
SELECT 
    category,
    COUNT(*) AS models_count
FROM products
GROUP BY category
HAVING COUNT(*) > 3;

-- Запрос 15. Клиенты, которые сделали больше 2 заказов
SELECT 
    u.full_name,
    COUNT(o.order_id) AS orders_count
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.full_name
HAVING COUNT(o.order_id) > 2;

-- Запрос 16. Модели, общая сумма продаж которых превысила 100 000 рублей
SELECT 
    p.product_name,
    SUM(oi.quantity * oi.price) AS total_sales
FROM products p
INNER JOIN stock_items si ON p.product_id = si.product_id
INNER JOIN order_items oi ON si.stock_item_id = oi.stock_item_id
GROUP BY p.product_id, p.product_name
HAVING SUM(oi.quantity * oi.price) > 100000;
-- Запрос 17. Топ-3 самых популярных размеров обуви (по количеству купленных пар)
SELECT 
    s.size_value,
    SUM(oi.quantity) AS total_sold
FROM order_items oi
INNER JOIN stock_items si ON oi.stock_item_id = si.stock_item_id
INNER JOIN sizes s ON si.size_id = s.size_id
GROUP BY s.size_id, s.size_value
ORDER BY total_sold DESC
LIMIT 3;

-- Запрос 18. Пользователи, которые ни разу ничего не заказали
SELECT 
    u.full_name,
    u.email
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE o.order_id IS NULL;

-- Запрос 19. Средний чек (средняя стоимость) одного заказа
SELECT 
    AVG(order_total) AS avg_order_value
FROM (
    SELECT 
        o.order_id,
        SUM(oi.quantity * oi.price) AS order_total
    FROM orders o
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_id
) AS subquery;

-- Запрос 20. Производитель, чьи товары принесли наибольшую выручку
SELECT 
    p.manufacturer,
    SUM(oi.quantity * oi.price) AS total_revenue
FROM products p
INNER JOIN stock_items si ON p.product_id = si.product_id
INNER JOIN order_items oi ON si.stock_item_id = oi.stock_item_id
GROUP BY p.manufacturer
ORDER BY total_revenue DESC
LIMIT 1;