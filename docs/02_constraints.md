# Ограничения полей

Документ описывает ограничения для каждого поля базы данных
«Чудо Обувь».

**Виды ограничений:**
- **NOT NULL** — поле обязательно для заполнения.
- **UNIQUE** — значение уникально в таблице.
- **CHECK** — значение удовлетворяет условию.
- **DEFAULT** — значение по умолчанию.
- **PRIMARY KEY** — первичный ключ.
- **FOREIGN KEY** — внешний ключ.

## Таблица roles

| Поле | NOT NULL | UNIQUE | CHECK | DEFAULT |
|---|---|---|---|---|
| role_id | да | да | - | - |
| name | да | да | - | - |

## Таблица users

| Поле | NOT NULL | UNIQUE | CHECK | DEFAULT |
|---|---|---|---|---|
| user_id | да | да | - | - |
| last_name | да | нет | - | - |
| first_name | да | нет | - | - |
| middle_name | нет | нет | - | NULL |
| login | да | да | - | - |
| role_id | да | нет | - | - |

## Таблица products

| Поле | NOT NULL | UNIQUE | CHECK | DEFAULT |
|---|---|---|---|---|
| product_id | да | да | - | - |
| name | да | нет | - | - |
| category | да | нет | - | - |
| subcategory | да | нет | - | - |
| manufacturer | да | нет | - | - |
| image_path | нет | нет | - | NULL |
| composition | нет | нет | - | NULL |
| description | нет | нет | - | NULL |
| price | да | нет | price > 0 | - |

**CHECK:** цена должна быть больше нуля (`price > 0`).

## Таблица sizes

| Поле | NOT NULL | UNIQUE | CHECK | DEFAULT |
|---|---|---|---|---|
| size_id | да | да | - | - |
| value | да | да | value BETWEEN 16 AND 50 | - |

**CHECK:** размер в диапазоне от 16 до 50.

## Таблица stock_items

| Поле | NOT NULL | UNIQUE | CHECK | DEFAULT |
|---|---|---|---|---|
| item_id | да | да | - | - |
| product_id | да | нет | - | - |
| size_id | да | нет | - | - |
| quantity | да | нет | quantity >= 0 | 0 |

**CHECK:** количество не может быть отрицательным (`quantity >= 0`).

**Дополнительно:** UNIQUE `(product_id, size_id)` — сочетание модели
и размера уникально.

## Таблица orders

| Поле | NOT NULL | UNIQUE | CHECK | DEFAULT |
|---|---|---|---|---|
| order_id | да | да | - | - |
| order_date | да | нет | - | CURRENT_DATE |
| user_id | да | нет | - | - |

**DEFAULT:** дата заказа по умолчанию — текущая дата.

## Таблица order_items

| Поле | NOT NULL | UNIQUE | CHECK | DEFAULT |
|---|---|---|---|---|
| order_item_id | да | да | - | - |
| order_id | да | нет | - | - |
| item_id | да | нет | - | - |
| quantity | да | нет | quantity > 0 | - |
| price | да | нет | price > 0 | - |

**CHECK:** количество в заказе должно быть больше нуля (`quantity > 0`).

## Сводка по CHECK-ограничениям

| Таблица | Поле | Условие |
|---|---|---|
| products | price | price > 0 |
| sizes | value | value BETWEEN 16 AND 50 |
| stock_items | quantity | quantity >= 0 |
| order_items | quantity | quantity > 0 |
| order_items | price | price > 0 |

## Сводка по DEFAULT

| Таблица | Поле | Значение по умолчанию |
|---|---|---|
| stock_items | quantity | 0 |
| orders | order_date | CURRENT_DATE |