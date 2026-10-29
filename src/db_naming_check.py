"""Автоматическая проверка имён таблиц и полей базы данных.

Скрипт читает структуру БД из sqlite_master и PRAGMA table_info
и проверяет каждое имя на соответствие правилам именования.
"""
import re

from src.db_init import get_connection

# Зарезервированные слова SQL, которых нельзя использовать как имена
RESERVED = {
    "select", "from", "where", "order", "group", "by", "having",
    "insert", "update", "delete", "create", "drop", "alter",
    "table", "index", "view", "trigger", "column", "key",
    "primary", "foreign", "references", "unique", "check",
    "default", "not", "null", "and", "or", "in", "is", "like",
    "between", "join", "on", "as", "distinct", "union", "all",
    "limit", "offset", "values", "into", "set",
    "case", "when", "then", "else", "end", "date", "time",
    "timestamp", "user", "role", "grant", "revoke",
}

def get_tables():
    """Возвращает список всех пользовательских таблиц в БД."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%' "
            "ORDER BY name"
        ).fetchall()
        return [r["name"] for r in rows]

def get_columns(table_name):
    """Возвращает список полей таблицы через PRAGMA table_info."""
    with get_connection() as conn:
        rows = conn.execute(
            f"PRAGMA table_info({table_name})"
        ).fetchall()
        return [r["name"] for r in rows]

def check_name(name):
    """Проверяет одно имя. Возвращает список ошибок (пустой, если ок)."""
    errors = []

    if not name:
        errors.append("имя пустое")
        return errors

    if not name[0].isalpha():
        errors.append("имя должно начинаться с буквы")

    if not re.match(r"^[a-z0-9_]+$", name):
        errors.append("только строчные латинские буквы, цифры и _")

    if name.lower() in RESERVED:
        errors.append("зарезервированное слово SQL")

    return errors

def check_database():
    """Проходит по всем таблицам и полям. Возвращает отчёт."""
    report = []
    tables = get_tables()

    for t in tables:
        t_errors = check_name(t)
        report.append(("таблица", t, t_errors))

        for col in get_columns(t):
            c_errors = check_name(col)
            report.append((f"поле {t}", col, c_errors))

    return report

if __name__ == "__main__":
    report = check_database()
    total = len(report)
    errors = [r for r in report if r[2]]

    print(f"Проверено объектов: {total}")
    print(f"Найдено ошибок: {len(errors)}")
    print()

    for kind, name, errs in report:
        if errs:
            print(f"[FAIL] {kind}: {name} — {'; '.join(errs)}")
        else:
            print(f"[PASS] {kind}: {name}")

    if not errors:
        print("\nВсе имена соответствуют правилам.")
