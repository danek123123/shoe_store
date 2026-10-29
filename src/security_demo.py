def vulnerable_login(conn, login):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE login = '{login}'")
    return cursor.fetchall()

def secure_login(conn, login):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE login = ?", (login,))
    return cursor.fetchall()
