"""Автоматическая проверка структуры базы данных."""
from src.db_init import get_connection

EXPECTED_TABLES = [
    "roles", "sizes", "users", "products",
    "stock_items", "orders", "order_items"
]

def get_tables():
    """Шаг 75. Список всех таблиц через sqlite_master."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%' "
            "ORDER BY name"
        ).fetchall()
        return [r["name"] for r in rows]

def get_columns(table):
    """Шаг 76. Список полей через PRAGMA table_info."""
    with get_connection() as conn:
        return conn.execute(f"PRAGMA table_info({table})").fetchall()

def get_foreign_keys(table):
    """Шаг 77. Список внешних ключей через PRAGMA foreign_key_list."""
    with get_connection() as conn:
        return conn.execute(f"PRAGMA foreign_key_list({table})").fetchall()

def get_indexes(table):
    """Шаг 78. Список индексов через PRAGMA index_list."""
    with get_connection() as conn:
        rows = conn.execute(f"PRAGMA index_list({table})").fetchall()
        # Исключаем автоиндексы, создаваемые для PRIMARY KEY и UNIQUE
        return [r["name"] for r in rows if not r["name"].startswith("sqlite_")]

def get_table_sql(table):
    """Возвращает SQL-скрипт создания таблицы для проверки ограничений."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
            (table,)
        ).fetchone()
        return row["sql"] if row else ""

def check_database():
    """Шаг 79. Проверяет все таблицы, поля, ключи и индексы."""
    tables = get_tables()
    print("# Проверка структуры базы данных\n")
    print(f"**Найдено таблиц:** {len(tables)} (ожидалось {len(EXPECTED_TABLES)})\n")
    
    for t in EXPECTED_TABLES:
        if t not in tables:
            print(f"## Таблица {t}\n")
            print("**ОШИБКА:** таблица не найдена!\n")
            continue

        print(f"## Таблица {t}\n")
        
        cols = get_columns(t)
        print(f"- **Количество полей:** {len(cols)}")
        
        pk = [c["name"] for c in cols if c["pk"] > 0]
        print(f"- **Первичный ключ:** {', '.join(pk) if pk else 'нет'}")
        
        fks = get_foreign_keys(t)
        if fks:
            print("- **Внешние ключи:**")
            for fk in fks:
                print(f"  - `{fk['from']}` → `{fk['table']}({fk['to']})` (ON DELETE {fk['on_delete']})")
        else:
            print("- **Внешние ключи:** нет")
            
        idxs = get_indexes(t)
        if idxs:
            print(f"- **Индексы:** {', '.join(idxs)}")
        else:
            print("- **Индексы:** нет (только автоиндексы)")
            
        sql = get_table_sql(t)
        constraints = []
        if "CHECK" in sql: constraints.append("CHECK")
        if "UNIQUE" in sql: constraints.append("UNIQUE")
        if "NOT NULL" in sql: constraints.append("NOT NULL")
        if "DEFAULT" in sql: constraints.append("DEFAULT")
        print(f"- **Ограничения:** {', '.join(constraints) if constraints else 'нет'}\n")
        
        print("| Поле | Тип | NOT NULL | DEFAULT | PK |")
        print("|---|---|---|---|---|")
        for c in cols:
            print(f"| {c['name']} | {c['type']} | {'да' if c['notnull'] else 'нет'} | {c['dflt_value'] or '—'} | {'да' if c['pk'] else '—'} |")
        print("\n---\n")

if __name__ == "__main__":
    check_database()
