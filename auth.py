import bcrypt
from database import conn, cursor

def hash_password(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

def register_user(name, email, password):

    hashed = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, hashed)
        )
        conn.commit()
        return True

    except:
        return False


def login_user(email,password):

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()

    if user:

        if bcrypt.checkpw(
            password.encode(),
            user[3]
        ):
            return user

    return None