"""Скрипт автоматизации обслуживания базы (День 12, шаг 3.3)."""
import sqlite3
from datetime import datetime

from src.backup_restore import (
    DB_PATH, check_integrity, backup_safe,
    get_db_stats, clear_old_logs,
)

def main():
    print(f"=== Обслуживание базы {datetime.now():%Y-%m-%d %H:%M:%S} ===\n")

    conn = sqlite3.connect(DB_PATH)
    try:
        print("1. Проверка целостности:")
        ok = check_integrity(conn)

        print("\n2. Резервная копия:")
        backup_path = backup_safe()

        print("\n3. Статистика базы:")
        stats = get_db_stats(conn)

        print("\n4. Очистка старых логов:")
        removed = clear_old_logs(conn, days=30)

        print("\n=== Итог ===")
        print(f"Целостность: {ok}")
        print(f"Бэкап: {backup_path}")
        print(f"Размер базы: {stats['total_bytes']} байт")
        print(f"Удалено старых логов: {removed}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
