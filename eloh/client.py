import socket
from io import BytesIO
import sys
import argparse

from .common import deserialize_addr, OK, new_token

from tqdm.autonotebook import tqdm


def connect(hostname: str, port: int, rdv: bytes):
    server_conn = socket.create_connection((hostname, port))
    out_port = server_conn.getsockname()[1]

    server_conn.send(rdv)
    resp = server_conn.recv(8)

    if resp == OK:
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", out_port))
        s.listen(1)
        conn, addr = s.accept()
    else:
        addr = deserialize_addr(resp)
        conn = socket.create_connection(addr)

    server_conn.close()

    return conn


def _send(conn, data):
    if data is None:
        with tqdm(
            desc="Sending data", unit="B", unit_scale=True, unit_divisor=1024
        ) as pbar:
            while True:
                b = sys.stdin.buffer.read(4096)
                conn.send(b)
                if not b:
                    break
                pbar.update(len(b))
    elif isinstance(data, bytes):
        conn.send(data)
    else:
        conn.sendfile(data)


def send(hostname: str, port: int, rdv: bytes, data):
    conn = connect(hostname, port, rdv)
    return _send(conn, data)


def _recv(conn, buffer=None):
    if buffer is None:
        with tqdm(
            desc="Receiving data", unit="B", unit_scale=True, unit_divisor=1024
        ) as pbar:
            while True:
                b = conn.recv(4096)
                sys.stdout.buffer.write(b)
                if not b:
                    break
                pbar.update(len(b))
    elif isinstance(buffer, BytesIO):
        conn.recv_into(buffer.getbuffer())
    else:
        conn.recv_into(buffer)
    return buffer


def recv(hostname: str, port: int, rdv: bytes, buffer=None):
    conn = connect(hostname, port, rdv)
    return _recv(conn, buffer)


def send_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname")
    parser.add_argument("port", type=int)
    parser.add_argument("--rdv", default=None, type=bytes.fromhex)
    parser.add_argument("file", nargs="?", type=argparse.FileType("rb"), default=None)

    args = parser.parse_args()
    if not args.rdv:
        args.rdv = new_token()
        print(
            f"Receive with:\n\n    eloh-recv --rdv {args.rdv.hex()} {args.hostname} {args.port} > file\n",
            file=sys.stderr,
        )

    send(args.hostname, args.port, args.rdv, args.file)
    print("Sent file", file=sys.stderr)


def recv_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname")
    parser.add_argument("port", type=int)
    parser.add_argument("--rdv", default=None, type=bytes.fromhex)

    args = parser.parse_args()
    if not args.rdv:
        args.rdv = new_token()
        print(
            f"Send with:\n\n    eloh-send --rdv {args.rdv.hex()} {args.hostname} {args.port} file\n",
            file=sys.stderr,
        )

    recv(args.hostname, args.port, args.rdv)

