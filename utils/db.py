import sqlite3

def save_to_db(prompt, response, reference, score, timestamp):
    conn = sqlite3.connect("logs/prompt_logs.db")
    c = conn.cursor()

    # Create table if it doesn't exist
    c.execute("""
        CREATE TABLE IF NOT EXISTS prompt_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            response TEXT,
            reference TEXT,
            score REAL,
            timestamp TEXT
        )
    """)

    # Insert the new log
    c.execute("INSERT INTO prompt_logs (prompt, response, reference, score, timestamp) VALUES (?, ?, ?, ?, ?)",
              (prompt, response, reference, score, timestamp))

    conn.commit()
    conn.close()
