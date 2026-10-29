# Результаты проверки ограничений

| Ограничение | Ожидаемый результат | Фактический результат | Статус |
|---|---|---|---|
| UNIQUE на login | ошибка | UNIQUE constraint failed: users.login | пройден |
| NOT NULL на last_name | ошибка | NOT NULL constraint failed: users.last_name | пройден |
| CHECK на price | ошибка | CHECK constraint failed: price > 0 AND price < 1000000 | пройден |
| CHECK на quantity | ошибка | CHECK constraint failed: quantity_available >= 0 | пройден |
| FOREIGN KEY на role_id | ошибка | FOREIGN KEY constraint failed | пройден |
| ON DELETE RESTRICT | ошибка | FOREIGN KEY constraint failed | пройден |
| ON DELETE CASCADE | каскадное удаление | позиции удалены | пройден |
