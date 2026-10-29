# Отчёт по администрированию базы данных (День 12)

## 1. Роли и права в SQLite

SQLite не поддерживает роли и права на уровне СУБД, в отличие от PostgreSQL или MySQL. Разграничение доступа реализуется **на уровне приложения**:

- В таблице `roles` хранятся роли: `admin_db`, `developer`, `reader`, а также старые `admin`, `manager`, `user`.
- В Python-словаре `PERMISSIONS` задано, какие действия разрешены каждой роли.
- Функция `check_permission(conn, user_id, action)` проверяет, разрешено ли действие пользователю.

### Матрица прав

| Роль | SELECT | DELETE |
|---|---:|---:|
| admin | True | True |
| manager | True | False |
| user | True | False |
| reader | True | False |
| developer | True | False |

**Вывод:** `DELETE` разрешено только администратору (`admin`, `admin_db`). Остальные роли, включая `manager`, `user`, `reader`, `developer`, получают отказ.

## 2. Функция `check_permission` и результаты тестирования

Функция делает `JOIN` таблиц `users` и `roles`, находит роль пользователя и сверяет запрошенное действие со списком в словаре `PERMISSIONS`.

```python
def check_permission(conn, user_id, action):
    row = conn.execute(
        "SELECT r.name FROM users u "
        "JOIN roles r ON r.role_id = u.role_id "
        "WHERE u.user_id = ?", (user_id,)
    ).fetchone()
    if not row:
        return False
    role = row["name"]
    return action.upper() in PERMISSIONS.get(role, [])
```

## 3. Способы резервного копирования

| Метод | Плюсы | Минусы |
|---|---|---|
| `shutil.copy2` | Простой, быстрый, стандартный | Небезопасен: если база активно пишется, копия может быть повреждена |
| `conn.backup()` | Безопасно, копия консистентна даже при активной записи | Чуть медленнее, требует открытого соединения |

В `src/backup_restore.py` реализованы обе функции:

- `backup_simple()` — через `shutil`;
- `backup_safe()` — через `conn.backup()`.

## 4. Результат `PRAGMA integrity_check`

```sql
PRAGMA integrity_check;
-- Результат: ok
```

База данных целостна, повреждений нет.

## 5. Восстановление базы из бэкапа

Сценарий «аварии» и восстановления:

1. Создан бэкап: `backup_simple()` → файл в `db/backups/backup_YYYY_MM_DD_HH_MM.sqlite`.
2. Симулирована «авария»: через SQLite Viewer удалена таблица `orders` или все заказы.
3. Вызвана функция `restore(backup_path)` — скопировала файл бэкапа обратно в `db/shoe_store.sqlite`.
4. Проверка: после восстановления таблица `orders` снова доступна, все заказы на месте, `PRAGMA integrity_check` возвращает `ok`.

## 6. Статистика базы данных

Функция `get_db_stats(conn)` в `src/backup_restore.py` собирает данные через `PRAGMA` и выводит их в консоль:

```text
Размер страницы (PRAGMA page_size): 4096 байт
Количество страниц (PRAGMA page_count): N
Общий размер базы: N * 4096 байт (~ N КБ)
Список таблиц (8): roles, sizes, users, products, stock_items, orders, order_items, audit_log
```

## 7. Скрипт автоматизации обслуживания

Файл `src/maintenance.py` выполняет полный цикл:

1. Проверяет целостность через `PRAGMA integrity_check`.
2. Делает резервную копию через `backup_safe`.
3. Собирает статистику через `get_db_stats`.
4. Очищает старые логи через `clear_old_logs`, старше 30 дней.
5. Выводит итоговый отчёт.

## 8. Вывод

Разграничение прав реализовано через Python-словарь `PERMISSIONS` и функцию `check_permission`. Резервное копирование и восстановление работают, что проверено через `PRAGMA integrity_check`. Скрипт `maintenance.py` автоматизирует проверку целостности, бэкап, сбор статистики и очистку логов.