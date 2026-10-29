# Проверка ограничений целостности

Скрипт: `src/db_test_constraints.py`
Команда запуска: `python -m src.db_test_constraints`

| Ограничение | Ожидаемый результат | Фактический результат | Статус |
|---|---|---|---|
| UNIQUE на login | ошибка | UNIQUE constraint failed: users.login | пройден |
| NOT NULL на last_name | ошибка | NOT NULL constraint failed: users.last_name | пройден |
| CHECK на price | ошибка | CHECK constraint failed: price > 0 | пройден |
| CHECK на quantity | ошибка | CHECK constraint failed: quantity >= 0 | пройден |
| FOREIGN KEY на role_id | ошибка | FOREIGN KEY constraint failed | пройден |
| ON DELETE RESTRICT | ошибка | FOREIGN KEY constraint failed | пройден |
| ON DELETE CASCADE | каскадное удаление | позиция удалена автоматически | пройден |

## Вывод

Все семь ограничений работают корректно:

- **UNIQUE на login** — не даёт вставить второго пользователя
  с существующим логином.
- **NOT NULL на last_name** — запрещает вставлять пользователя
  без фамилии.
- **CHECK на price** — не пропускает товар с отрицательной ценой.
- **CHECK на quantity** — не пропускает отрицательное количество
  в товарной позиции.
- **FOREIGN KEY на role_id** — запрещает ссылку на несуществующую
  роль.
- **ON DELETE RESTRICT** — не даёт удалить роль, на которую
  ссылаются пользователи.
- **ON DELETE CASCADE** — автоматически удаляет позиции заказа
  при удалении самого заказа.
