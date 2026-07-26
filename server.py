import sqlite3
import hashlib
import socket
import threading


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 1111))


server.listen()


def handle_connection(c) :
    try:
        while True:

            username = client.recv(1024).strip().decode()
            password = client.recv(1024).strip().decode()

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if not username:
                 break
    
    


            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()

            cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, hashed_password))
            verdict = cur.fetchall()

            if verdict:
             print("sending success")
             c.send("login successfull!".encode())
            else:
                print("sending failure")
                c.send("login failed!".encode())
    except Exception as e:
        print(f"connection error {e}")
    finally:
        c.close()


while True:
    client, addr = server.accept()
    threading.Thread(target=handle_connection, args=(client, )).start()

