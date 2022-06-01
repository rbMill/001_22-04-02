import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.bind(('127.0.0.1',9999))

msg,address = server.recvfrom(1024)

print('<<',msg.decode('utf-8'))

server.sendto(input( 'From Server\n>>').encode('utf-8'),address)