import socket
import struct


SOURCE: str = '213.159.195.33'
MY_IP: str = '213.159.195.33'
# MY_IP = '101.112.199.33'
# MY_IP = '45.62.195.33'


def get_ip(ip: str, count: int) -> [str]:
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
        print(new_ip)
    return ips


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ips: list = get_ip(struct.unpack('I', socket.inet_aton(MY_IP))[0], 13)
    for ip in ips:
        sock.sendto(b'hello', (ip, 49678))


if __name__ == '__main__':
    main()
