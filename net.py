import socket
import json

SERVER_HOST = "192.168.1.116"
SERVER_PORT = 1111

_sock = None
_file = None
_creds = None   # remembered after a successful login


def _reset():
    global _sock, _file
    try:
        if _sock:
            _sock.close()
    except OSError:
        pass
    _sock = None
    _file = None


def _send(msg):
    _sock.sendall((json.dumps(msg) + "\n").encode())
    line = _file.readline()
    if not line:
        raise ConnectionError("server closed the connection")
    return json.loads(line)


def request(msg):
    global _sock, _file, _creds
    try:
        if _sock is None:
            _sock = socket.create_connection((SERVER_HOST, SERVER_PORT), timeout=15)
            _file = _sock.makefile("r", encoding="utf-8")
            print("opened new connection")
            # new connection starts logged out, so log back in first
            if _creds and msg.get("action") != "login":
                _send({"action": "login", **_creds})

        response = _send(msg)

        if msg.get("action") == "login":
            _creds = ({"username": msg["username"], "password": msg["password"]}
                      if response.get("ok") else None)
        elif msg.get("action") == "logout":
            _creds = None
        return response
    except Exception:
        _reset()
        raise