# Описание ER-диаграммы «Чудо Обувь»

Текстовое описание сущностей и связей, изображённых на диаграмме
`ERD_module_1.pdf` (исходник — `ERD_module_1.drawio`).

## 1. Таблицы

### 1.1. roles

**Назначение:** справочник ролей пользователей системы.

**Ключи:**
- Первичный ключ: `role_id` (PK, автоинкремент).
- Уникальное поле: `name`.

**Поля:** `role_id`, `name`.

**Значения:** `admin`, `manager`, `user`.

### 1.2. users

**Назначение:** пользователи системы. Вход выполняется только
по логину, без пароля.

**Ключи:**
- Первичный ключ: `user_id` (PK).
- Внешний ключ: `role_id` → `roles.role_id` (FK).
- Уникальное поле: `login`.

**Поля:** `user_id`, `last_name`, `first_name`, `middle_name`,
`login`, `role_id`.

**Обязательные:** `login`, `last_name`, `first_name`, `role_id`.
**Необязательное:** `middle_name`.

### 1.3. products

**Назначение:** каталог моделей обуви.

**Ключи:**
- Первичный ключ: `product_id` (PK).

**Поля:** `product_id`, `name`, `category`, `subcategory`,
`manufacturer`, `image_path`, `composition`, `description`, `price`.

**Обязательные:** `name`, `category`, `subcategory`, `manufacturer`,
`price`.
**Необязательные:** `image_path`, `composition`, `description`.

### 1.4. sizes

**Назначение:** справочник размеров обуви.

**Ключи:**
- Первичный ключ: `size_id` (PK).
- Уникальное поле: `value`.

**Поля:** `size_id`, `value`.

**Диапазон:** от 16 до 50.

### 1.5. stock_items

**Назначение:** товарные позиции — сочетания модели и размера
с доступным количеством.

**Ключи:**
- Первичный ключ: `item_id` (PK).
- Внешний ключ: `product_id` → `products.product_id` (FK).
- Внешний ключ: `size_id` → `sizes.size_id` (FK).
- UNIQUE: `(product_id, size_id)`.

**Поля:** `item_id`, `product_id`, `size_id`, `quantity`.

**Значения по умолчанию:** `quantity = 0`.

### 1.6. orders

**Назначение:** заказы клиентов. Итоговая сумма не хранится —
вычисляется при выборке из `order_items`.

**Ключи:**
- Первичный ключ: `order_id` (PK).
- Внешний ключ: `user_id` → `users.user_id` (FK).

**Поля:** `order_id`, `order_date`, `user_id`.

**Значения по умолчанию:** `order_date` — текущая дата.

### 1.7. order_items

**Назначение:** состав заказа. Каждая строка — одна позиция
в заказе.

**Ключи:**
- Первичный ключ: `order_item_id` (PK).
- Внешний ключ: `order_id` → `orders.order_id` (FK).
- Внешний ключ: `item_id` → `stock_items.item_id` (FK).

**Поля:** `order_item_id`, `order_id`, `item_id`, `quantity`,
`price`.

**Особенность:** хранится `price` — цена на момент оформления
заказа.

## 2. Связи

| № | Связь | Тип | Кардинальность |
|---|---|---|---|
| 1 | roles → users | 1:N | один-ко-многим |
| 2 | users → orders | 1:N | один-ко-многим |
| 3 | products → stock_items | 1:N | один-ко-многим |
| 4 | sizes → stock_items | 1:N | один-ко-многим |
| 5 | orders → order_items | 1:N | один-ко-многим |
| 6 | stock_items → order_items | 1:N | один-ко-многим |

**Пояснения:**

- **roles → users (1:N).** У одной роли много пользователей.
- **users → orders (1:N).** Один пользователь оформляет много заказов.
- **products → stock_items (1:N).** У одной модели много товарных позиций.
- **sizes → stock_items (1:N).** Один размер встречается у разных моделей.
- **orders → order_items (1:N).** В одном заказе много позиций.
- **stock_items → order_items (1:N).** Одна позиция может входить в разные заказы.

## 3. Проверка диаграммы

- Семь таблиц.
- У каждой таблицы есть первичный ключ (PK).
- У зависимых таблиц есть внешние ключи (FK).
- Все связи проведены с кардинальностью 1:N.
- Нет изолированных таблиц.

## 4. Схематичное изображение связей

    roles (1)
       │
       │ N
       ▼
    users (1)
       │
       │ N
       ▼
    orders (1)              sizes (1)
       │                       │
       │ N                     │ N
       ▼                       ▼
    order_items (N) ◄── N ── stock_items (N) ◄── N ── products (1)
