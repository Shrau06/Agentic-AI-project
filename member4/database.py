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

        monthly_investment REAL,

        annual_return REAL,

        years INTEGER,

        goal REAL,

        future_wealth REAL

    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Save User Data
# -----------------------------
def save_data(investment, rate, years, goal, future):

    conn = sqlite3.connect("wealth.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO wealth_data(

        monthly_investment,
        annual_return,
        years,
        goal,
        future_wealth

    )

    VALUES(?,?,?,?,?)

    """, (
        investment,
        rate,
        years,
        goal,
        future
    ))

    conn.commit()
    conn.close()


# -----------------------------
# Read All Data
# -----------------------------
def get_data():

    conn = sqlite3.connect("wealth.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM wealth_data")

    data = cursor.fetchall()

    conn.close()

    return data


# -----------------------------
# Delete All Data
# -----------------------------
def delete_data():

    conn = sqlite3.connect("wealth.db")

    cursor = conn.cursor()

    cursor.execute("DELETE FROM wealth_data")

    conn.commit()
    conn.close()


# -----------------------------
# Create Database Automatically
# -----------------------------
create_database()