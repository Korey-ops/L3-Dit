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
username2, password2 = "June", hashlib.sha256("Crawford".encode()).hexdigest()
username3, password3 = "Kate", hashlib.sha256("Fox".encode()).hexdigest()
username4, password4 = "Kerry", hashlib.sha256("MacKenzie".encode()).hexdigest()
username5, password5 = "James", hashlib.sha256("Bailey".encode()).hexdigest()
username6, password6 = "Lana", hashlib.sha256("Richards".encode()).hexdigest()
cur.execute("INSERT INTO userdata (username, password) Values (?, ?)", (username1, password1))
cur.execute("INSERT INTO userdata (username, password) Values (?, ?)", (username2, password2))

print(password1)

conn.commit()