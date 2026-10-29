# Отчёт о финальном DDL-скрипте

Файл: `src/db_init.py`
Назначение: создание базы данных `db/shoe_store.sqlite` со всеми
таблицами, ограничениями и индексами.

## 1. Порядок создания

Скрипт создаёт объекты в следующем порядке:

1. **PRAGMA foreign_keys = ON** при подключении.
2. **Справочники:** `roles`, `sizes`.
3. **Основные сущности:** `products`, `users`.
4. **Товарные позиции:** `stock_items`.
5. **Заказы:** `orders`.
6. **Состав заказов:** `order_items`.
7. **Индексы** — десять штук.

Порядок важен: дочерние таблицы создаются после родительских,
иначе внешние ключи не сработают.

## 2. Таблицы и ограничения

### roles

- PK: `role_id`;
- UNIQUE: `name`.

### sizes

- PK: `size_id`;
- UNIQUE: `value`;
- CHECK: `value > 20 AND value < 50`.

### products

- PK: `product_id`;
- CHECK: `length(name) > 0`;
- CHECK: `price > 0 AND price < 1000000`.

### users

- PK: `user_id`;
- UNIQUE: `login`;
- CHECK: `length(login) >= 3 AND length(login) <= 20`;
- FK: `role_id → roles(role_id) ON DELETE RESTRICT`.

### stock_items

- PK: `item_id`;
- UNIQUE: `(product_id, size_id)`;
- CHECK: `quantity >= 0`;
- DEFAULT: `quantity = 0`;
- FK: `product_id → products(product_id) ON DELETE RESTRICT`;
- FK: `size_id → sizes(size_id) ON DELETE RESTRICT`.

### orders

- PK: `order_id`;
- DEFAULT: `order_date = datetime('now')`;
- CHECK: `date(order_date) IS NOT NULL`;
- FK: `user_id → users(user_id) ON DELETE RESTRICT`.

### order_items

- PK: `order_item_id`;
- CHECK: `quantity > 0`;
- CHECK: `price > 0`;
- FK: `order_id → orders(order_id) ON DELETE CASCADE`;
- FK: `item_id → stock_items(item_id) ON DELETE RESTRICT`.

## 3. Индексы

| Индекс | Таблица | Поле | Назначение |
|---|---|---|---|
| idx_users_role_id | users | role_id | JOIN с roles |
| idx_orders_user_id | orders | user_id | JOIN с users |
| idx_orders_order_date | orders | order_date | сортировка заказов по дате |
| idx_products_category | products | category | фильтрация по категории |
| idx_products_manufacturer | products | manufacturer | поиск по производителю |
| idx_products_price | products | price | сортировка по цене |
| idx_stock_items_product | stock_items | product_id | JOIN с products |
| idx_stock_items_size | stock_items | size_id | JOIN с sizes |
| idx_order_items_order | order_items | order_id | JOIN с orders |
| idx_order_items_item | order_items | item_id | JOIN с stock_items |

## 4. Проверка после пересоздания

- База создаётся без ошибок.
- Все семь таблиц присутствуют.
- Все десять индексов созданы.
- Ограничения CHECK работают (5 проверок).
- Внешние ключи работают (3 проверки RESTRICT).
- Каскадное удаление работает (1 проверка CASCADE).

Подробности — в `docs/03_data_integrity.md`.

## 5. Соответствие требованиям

- Все таблицы соответствуют правилам именования.
- Все ограничения заданы в DDL.
- Все внешние ключи имеют явные стратегии удаления.
- PRAGMA foreign_keys = ON включён.
- Порядок создания корректен.
