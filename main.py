import socket
import struct
import random
import asyncio
from multiprocessing import Process
import threading

MY_IP: str = '193.151.222.197'
UDP_IP = "0.0.0.0"
UDP_PORT = 49678


def get_ip(ip: int, count: int) -> [str]:
    ips = []
    print(ip)
    param = 4294967295
    count *= 100000
    for i in range(-count, count, 100000):
        hash = (ip + i) % param
        new_ip = socket.inet_ntoa(struct.pack('I', hash))
        octets: list = list(map(int, new_ip.split(".")))
        if octets[0] == 10:
            continue
        if octets[0] == 172:
            if 16 <= int(octets[1]) <= 31:
                continue
        if octets[0] == 192 and octets[1] == 168:
            continue

        ips.append(new_ip)
    return ips


def sender(ips: [str], sock):
    while True:
        num = random.randint(0, len(ips))
        faked_ip = ips[num]
        message = input()
        print(message)
        for ip in ips:
            sock.sendto(faked_ip.encode() + message.encode(), (ip, 49678))


def listener(sock_rec):
    while True:
        data, addr = sock_rec.recv(10000)  # buffer size is 1024 bytes
        print("received message: %s" % data)


if __name__ == '__main__':
    sock_rec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_rec.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_rec.bind((UDP_IP, UDP_PORT))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ips: [str] = get_ip(struct.unpack('I', socket.inet_aton(MY_IP))[0], 13)

    t1 = threading.Thread(target=sender, args=(ips, sock), daemon=True)
    t1.start()
    while True:
        data, addr = sock_rec.recv(10000)  # buffer size is 1024 bytes
        print("received message: %s" % data)
