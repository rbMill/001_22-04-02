import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto(input('From client:\n>>').encode('utf-8'),('127.0.0.1',9999))
dat = client.recvfrom(1024)
print('<<',dat[0].decode('utf-8'))