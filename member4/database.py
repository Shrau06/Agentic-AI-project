import sqlite3


# -----------------------------
# Create Database & Table
# -----------------------------
def create_database():

    conn = sqlite3.connect("wealth.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wealth_data(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER DEFAULT 0,

        monthly_investment REAL,

        annual_return REAL,

        years INTEGER,

        goal REAL,

        future_wealth REAL

    )
    """)

    # Check and migrate existing tables missing user_id column
    cursor.execute("PRAGMA table_info(wealth_data)")
    columns = [row[1] for row in cursor.fetchall()]
    if "user_id" not in columns:
        try:
            cursor.execute("ALTER TABLE wealth_data ADD COLUMN user_id INTEGER DEFAULT 0")
        except Exception as e:
            print(f"Migration notice: {e}")

    conn.commit()
    conn.close()


# -----------------------------
# Save User Data
# -----------------------------
def save_data(investment, rate, years, goal, future, user_id=0):

    conn = sqlite3.connect("wealth.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO wealth_data(

        user_id,
        monthly_investment,
        annual_return,
        years,
        goal,
        future_wealth

    )

    VALUES(?,?,?,?,?,?)

    """, (
        user_id,
        investment,
        rate,
        years,
        goal,
        future
    ))

    conn.commit()
    conn.close()


# -----------------------------
# Read User Data
# -----------------------------
def get_data(user_id=None):

    conn = sqlite3.connect("wealth.db")

    cursor = conn.cursor()

    if user_id is not None:
        cursor.execute("SELECT * FROM wealth_data WHERE user_id=?", (user_id,))
    else:
        cursor.execute("SELECT * FROM wealth_data")

    data = cursor.fetchall()

    conn.close()

    return data


# -----------------------------
# Delete User Data
# -----------------------------
def delete_data(user_id=None):

    conn = sqlite3.connect("wealth.db")

    cursor = conn.cursor()

    if user_id is not None:
        cursor.execute("DELETE FROM wealth_data WHERE user_id=?", (user_id,))
    else:
        cursor.execute("DELETE FROM wealth_data")

    conn.commit()
    conn.close()


# -----------------------------
# Create Database Automatically
# -----------------------------
create_database()