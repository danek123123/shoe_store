# Типы данных, назначение и роли полей

Документ описывает все таблицы и поля базы данных «Чудо Обувь»:
назначение каждого поля и его роль (PK / FK / UK / атрибут).

**Обозначения:**
- **PK** — первичный ключ (Primary Key)
- **FK** — внешний ключ (Foreign Key)
- **UK** — уникальное поле (Unique Key)
- **атрибут** — обычное поле (не ключ)

## Таблица roles

Справочник ролей пользователей системы.

| Поле | Роль | Назначение |
|---|---|---|
| role_id | **PK** | идентификатор роли (автоинкремент) |
| name | атрибут (**UK**) | название роли: admin, manager, user |

## Таблица users

Пользователи системы. Вход выполняется только по логину, без пароля.

| Поле | Роль | Назначение |
|---|---|---|
| user_id | **PK** | идентификатор пользователя |
| last_name | атрибут | фамилия |
| first_name | атрибут | имя |
| middle_name | атрибут (необязательное) | отчество |
| login | атрибут (**UK**) | логин для входа |
| role_id | **FK** → roles.role_id | ссылка на роль пользователя |

## Таблица products

Каталог моделей обуви.

| Поле | Роль | Назначение |
|---|---|---|
| product_id | **PK** | идентификатор модели обуви |
| name | атрибут | название модели |
| category | атрибут | категория |
| subcategory | атрибут | подкатегория |
| manufacturer | атрибут | производитель |
| image_path | атрибут (необязательное) | путь к изображению |
| composition | атрибут (необязательное) | состав материала |
| description | атрибут (необязательное) | описание модели |
| price | атрибут | цена |

## Таблица sizes

Справочник размеров обуви.

| Поле | Роль | Назначение |
|---|---|---|
| size_id | **PK** | идентификатор размера |
| value | атрибут (**UK**) | значение размера (от 16 до 50) |

## Таблица stock_items

Товарные позиции — сочетания модели и размера с доступным количеством.

| Поле | Роль | Назначение |
|---|---|---|
| item_id | **PK** | идентификатор товарной позиции |
| product_id | **FK** → products.product_id | ссылка на модель обуви |
| size_id | **FK** → sizes.size_id | ссылка на размер |
| quantity | атрибут (по умолчанию 0) | доступное количество |

Дополнительно: **UNIQUE (product_id, size_id)** — одна модель + один размер
встречаются только один раз.

## Таблица orders

Заказы клиентов. Итоговая сумма не хранится — вычисляется при выборке
из `order_items`.

| Поле | Роль | Назначение |
|---|---|---|
| order_id | **PK** | идентификатор заказа |
| order_date | атрибут (по умолчанию текущая дата) | дата оформления заказа |
| user_id | **FK** → users.user_id | ссылка на пользователя |

## Таблица order_items

Состав заказа. Каждая строка — одна позиция в заказе.

| Поле | Роль | Назначение |
|---|---|---|
| order_item_id | **PK** | идентификатор позиции заказа |
| order_id | **FK** → orders.order_id | ссылка на заказ |
| item_id | **FK** → stock_items.item_id | ссылка на товарную позицию |
| quantity | атрибут | количество единиц товара |
| price | атрибут | цена на момент оформления заказа |

## Сводка по ключам

| Таблица | PK | FK | Уникальные |
|---|---|---|---|
| roles | role_id | — | name |
| users | user_id | role_id | login |
| products | product_id | — | — |
| sizes | size_id | — | value |
| stock_items | item_id | product_id, size_id | (product_id, size_id) |
| orders | order_id | user_id | — |
| order_items | order_item_id | order_id, item_id | — |

# Типы данных SQLite

Документ описывает все таблицы и поля базы данных «Чудо Обувь»:
тип данных SQLite, назначение, обязательность (NOT NULL), значение
по умолчанию и ограничения.

**Правила выбора типов:**
- Идентификаторы (PK и FK) — `INTEGER`.
- Строковые значения — `TEXT`.
- Даты — `TEXT` в формате ISO 8601.
- Целые числовые значения (количество, размер) — `INTEGER`.
- Денежные значения (цена) — `REAL` или `NUMERIC`.

## Таблица roles

Справочник ролей пользователей системы.

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|---|---|---|---|---|---|
| role_id | INTEGER | идентификатор роли | да | - | PRIMARY KEY AUTOINCREMENT |
| name | TEXT | название роли | да | - | UNIQUE |

## Таблица users

Пользователи системы. Вход выполняется только по логину, без пароля.

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|---|---|---|---|---|---|
| user_id | INTEGER | идентификатор пользователя | да | - | PRIMARY KEY AUTOINCREMENT |
| last_name | TEXT | фамилия | да | - | - |
| first_name | TEXT | имя | да | - | - |
| middle_name | TEXT | отчество | нет | NULL | - |
| login | TEXT | логин | да | - | UNIQUE |
| role_id | INTEGER | ссылка на роль | да | - | FOREIGN KEY → roles.role_id |

## Таблица products

Каталог моделей обуви.

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|---|---|---|---|---|---|
| product_id | INTEGER | идентификатор модели | да | - | PRIMARY KEY AUTOINCREMENT |
| name | TEXT | название модели | да | - | - |
| category | TEXT | категория | да | - | - |
| subcategory | TEXT | подкатегория | да | - | - |
| manufacturer | TEXT | производитель | да | - | - |
| image_path | TEXT | путь к изображению | нет | NULL | - |
| composition | TEXT | состав материала | нет | NULL | - |
| description | TEXT | описание модели | нет | NULL | - |
| price | NUMERIC | цена | да | - | CHECK (price >= 0) |

## Таблица sizes

Справочник размеров обуви.

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|---|---|---|---|---|---|
| size_id | INTEGER | идентификатор размера | да | - | PRIMARY KEY AUTOINCREMENT |
| value | INTEGER | значение размера | да | - | UNIQUE, CHECK (value BETWEEN 16 AND 50) |

## Таблица stock_items

Товарные позиции — сочетания модели и размера с доступным количеством.

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|---|---|---|---|---|---|
| item_id | INTEGER | идентификатор товарной позиции | да | - | PRIMARY KEY AUTOINCREMENT |
| product_id | INTEGER | ссылка на модель | да | - | FOREIGN KEY → products.product_id |
| size_id | INTEGER | ссылка на размер | да | - | FOREIGN KEY → sizes.size_id |
| quantity | INTEGER | доступное количество | да | 0 | CHECK (quantity >= 0) |

Дополнительно: **UNIQUE (product_id, size_id)** — одна модель + один размер
встречаются только один раз.

## Таблица orders

Заказы клиентов. Итоговая сумма не хранится — вычисляется при выборке
из `order_items`.

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|---|---|---|---|---|---|
| order_id | INTEGER | идентификатор заказа | да | - | PRIMARY KEY AUTOINCREMENT |
| order_date | TEXT | дата оформления (ISO 8601) | да | CURRENT_DATE | - |
| user_id | INTEGER | ссылка на пользователя | да | - | FOREIGN KEY → users.user_id |

## Таблица order_items

Состав заказа. Каждая строка — одна позиция в заказе.

| Поле | Тип SQLite | Назначение | NOT NULL | DEFAULT | Ограничения |
|---|---|---|---|---|---|
| order_item_id | INTEGER | идентификатор позиции | да | - | PRIMARY KEY AUTOINCREMENT |
| order_id | INTEGER | ссылка на заказ | да | - | FOREIGN KEY → orders.order_id |
| item_id | INTEGER | ссылка на товарную позицию | да | - | FOREIGN KEY → stock_items.item_id |
| quantity | INTEGER | количество единиц | да | - | CHECK (quantity > 0) |
| price | NUMERIC | цена на момент заказа | да | - | CHECK (price >= 0) |

## Пояснения по отдельным полям

- **users.login** — уникальное поле. Система различает пользователей
  по логину, поэтому дубликаты недопустимы (ограничение `UNIQUE`).
- **users.middle_name** — может быть пустым, так как отчество есть
  не у всех (допускает `NULL`, `NOT NULL` не задаётся).
- **users.role_id** — внешний ключ на `roles.role_id`. Обязателен,
  потому что каждый пользователь должен иметь роль.
- **orders.order_date** — хранится как `TEXT` в формате ISO 8601
  (`YYYY-MM-DD`), значение по умолчанию — текущая дата (`CURRENT_DATE`).
- **products.price** и **order_items.price** — денежные значения,
  тип `NUMERIC` (допускается `REAL`).

## Сводка по ключам

| Таблица | PK | FK | Уникальные |
|---|---|---|---|
| roles | role_id | — | name |
| users | user_id | role_id | login |
| products | product_id | — | — |
| sizes | size_id | — | value |
| stock_items | item_id | product_id, size_id | (product_id, size_id) |
| orders | order_id | user_id | — |
| order_items | order_item_id | order_id, item_id | — |