import socket
import struct
import secrets

TOKEN_LENGTH = 2


def new_token():
    return secrets.token_bytes(TOKEN_LENGTH)


OK = b"\x00"
ADDR = "!4sH"


def serialize_addr(ip, port):
    return struct.pack(ADDR, socket.inet_aton(ip), port)


def deserialize_addr(packed):
    ip, port = struct.unpack(ADDR, packed)
    ip = socket.inet_ntoa(ip)
    return ip, port

