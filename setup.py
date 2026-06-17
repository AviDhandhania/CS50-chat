import os
import sqlite3

if os.path.exists("chat.db"):
    os.remove("chat.db")
conn = sqlite3.connect('chat.db')

with open("schema.sql") as f:
    conn.executescript(f.read())

conn.commit()
conn.close()

print("Database created successfully!")

exit()