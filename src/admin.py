"""Администрирование: роли, права, проверка доступа (День 12)."""
from src.db_init import get_connection

# Шаг 1.2. Словарь прав по ролям
PERMISSIONS = {
    "admin_db":  ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP"],
    "developer": ["SELECT", "INSERT", "UPDATE"],
    "reader":    ["SELECT"],
    "admin":     ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP"],
    "manager":   ["SELECT", "INSERT", "UPDATE"],
    "user":      ["SELECT", "INSERT"],
}

def add_new_roles():
    """Шаг 1.1. Добавляет роли admin_db, developer, reader."""
    with get_connection() as conn:
        for role in ("admin_db", "developer", "reader"):
            conn.execute(
                "INSERT OR IGNORE INTO roles (name) VALUES (?)", (role,)
            )
        conn.commit()
        print("OK: роли admin_db, developer, reader добавлены")

def check_permission(conn, user_id, action):
    """Шаг 1.3. Проверяет, разрешено ли пользователю действие."""
    try:
        row = conn.execute(
            "SELECT r.name AS role FROM users u "
            "JOIN roles r ON r.role_id = u.role_id "
            "WHERE u.user_id = ?",
            (user_id,),
        ).fetchone()
        if row is None:
            return False
        role = row["role"]
        allowed = PERMISSIONS.get(role, [])
        return action.upper() in [a.upper() for a in allowed]
    except Exception as e:
        print(f"Ошибка check_permission: {e}")
        return False

def find_user_by_role(conn, role_name):
    """Возвращает user_id первого пользователя с указанной ролью."""
    row = conn.execute(
        "SELECT u.user_id FROM users u "
        "JOIN roles r ON r.role_id = u.role_id "
        "WHERE r.name = ? LIMIT 1",
        (role_name,),
    ).fetchone()
    return row["user_id"] if row else None

if __name__ == "__main__":
    add_new_roles()
    with get_connection() as conn:
        conn.row_factory = __import__("sqlite3").Row

        # Тест: читаем роли
        print("\n--- Роли в базе ---")
        for r in conn.execute("SELECT role_id, name FROM roles ORDER BY role_id"):
            print(dict(r))

        # Шаг 1.4. Тест прав
        print("\n--- Тест прав ---")
        for role_name in ("admin", "manager", "user", "reader", "developer"):
            uid = find_user_by_role(conn, role_name)
            if uid is None:
                print(f"  {role_name}: нет пользователя")
                continue
            can_delete = check_permission(conn, uid, "DELETE")
            can_select = check_permission(conn, uid, "SELECT")
            print(f"  {role_name} (user_id={uid}): SELECT={can_select}, DELETE={can_delete}")
