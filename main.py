import socket
import struct
import random
import threading
import argparse

UDP_IP = "0.0.0.0"
UDP_PORT = 49678

class Profile:
    def __init__(self, dst_ip: str, src_ip: str, count: int) -> None:
        self.ip = dst_ip
        self.count = count
        self.frequency = 4294967295 // (count - 1)
        if not src_ip:
            src_ip = self.get_ip()
        
        self.src_fake_ip = self.generate_fake_ip(src_ip)

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    
    def generate_fake_ip(self, ip: str):
        ips: [str] = get_ip(struct.unpack('I', socket.inet_aton(str(ip)))[0], self)
        num = random.randint(0, len(ips)-1)
        return ips[num]
        


def get_ip(ip: int, partner: Profile) -> [str]:
    ips = []
    param = 4294967295
    for i in range(0, param, partner.frequency):
        raw_ip = (ip + i) % param
        new_ip = socket.inet_ntoa(struct.pack('I', raw_ip))
        octets: list = list(map(int, new_ip.split(".")))
        if octets[0] == 10:
            continue
        if octets[0] == 127:
            continue
        if octets[0] == 172:
            if 16 <= int(octets[1]) <= 31:
                continue
        if octets[0] == 192 and octets[1] == 168:
            continue
        ips.append(new_ip)
    return ips


def sender(sock, partner: Profile):
    while True:
        message = ' ' + input()
        print()

        ips: [str] = get_ip(struct.unpack('I', socket.inet_aton(str(partner.ip)))[0], partner)

        for ip in ips:
            sock.sendto(partner.src_fake_ip.encode() + message.encode(), (ip, UDP_PORT))


def parse_args():
    parser = argparse.ArgumentParser(description='TrashSender')
    parser.add_argument('dst_ip', type=str, help='Ip адрес получателя')
    parser.add_argument('--src_ip', dest='src_ip', type=str, required=False, help='Ip адрес отправителя')
    parser.add_argument('-c', dest='count', choices=[18, 52, 86, 256, 772, 1286],
                        default=256, help="Количество различных ip адресов для отправки")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    partner = Profile(args.dst_ip, args.src_ip, args.count)

    sock_rec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_rec.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_rec.bind((UDP_IP, UDP_PORT))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    t1 = threading.Thread(target=sender, args=(sock, partner), daemon=True)
    t1.start()

    while True:
        data, addr = sock_rec.recvfrom(10000000)
        ip, message = data.decode().split(' ', 1)
        if not ip:
            print("Invalid message:")
            print(message)
            print('Unable to answer back')
        else:
            partner.ip = ip
            print("received message: %s" % message)
            print(addr)
