# Отчёт по схеме базы данных (черновик)

Список всех таблиц в порядке создания с полным описанием:
поля, первичный ключ, внешние ключи, ограничения, индексы.

## 1. roles — справочник ролей

Поля: role_id, name.
PK: role_id. UNIQUE: name.
Ограничения: PRIMARY KEY, NOT NULL, UNIQUE.
Индексы: нет отдельных (UNIQUE name создаёт автоматический).

## 2. sizes — справочник размеров

Поля: size_id, value.
PK: size_id. UNIQUE: value.
CHECK: value > 20 AND value < 50.
Индексы: нет отдельных (UNIQUE value создаёт автоматический).

## 3. products — каталог товаров

Поля: product_id, name, category, subcategory, manufacturer,
image_path, composition, description, price.
PK: product_id. FK: нет.
CHECK: length(name) > 0; price > 0 AND price < 1000000.
Индексы: idx_products_category, idx_products_manufacturer,
idx_products_price.

## 4. users — пользователи системы

Поля: user_id, last_name, first_name, middle_name, login, role_id.
PK: user_id. FK: role_id → roles (RESTRICT).
UNIQUE: login. CHECK: length(login) 3–20.
Индексы: idx_users_role_id.

## 5. stock_items — товарные позиции

Поля: item_id, product_id, size_id, quantity.
PK: item_id. FK: product_id → products (RESTRICT),
size_id → sizes (RESTRICT).
UNIQUE: (product_id, size_id). CHECK: quantity >= 0.
Индексы: idx_stock_items_product, idx_stock_items_size.

## 6. orders — заказы

Поля: order_id, order_date, user_id.
PK: order_id. FK: user_id → users (RESTRICT).
DEFAULT: order_date = текущая дата. CHECK: date(order_date)
IS NOT NULL.
Индексы: idx_orders_user_id, idx_orders_order_date.

## 7. order_items — состав заказов

Поля: order_item_id, order_id, item_id, quantity, price.
PK: order_item_id. FK: order_id → orders (CASCADE),
item_id → stock_items (RESTRICT).
CHECK: quantity > 0; price > 0.
Индексы: idx_order_items_order, idx_order_items_item.

## Сводная таблица

| № | Таблица | PK | FK | CHECK | Индексы |
|---|---|---|---|---|---|
| 1 | roles | role_id | — | — | (UNIQUE) |
| 2 | sizes | size_id | — | value | (UNIQUE) |
| 3 | products | product_id | — | name, price | 3 |
| 4 | users | user_id | role_id | login | 1 |
| 5 | stock_items | item_id | product_id, size_id | quantity | 2 |
| 6 | orders | order_id | user_id | date | 2 |
| 7 | order_items | order_item_id | order_id, item_id | quantity, price | 2 |

## Порядок создания

1. roles
2. sizes
3. products
4. users
5. stock_items
6. orders
7. order_items

Такой порядок гарантирует, что к моменту создания дочерней
таблицы родительская уже существует.
