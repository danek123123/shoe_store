# Анализ запросов через EXPLAIN QUERY PLAN (День 9)

## Созданные индексы

| Индекс | Таблица | Поле | Назначение |
|---|---|---|---|
| idx_products_category | products | category | фильтрация по категории |
| idx_orders_order_date | orders | order_date | сортировка по дате |
| idx_orders_user_id | orders | user_id | JOIN с users |
| idx_stock_items_product | stock_items | product_id | JOIN с products |
| idx_stock_items_size | stock_items | size_id | JOIN с sizes |
| idx_products_manufacturer_category | products | manufacturer, category | составной индекс |

## 1. Поиск по категории

Запрос:

    EXPLAIN QUERY PLAN
    SELECT * FROM products WHERE category = 'мужская';

План: база использует индекс `idx_products_category`.

## 2. Поиск по производителю

Запрос:

    EXPLAIN QUERY PLAN
    SELECT * FROM products WHERE manufacturer = 'Nike';

План: используется составной индекс `idx_products_manufacturer_category`
(первое поле — manufacturer).

## 3. JOIN orders + users

Запрос:

    EXPLAIN QUERY PLAN
    SELECT * FROM orders o JOIN users u ON o.user_id = u.user_id;

План: используется индекс `idx_orders_user_id` для соединения.


## 4. Попытка обновления представления

Запрос:

    CREATE VIEW v_simple AS SELECT product_id, price FROM products;
    UPDATE v_simple SET price = 100 WHERE product_id = 1;

Результат:

    sqlite3.OperationalError: cannot modify v_simple because it is a view

Вывод: представление v_simple, даже простое (одна таблица без агрегатов),
**нельзя обновить напрямую** в SQLite через UPDATE. SQLite разрешает
обновление VIEW только при выполнении жёстких условий (INSTEAD OF-триггеры
или определённые виды VIEW), которых здесь нет.

Сложные представления (v_orders_full, v_products_with_stock, v_user_stats)
с JOIN и GROUP BY — тем более не обновляются.

## 5. Вывод

**Когда индекс ускоряет:**

- поле в WHERE;
- поле в JOIN;
- поле в ORDER BY.

**Когда база игнорирует индекс:**

- функция от поля в WHERE (например, `length(name) > 0`);
- таблица маленькая (5 строк) — сканирование быстрее;
- поле не первое в составном индексе.
