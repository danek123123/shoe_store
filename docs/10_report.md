# Отчёт по функциям и процедурам (День 10)

## 1. Чем отличается функция от процедуры

**Функция** возвращает значение и может использоваться внутри
SQL-выражений (`SELECT calculate_total(price, quantity) ...`).
Она не изменяет данные (в идеале), только вычисляет.

**Процедура** — это набор команд, который изменяет данные
(`INSERT`, `UPDATE`, `DELETE`) и не обязательно что-то возвращает.
Она вызывается отдельно (`CALL procedure_name(...)`) и работает
с транзакциями.

## 2. Python-функции (Блок 1)

### calc_order_total(price, quantity)

Считает сумму: `price * quantity`. Если `quantity <= 0` — 0.

Пример:
- calc_order_total(1000, 3) -> 3000
- calc_order_total(1000, 0) -> 0
- calc_order_total(None, 3) -> 0

Зарегистрирована как `calculate_total`.

### get_category_count(conn, category_name)

Возвращает COUNT(*) по категории.

Пример:
- get_category_count(conn, "мужская") -> 3

### format_phone(phone)

Форматирует телефон. Если формат неверный — возвращает исходную строку.

Пример:
- format_phone("89991234567") -> +7 (999) 123-45-67
- format_phone("123") -> 123

## 3. Процедуры (Блок 2)

### create_order(conn, user_id, stock_item_id, quantity)

1. Проверяет остаток.
2. Вставляет orders.
3. Вставляет order_items.
4. commit().
Возвращает True/False.

### update_stock(conn, stock_item_id, quantity_sold)

1. Читает текущий остаток.
2. Если новый < 0 — ValueError + rollback().
3. Иначе UPDATE + commit().

### get_sales_report(conn, start_date, end_date)

Возвращает строку:
"С 2026-01-01 по 2026-12-31 продано товаров на сумму 32980.00 руб."

### Как реализованы транзакции

В create_order и update_stock — conn.commit() при успехе,
conn.rollback() при любой ошибке.

## 4. SQL для PostgreSQL (Блок 3)

Полный код — в файле db/procedures_functions.sql.

Функция суммы заказа:

    CREATE OR REPLACE FUNCTION calc_total_pg(price NUMERIC, quantity INTEGER)
    RETURNS NUMERIC AS $$
    BEGIN
        IF quantity <= 0 THEN
            RETURN 0;
        END IF;
        RETURN price * quantity;
    END;
    $$ LANGUAGE plpgsql;

Процедура создания заказа — create_order_pg.

Процедура с обработкой ошибок — write_off_stock_pg (использует
RAISE NOTICE и EXCEPTION).

## 5. Вывод

Все функции протестированы и работают. Процедуры корректно
обрабатывают ошибки через rollback(). SQL для PostgreSQL
написан и приложен в db/procedures_functions.sql.
