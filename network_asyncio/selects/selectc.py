# coding: utf-8
# py2 客户端
import socket


messages = ['This is the message ', 'It will be sent ', 'in parts ', '2', '3']

server_address = ('localhost', 8090)

# Create aTCP/IP socket

socks = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for i in range(10) ]

# Connect thesocket to the port where the server is listening

print ('connecting to %s port %s' % server_address)
# 连接到服务器
for s in socks:
    s.connect(server_address)

for index, message in enumerate(messages):
    # Send messages on both sockets
    for s in socks:
        print ('%s: sending "%s"' % (s.getsockname(), message + str(index)))
        s.send(bytes(message + str(index)).decode('utf-8'))
    # Read responses on both sockets

for s in socks:
    data = s.recv(1024)
    print ('%s: received "%s"' % (s.getsockname(), data))
    if data != "":
        print ('closingsocket', s.getsockname())
        s.close()
