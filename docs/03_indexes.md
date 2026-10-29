# Индексы базы данных

Документ описывает индексы, создаваемые для ускорения JOIN,
поиска и сортировки. Индексы добавляются в DDL-скрипт
`src/db_init.py`.

## 1. Сводная таблица индексов

| Таблица | Поле | Тип | Обоснование |
|---|---|---|---|
| users | role_id | обычный | ускоряет JOIN с roles |
| orders | user_id | обычный | ускоряет JOIN с users |
| orders | order_date | обычный | ускоряет сортировку заказов по дате |
| products | category | обычный | ускоряет фильтрацию по категории |
| products | manufacturer | обычный | ускоряет поиск по производителю |
| products | price | обычный | ускоряет сортировку по цене |
| stock_items | product_id | обычный | ускоряет JOIN с products |
| stock_items | size_id | обычный | ускоряет JOIN с sizes |
| order_items | order_id | обычный | ускоряет JOIN с orders |
| order_items | item_id | обычный | ускоряет JOIN с stock_items |

## 2. Индексы по внешним ключам

Индексы на полях внешних ключей ускоряют JOIN между таблицами.
SQLite создаёт индексы автоматически только для PRIMARY KEY
и UNIQUE, поэтому внешние ключи надо индексировать вручную.

| Таблица | Поле | Ссылается на |
|---|---|---|
| users | role_id | roles.role_id |
| orders | user_id | users.user_id |
| stock_items | product_id | products.product_id |
| stock_items | size_id | sizes.size_id |
| order_items | order_id | orders.order_id |
| order_items | item_id | stock_items.item_id |

## 3. Индексы по полям поиска

Поиск товаров выполняется по категории и производителю.
Соответственно нужны индексы:

- `products.category` — фильтрация по категории;
- `products.manufacturer` — поиск по производителю.

## 4. Индексы по полям сортировки

Сортировка заказов — по дате; сортировка товаров — по цене.
Соответственно нужны индексы:

- `orders.order_date` — сортировка заказов по дате;
- `products.price` — сортировка товаров по цене.

## 5. Не создавать индексы на все поля

Индексы ускоряют выборку, но замедляют вставку и обновление,
а также увеличивают размер базы. Поэтому индексируются только
поля, участвующие в JOIN, поиске или сортировке. На поля
`description`, `composition`, `image_path` индексы не нужны —
по ним не выполняется поиск.

## 6. Список CREATE INDEX

    CREATE INDEX idx_users_role_id       ON users(role_id);
    CREATE INDEX idx_orders_user_id      ON orders(user_id);
    CREATE INDEX idx_orders_order_date   ON orders(order_date);
    CREATE INDEX idx_products_category   ON products(category);
    CREATE INDEX idx_products_manufacturer ON products(manufacturer);
    CREATE INDEX idx_products_price      ON products(price);
    CREATE INDEX idx_stock_items_product ON stock_items(product_id);
    CREATE INDEX idx_stock_items_size    ON stock_items(size_id);
    CREATE INDEX idx_order_items_order   ON order_items(order_id);
    CREATE INDEX idx_order_items_item    ON order_items(item_id);
