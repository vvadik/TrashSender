import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 49678

sock_rec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_rec.bind((UDP_IP, UDP_PORT))


data, addr = sock_rec.recv(10000)  # buffer size is 1024 bytes
print("received message: %s" % data)