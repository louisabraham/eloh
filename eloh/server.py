import socket
from argparse import ArgumentParser


from .common import serialize_addr, OK


def server(port):
    s = socket.socket()
    s.bind(("0.0.0.0", port))
    s.listen(5)

    rendez_vous = {}

    while True:

        conn, addr = s.accept()
        print(f"new connection from {addr}")

        rdv = conn.recv(2048)

        if rdv in rendez_vous:
            print(f"found: {rdv.hex()}")
            conn.send(serialize_addr(*rendez_vous[rdv]))

        else:
            rendez_vous[rdv] = addr
            print(f"created: {rdv.hex()}")
            conn.send(OK)


def main():
    parser = ArgumentParser()
    parser.add_argument("port", type=int)

    args = parser.parse_args()
    server(args.port)


if __name__ == "__main__":
    main()

