import bcrypt
from database import conn, cursor

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )

def register_user(name: str, email: str, password: str) -> bool:
    hashed = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name.strip(), email.strip().lower(), hashed)
        )
        user_id = cursor.lastrowid
        cursor.execute("""
            INSERT OR IGNORE INTO user_profiles(user_id, age, occupation, monthly_income, other_income, monthly_expenses, current_savings, monthly_savings, loan_amount, monthly_emi, goal)
            VALUES(?, 25, '', 0, 0, 0, 0, 0, 0, 0, 'Retirement')
        """, (user_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error registering user: {e}")
        return False


def login_user(email: str, password: str):
    try:
        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email.strip().lower(),)
        )
        user = cursor.fetchone()
        if user:
            hashed_pw = user[3]
            if isinstance(hashed_pw, str):
                hashed_pw = hashed_pw.encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), hashed_pw):
                return user
    except Exception as e:
        print(f"Error during login: {e}")
        return None

    return None