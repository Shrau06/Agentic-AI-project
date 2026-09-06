import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_profiles(
    user_id INTEGER PRIMARY KEY,
    age INTEGER DEFAULT 25,
    occupation TEXT DEFAULT '',
    monthly_income REAL DEFAULT 0,
    other_income REAL DEFAULT 0,
    monthly_expenses REAL DEFAULT 0,
    current_savings REAL DEFAULT 0,
    monthly_savings REAL DEFAULT 0,
    loan_amount REAL DEFAULT 0,
    monthly_emi REAL DEFAULT 0,
    goal TEXT DEFAULT 'Retirement',
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

conn.commit()


def get_default_profile():
    return {
        "age": 25,
        "occupation": "",
        "monthly_income": 0,
        "other_income": 0,
        "monthly_expenses": 0,
        "current_savings": 0,
        "monthly_savings": 0,
        "loan_amount": 0,
        "monthly_emi": 0,
        "goal": "Retirement"
    }


def get_user_profile(user_id):
    if not user_id:
        return None
    cursor.execute("""
        SELECT age, occupation, monthly_income, other_income, monthly_expenses, current_savings, monthly_savings, loan_amount, monthly_emi, goal
        FROM user_profiles WHERE user_id=?
    """, (user_id,))
    row = cursor.fetchone()
    if row:
        return {
            "age": row[0] if row[0] is not None else 25,
            "occupation": row[1] if row[1] is not None else "",
            "monthly_income": row[2] if row[2] is not None else 0,
            "other_income": row[3] if row[3] is not None else 0,
            "monthly_expenses": row[4] if row[4] is not None else 0,
            "current_savings": row[5] if row[5] is not None else 0,
            "monthly_savings": row[6] if row[6] is not None else 0,
            "loan_amount": row[7] if row[7] is not None else 0,
            "monthly_emi": row[8] if row[8] is not None else 0,
            "goal": row[9] if row[9] is not None else "Retirement"
        }
    return None


def save_user_profile(user_id, profile):
    if not user_id or not profile:
        return
    cursor.execute("""
        INSERT INTO user_profiles(user_id, age, occupation, monthly_income, other_income, monthly_expenses, current_savings, monthly_savings, loan_amount, monthly_emi, goal)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            age=excluded.age,
            occupation=excluded.occupation,
            monthly_income=excluded.monthly_income,
            other_income=excluded.other_income,
            monthly_expenses=excluded.monthly_expenses,
            current_savings=excluded.current_savings,
            monthly_savings=excluded.monthly_savings,
            loan_amount=excluded.loan_amount,
            monthly_emi=excluded.monthly_emi,
            goal=excluded.goal
    """, (
        user_id,
        profile.get("age", 25),
        profile.get("occupation", ""),
        profile.get("monthly_income", 0),
        profile.get("other_income", 0),
        profile.get("monthly_expenses", 0),
        profile.get("current_savings", 0),
        profile.get("monthly_savings", 0),
        profile.get("loan_amount", 0),
        profile.get("monthly_emi", 0),
        profile.get("goal", "Retirement")
    ))
    conn.commit()