# Результаты SQL-запросов

## 1. Список всех ролей

```sql
SELECT * FROM roles
```

| role_id | name |
|---|---|
| 1 | admin |
| 2 | manager |
| 3 | user |

## 2. Список всех пользователей с ролями

```sql
SELECT u.user_id, u.last_name, u.first_name, r.name AS role
FROM users u JOIN roles r ON r.role_id = u.role_id
```

| user_id | last_name | first_name | role |
|---|---|---|---|
| 1 | Админов | Алексей | admin |
| 2 | Менеджеров | Михаил | manager |
| 3 | Пользователев | Пётр | user |

## 3. Список всех товаров

```sql
SELECT product_id, product_name, category, price FROM products
```

| product_id | product_name | category | price |
|---|---|---|---|
| 1 | Nike Air Max | мужская | 8990.0 |
| 2 | Adidas Ultraboost | мужская | 12490.0 |
| 3 | Ecco Soft 7 | женская | 10990.0 |
| 4 | Ralf Ringer Classic | мужская | 7490.0 |
| 5 | Crocs Classic | детская | 2990.0 |

## 4. Список всех размеров

```sql
SELECT * FROM sizes
```

| size_id | size_value |
|---|---|
| 1 | 36.0 |
| 2 | 37.0 |
| 3 | 38.0 |
| 4 | 39.0 |
| 5 | 40.0 |

## 5. Список всех заказов с ФИО клиентов

```sql
SELECT o.order_id, o.order_date, u.last_name, u.first_name
FROM orders o JOIN users u ON u.user_id = o.user_id
```

| order_id | order_date | last_name | first_name |
|---|---|---|---|
| 1 | 2026-10-10 10:15:00 | Пользователев | Пётр |
| 2 | 2026-10-11 14:30:00 | Менеджеров | Михаил |
| 3 | 2026-10-12 09:05:00 | Админов | Алексей |

## 6. Список всех товарных позиций с наименованием и размером

```sql
SELECT si.stock_item_id, p.product_name, s.size_value, si.quantity_available
FROM stock_items si
JOIN products p ON p.product_id = si.product_id
JOIN sizes s ON s.size_id = si.size_id
```

| stock_item_id | product_name | size_value | quantity_available |
|---|---|---|---|
| 1 | Nike Air Max | 36.0 | 5 |
| 2 | Nike Air Max | 37.0 | 3 |
| 3 | Adidas Ultraboost | 37.0 | 2 |
| 4 | Adidas Ultraboost | 38.0 | 4 |
| 5 | Ecco Soft 7 | 36.0 | 6 |
| 6 | Ecco Soft 7 | 39.0 | 1 |
| 7 | Ralf Ringer Classic | 37.0 | 3 |
| 8 | Ralf Ringer Classic | 40.0 | 5 |
| 9 | Crocs Classic | 36.0 | 10 |
| 10 | Crocs Classic | 38.0 | 8 |
