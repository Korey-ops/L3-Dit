import sqlite3
import hashlib

conn = sqlite3.connect("userdata.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS userdata (
    
    id INTEGER PRIMARY KEY  ,
    username VARCHAR(2555) NOT NULL,
    Password VARCHAR(255) not NULL)

            """)

username1, password1 = "admin", hashlib.sha256("admin".encode()).hexdigest()
username2, password3 = "user", hashlib.sha256("user".encode()).hexdigest()
cur.execute("INSERT INTO userdata (username, password) Values (?, ?)", (username1, password1))

print(password1)

conn.commit()