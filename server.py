import sqlite3
import hashlib
import socket
import threading


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 1111))

server.listen()


def handle_connection(c) :\

    username = client.recv(1024)
    password = client.recv(1024)
    
    


    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

    if cur.fetchall():
        print("sending success")
        c.send("login successful!".encode())
    else:
        print("sending failure")
        c.send("login failed!".encode())


while True:
    client, addr = server.accept()
    threading.Thread(target=handle_connection, args=(client, )).start()

