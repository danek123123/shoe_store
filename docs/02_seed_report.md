# Отчёт о заполнении базы тестовыми данными

Скрипт: src/db_seed.py
Команда запуска: python -m src.db_seed

## Таблица roles (3 записи)

role_id | name
1       | admin
2       | manager
3       | user

## Таблица users (3 записи)

user_id | last_name       | first_name | middle_name | login   | role_id
1       | Админов         | Алексей    | Алексеевич  | admin   | 1
2       | Менеджеров      | Михаил     | —           | manager | 2
3       | Пользователев   | Пётр       | —           | user    | 3

## Таблица products (5 записей)

product_id | name                 | category | subcategory | manufacturer | price
1          | Nike Air Max         | мужская  | кроссовки   | Nike         | 8990
2          | Adidas Ultraboost    | мужская  | кроссовки   | Adidas       | 12490
3          | Ecco Soft 7          | женская  | кроссовки   | Ecco         | 10990
4          | Ralf Ringer Classic  | мужская  | туфли       | Ralf Ringer  | 7490
5          | Crocs Classic        | детская  | сандалии    | Crocs        | 2990

У каждого товара заполнено поле image_path — путь к изображению.

## Таблица sizes (5 записей)

size_id | value
1       | 36
2       | 37
3       | 38
4       | 39
5       | 40

## Таблица stock_items (10 записей)

item_id | product_id | size_id | quantity
1       | 1          | 1       | 5
2       | 1          | 2       | 3
3       | 2          | 2       | 2
4       | 2          | 3       | 4
5       | 3          | 1       | 6
6       | 3          | 4       | 1
7       | 4          | 2       | 3
8       | 4          | 5       | 5
9       | 5          | 1       | 10
10      | 5          | 3       | 8

Не все товары имеют все размеры: Nike Air Max — 36 и 37,
Adidas Ultraboost — 37 и 38, Ecco Soft 7 — 36 и 39,
Ralf Ringer — 37 и 40, Crocs — 36 и 38.

## Таблица orders (3 записи)

order_id | order_date           | user_id
1        | 2026-10-10 10:15:00  | 3
2        | 2026-10-11 14:30:00  | 2
3        | 2026-10-12 09:05:00  | 1

## Таблица order_items (6 записей)

order_item_id | order_id | item_id | quantity | price
1             | 1        | 1       | 1        | 8990
2             | 1        | 3       | 2        | 12490
3             | 2        | 5       | 1        | 10990
4             | 2        | 7       | 1        | 7490
5             | 3        | 9       | 3        | 2990
6             | 3        | 10      | 1        | 2990

В каждом заказе — две позиции.

## Связь заказов и пользователей (шаг 68)

В таблице orders поле user_id ссылается на users.user_id.
Это позволяет при выборке заказов определить, кто их оформил:

SELECT o.order_id, o.order_date, u.last_name, u.first_name
FROM orders o
JOIN users u ON u.user_id = o.user_id
ORDER BY o.order_id;

Результат:

order_id | order_date           | last_name        | first_name
1        | 2026-10-10 10:15:00  | Пользователев    | Пётр
2        | 2026-10-11 14:30:00  | Менеджеров       | Михаил
3        | 2026-10-12 09:05:00  | Админов          | Алексей

## Итог

Таблица      | Записей
roles        | 3
users        | 3
products     | 5
sizes        | 5
stock_items  | 10
orders       | 3
order_items  | 6
Всего        | 35

База наполнена тестовыми данными. Все ограничения целостности
соблюдены. Связи между таблицами настроены.