# Отчёт о структуре базы данных

База данных: `db/shoe_store.sqlite`.
Скрипт создания: `src/db_init.py`.
Команда запуска: `python -m src.db_init`.

Создано **семь таблиц**. Внешние ключи включены
(`PRAGMA foreign_keys = ON`).

## 1. roles — справочник ролей

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| role_id | INTEGER | PK AUTOINCREMENT | Идентификатор роли |
| name | TEXT | NOT NULL, UNIQUE | Название роли |

Значения: `admin`, `manager`, `user`.

## 2. sizes — справочник размеров

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| size_id | INTEGER | PK AUTOINCREMENT | Идентификатор размера |
| value | INTEGER | NOT NULL, UNIQUE, CHECK (16–50) | Значение размера |

## 3. products — каталог моделей обуви

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| product_id | INTEGER | PK AUTOINCREMENT | Идентификатор |
| name | TEXT | NOT NULL | Наименование модели |
| category | TEXT | NOT NULL | Категория |
| subcategory | TEXT | NOT NULL | Подкатегория |
| manufacturer | TEXT | NOT NULL | Производитель |
| image_path | TEXT | NULL | Путь к изображению |
| composition | TEXT | NULL | Состав |
| description | TEXT | NULL | Описание |
| price | REAL | NOT NULL, CHECK (price > 0) | Цена |

## 4. users — пользователи системы

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| user_id | INTEGER | PK AUTOINCREMENT | Идентификатор |
| last_name | TEXT | NOT NULL | Фамилия |
| first_name | TEXT | NOT NULL | Имя |
| middle_name | TEXT | NULL | Отчество |
| login | TEXT | NOT NULL, UNIQUE | Логин |
| role_id | INTEGER | NOT NULL, FK → roles, ON DELETE RESTRICT | Ссылка на роль |

## 5. stock_items — товарные позиции

Сочетание модели и размера с доступным количеством.

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| item_id | INTEGER | PK AUTOINCREMENT | Идентификатор |
| product_id | INTEGER | NOT NULL, FK → products, ON DELETE CASCADE | Ссылка на товар |
| size_id | INTEGER | NOT NULL, FK → sizes, ON DELETE RESTRICT | Ссылка на размер |
| quantity | INTEGER | NOT NULL, DEFAULT 0, CHECK (quantity >= 0) | Доступное количество |

Дополнительно: **UNIQUE (product_id, size_id)** — одна пара
(модель, размер) встречается в таблице один раз.

## 6. orders — заказы

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| order_id | INTEGER | PK AUTOINCREMENT | Идентификатор |
| order_date | TEXT | NOT NULL, DEFAULT datetime('now') | Дата заказа |
| user_id | INTEGER | NOT NULL, FK → users, ON DELETE RESTRICT | Кто оформил |

Итоговая сумма **не хранится** — вычисляется при выборке
как `SUM(quantity * price)` по позициям заказа.


## 7. order_items — состав заказа

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| order_item_id | INTEGER | PK AUTOINCREMENT | Идентификатор |
| order_id | INTEGER | NOT NULL, FK → orders, ON DELETE CASCADE | Ссылка на заказ |
| item_id | INTEGER | NOT NULL, FK → stock_items, ON DELETE RESTRICT | Ссылка на товарную позицию |
| quantity | INTEGER | NOT NULL, CHECK (quantity > 0) | Количество |
| price | REAL | NOT NULL, CHECK (price > 0) | Цена на момент заказа |

## Сводка ключей и ограничений

**Первичные ключи (PK):** у каждой таблицы — числовой
идентификатор с `AUTOINCREMENT`.

**Внешние ключи (FK):**

| Таблица | Поле | Ссылается на | ON DELETE |
|---|---|---|---|
| users | role_id | roles.role_id | RESTRICT |
| stock_items | product_id | products.product_id | CASCADE |
| stock_items | size_id | sizes.size_id | RESTRICT |
| orders | user_id | users.user_id | RESTRICT |
| order_items | order_id | orders.order_id | CASCADE |
| order_items | item_id | stock_items.item_id | RESTRICT |

**Ограничения UNIQUE:**

- `roles.name`
- `sizes.value`
- `users.login`
- `stock_items (product_id, size_id)`

**Ограничения CHECK:**

- `sizes.value BETWEEN 16 AND 50`
- `products.price > 0`
- `stock_items.quantity >= 0`
- `order_items.quantity > 0`
- `order_items.price > 0`

**Значения по умолчанию (DEFAULT):**

- `stock_items.quantity = 0`
- `orders.order_date = datetime('now')`

## Скриншот структуры

См. `docs/02_schema_screenshot.png`.
