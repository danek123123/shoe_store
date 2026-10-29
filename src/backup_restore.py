"""Резервное копирование и восстановление базы (День 12)."""
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "db" / "shoe_store.sqlite"
BACKUP_DIR = PROJECT_ROOT / "db" / "backups"

def backup_simple():
    """Шаг 2.1. Копирует файл базы через shutil."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    backup_path = BACKUP_DIR / f"backup_{stamp}.sqlite"
    shutil.copy2(DB_PATH, backup_path)
    print(f"OK: бэкап (shutil) создан: {backup_path}")
    return backup_path

def backup_safe():
    """Шаг 2.2. Безопасный бэкап через conn.backup()."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    backup_path = BACKUP_DIR / f"safe_{stamp}.sqlite"

    source = sqlite3.connect(DB_PATH)
    target = sqlite3.connect(backup_path)
    try:
        source.backup(target)
        print(f"OK: бэкап (safe) создан: {backup_path}")
    finally:
        target.close()
        source.close()
    return backup_path

def check_integrity(conn):
    """Шаг 2.3. PRAGMA integrity_check."""
    result = conn.execute("PRAGMA integrity_check").fetchone()[0]
    if result == "ok":
        print("OK: integrity_check — ok")
    else:
        print(f"FAIL: integrity_check — {result}")
    return result

def restore(backup_path):
    """Шаг 2.4. Восстанавливает базу из файла бэкапа."""
    backup_path = Path(backup_path)
    if not backup_path.exists():
        print(f"Нет файла: {backup_path}")
        return False
    shutil.copy2(backup_path, DB_PATH)
    print(f"OK: база восстановлена из {backup_path}")
    return True

def get_db_stats(conn):
    """Шаг 3.1. Статистика базы через PRAGMA."""
    page_size = conn.execute("PRAGMA page_size").fetchone()[0]
    page_count = conn.execute("PRAGMA page_count").fetchone()[0]
    total = page_size * page_count
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    )]
    print(f"Размер страницы: {page_size} байт")
    print(f"Количество страниц: {page_count}")
    print(f"Общий размер: {total} байт ({total/1024:.1f} КБ)")
    print(f"Таблицы ({len(tables)}): {', '.join(tables)}")
    return {"page_size": page_size, "page_count": page_count,
            "total_bytes": total, "tables": tables}

def clear_old_logs(conn, days=30):
    """Шаг 3.2. Удаляет audit_log старше 30 дней."""
    try:
        cur = conn.execute(
            "DELETE FROM audit_log WHERE changed_at < date('now', ?)",
            (f"-{days} days",),
        )
        conn.commit()
        print(f"OK: удалено старых логов: {cur.rowcount}")
        return cur.rowcount
    except Exception as e:
        print(f"Ошибка clear_old_logs: {e}")
        return 0

if __name__ == "__main__":
    print("=== Блок 2. Бэкапы ===")
    backup_simple()
    backup_safe()

    conn = sqlite3.connect(DB_PATH)
    check_integrity(conn)

    print("\n=== Блок 3. Статистика и очистка ===")
    get_db_stats(conn)
    clear_old_logs(conn)

    conn.close()
