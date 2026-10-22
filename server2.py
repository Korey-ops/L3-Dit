import sqlite3
import hashlib
import socket
import threading
import json
from contextlib import closing

HOST, PORT = "192.168.1.116", 1111   # 0.0.0.0 = accept connections from other machines


#send a json message to the client with a newline on the end
def send(c, obj):
    c.sendall((json.dumps(obj) + "\n").encode())


#hash the password and check it against the database
def check_login(username, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    print(username)
    with closing(sqlite3.connect("userdata.db")) as conn:
        row = conn.execute(
            "SELECT 1 FROM userdata WHERE username = ? AND password = ?",
            (username, hashed)).fetchone()
    return row is not None


#deal with one client for as long as they are connected
def handle_connection(c):
    f = c.makefile("r", encoding="utf-8")
    
    user = None                      # who is logged in on THIS connection
    try:
        for line in f:               # one JSON message per line
            #turn the line into a dictionary
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                send(c, {"ok": False, "error": "bad message"})
                continue

            action = msg.get("action")

            #log the user in
            if action == "login":
                u, p = msg.get("username", ""), msg.get("password", "")
                if u and check_login(u, p):
                    user = u
                    send(c, {"ok": True, "is_admin": u == "admin"})
                else:
                    user = None
                    send(c, {"ok": False})

            #block everything below if not logged in
            elif user is None:
                send(c, {"ok": False, "error": "not logged in"})

            #log the user out
            elif action == "logout":
                user = None
                send(c, {"ok": True})

            #add a new job to the database
            elif action == "submit_job":
                with closing(sqlite3.connect("jobs.db")) as conn:
                    conn.execute(
                        "INSERT INTO jobs (name, location, type, urgency, task) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (msg["name"], msg["location"], msg["type"],
                         msg["urgency"], msg["task"]))
                    conn.commit()
                send(c, {"ok": True})

            #send all the jobs back but only to the admin
            elif action == "get_jobs":
                if user != "admin":
                    send(c, {"ok": False, "error": "admin only"})
                else:
                    with closing(sqlite3.connect("jobs.db")) as conn:
                        rows = conn.execute(
                            "SELECT id, name, location, type, urgency, task FROM jobs"
                        ).fetchall()
                    send(c, {"ok": True, "jobs": rows})

            #remove a job by its id but only for the admin
            elif action == "delete_job":
                if user != "admin":
                    send(c, {"ok": False, "error": "admin only"})
                else:
                    with closing(sqlite3.connect("jobs.db")) as conn:
                        conn.execute("DELETE FROM jobs WHERE id = ?", (msg["id"],))
                        conn.commit()
                    send(c, {"ok": True})

            #anything else isnt a real action
            else:
                send(c, {"ok": False, "error": "unknown action"})
    except Exception as e:
        print(f"connection error: {e}")
    finally:
        #always close the connection at the end
        c.close()


#set up the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print(f"listening on {PORT}")

#wait for clients and give each one its own thread
while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_connection, args=(conn,), daemon=True).start()