# Проверка структуры базы данных

**Найдено таблиц:** 7 (ожидалось 7)

## Таблица roles

- **Количество полей:** 2
- **Первичный ключ:** role_id
- **Внешние ключи:** нет
- **Индексы:** нет (только автоиндексы)
- **Ограничения:** UNIQUE, NOT NULL

| Поле | Тип | NOT NULL | DEFAULT | PK |
|---|---|---|---|---|
| role_id | INTEGER | нет | — | да |
| name | TEXT | да | — | — |

---

## Таблица sizes

- **Количество полей:** 2
- **Первичный ключ:** size_id
- **Внешние ключи:** нет
- **Индексы:** нет (только автоиндексы)
- **Ограничения:** CHECK, UNIQUE, NOT NULL

| Поле | Тип | NOT NULL | DEFAULT | PK |
|---|---|---|---|---|
| size_id | INTEGER | нет | — | да |
| size_value | REAL | да | — | — |

---

## Таблица users

- **Количество полей:** 6
- **Первичный ключ:** user_id
- **Внешние ключи:**
  - `role_id` → `roles(role_id)` (ON DELETE RESTRICT)
- **Индексы:** idx_users_role_id
- **Ограничения:** CHECK, UNIQUE, NOT NULL

| Поле | Тип | NOT NULL | DEFAULT | PK |
|---|---|---|---|---|
| user_id | INTEGER | нет | — | да |
| last_name | TEXT | да | — | — |
| first_name | TEXT | да | — | — |
| middle_name | TEXT | нет | — | — |
| login | TEXT | да | — | — |
| role_id | INTEGER | да | — | — |

---

## Таблица products

- **Количество полей:** 9
- **Первичный ключ:** product_id
- **Внешние ключи:** нет
- **Индексы:** idx_products_price, idx_products_manufacturer, idx_products_category
- **Ограничения:** CHECK, NOT NULL

| Поле | Тип | NOT NULL | DEFAULT | PK |
|---|---|---|---|---|
| product_id | INTEGER | нет | — | да |
| product_name | TEXT | да | — | — |
| category | TEXT | да | — | — |
| subcategory | TEXT | нет | — | — |
| manufacturer | TEXT | да | — | — |
| image_path | TEXT | нет | — | — |
| composition | TEXT | нет | — | — |
| description | TEXT | нет | — | — |
| price | REAL | да | — | — |

---

## Таблица stock_items

- **Количество полей:** 4
- **Первичный ключ:** stock_item_id
- **Внешние ключи:**
  - `size_id` → `sizes(size_id)` (ON DELETE RESTRICT)
  - `product_id` → `products(product_id)` (ON DELETE RESTRICT)
- **Индексы:** idx_stock_items_size, idx_stock_items_product
- **Ограничения:** CHECK, UNIQUE, NOT NULL, DEFAULT

| Поле | Тип | NOT NULL | DEFAULT | PK |
|---|---|---|---|---|
| stock_item_id | INTEGER | нет | — | да |
| product_id | INTEGER | да | — | — |
| size_id | INTEGER | да | — | — |
| quantity_available | INTEGER | да | 0 | — |

---

## Таблица orders

- **Количество полей:** 3
- **Первичный ключ:** order_id
- **Внешние ключи:**
  - `user_id` → `users(user_id)` (ON DELETE RESTRICT)
- **Индексы:** idx_orders_order_date, idx_orders_user_id
- **Ограничения:** CHECK, NOT NULL, DEFAULT

| Поле | Тип | NOT NULL | DEFAULT | PK |
|---|---|---|---|---|
| order_id | INTEGER | нет | — | да |
| order_date | TEXT | да | datetime('now') | — |
| user_id | INTEGER | да | — | — |

---

## Таблица order_items

- **Количество полей:** 5
- **Первичный ключ:** order_item_id
- **Внешние ключи:**
  - `stock_item_id` → `stock_items(stock_item_id)` (ON DELETE RESTRICT)
  - `order_id` → `orders(order_id)` (ON DELETE CASCADE)
- **Индексы:** idx_order_items_stock_item, idx_order_items_order
- **Ограничения:** CHECK, NOT NULL

| Поле | Тип | NOT NULL | DEFAULT | PK |
|---|---|---|---|---|
| order_item_id | INTEGER | нет | — | да |
| order_id | INTEGER | да | — | — |
| stock_item_id | INTEGER | да | — | — |
| quantity | INTEGER | да | — | — |
| price | REAL | да | — | — |

---

