# Отчёт по триггерам (День 11)

## 1. Созданные триггеры

| Триггер | Таблица | Событие | Назначение |
|---|---|---|---|
| trg_products_price_update | products | AFTER UPDATE | логирует изменение цены в audit_log |
| trg_orders_delete | orders | AFTER DELETE | логирует удаление заказа |
| trg_users_updated_at | users | AFTER UPDATE | обновляет поле updated_at |
| trg_order_items_insert | order_items | AFTER INSERT | списывает остаток со склада |
| trg_users_before_delete | users | BEFORE DELETE | запрещает удаление пользователя с заказами |
| trg_stock_items_insert | stock_items | BEFORE INSERT | запрещает отрицательное количество |

## 2. Разница между BEFORE и AFTER

- **BEFORE** — срабатывает до изменения данных. Можно **отменить** операцию через `RAISE(ABORT, '...')`. Используется для валидации и защиты.
- **AFTER** — срабатывает после изменения данных. Отменить операцию нельзя, можно только логировать или делать дополнительные действия.

В проекте: BEFORE используется для защиты от удаления пользователя с заказами и проверки отрицательного количества. AFTER — для логирования, автосписания остатков и обновления updated_at.

## 3. Использование OLD и NEW

- **OLD** — старое значение записи (до изменения/удаления).
- **NEW** — новое значение (при INSERT/UPDATE).

Примеры:
- `trg_products_price_update`: `OLD.price` — старая цена, `NEW.price` — новая;
- `trg_orders_delete`: `OLD.order_id` — ID удалённого заказа (`NEW` недоступен);
- `trg_order_items_insert`: `NEW.stock_item_id`, `NEW.quantity` — данные новой позиции.

## 4. Результаты работы audit_log

После тестовых операций в таблице появились записи об изменении цен и удалении заказов (скриншот прилагается в терминале).

## 5. Защита от удаления пользователя с заказами

Триггер `trg_users_before_delete` срабатывает BEFORE DELETE, проверяет наличие заказов через `SELECT COUNT(*) FROM orders WHERE user_id = OLD.user_id`. Если заказы есть, вызывается `RAISE(ABORT, 'Нельзя удалить пользователя с активными заказами')`.

Проверка: `DELETE FROM users WHERE user_id = 1` → `sqlite3.IntegrityError: Нельзя удалить пользователя с активными заказами`.

## 6. Автосписание остатков

Триггер `trg_order_items_insert` срабатывает AFTER INSERT в `order_items` и уменьшает `quantity_available` в `stock_items` на `NEW.quantity`.

Проверка: Остаток до: 5 → Вставка order_items (quantity = 2) → Остаток после: 3.

## 7. Вывод

Все шесть триггеров работают корректно. `audit_log` заполняется при изменении цен и удалении заказов. Защита от удаления пользователя с заказами срабатывает через `RAISE(ABORT)`.
