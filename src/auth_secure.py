import hashlib
from datetime import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(conn, login, password):
    p_hash = hash_password(password)
    try:
        conn.execute("INSERT INTO users (login, password_hash, last_name, first_name, role_id) VALUES (?, ?, 'Иванов', 'Иван', 3)", (login, p_hash))
        conn.commit()
        return True
    except Exception:
        return False

def check_password(conn, login, password):
    row = conn.execute("SELECT password_hash FROM users WHERE login = ?", (login,)).fetchone()
    status = 'отказ'
    result = False
    if row and row["password_hash"] == hash_password(password):
        status = 'успех'
        result = True
    
    conn.execute("INSERT INTO login_audit (login, status, login_time) VALUES (?, ?, ?)", (login, status, datetime.now().isoformat()))
    conn.commit()
    return result
