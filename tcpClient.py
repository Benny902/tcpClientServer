import socket  # main Client
import struct
import atexit


def exit_handler():  # to close the socket before exiting program so that i can connect again to same port
    sock.close()
    print ('program end, socket closed')

atexit.register(exit_handler)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.connect(('127.0.0.1', 1111))  # server ip, port


print('successful connection')



def SecondaryClient(port):
    newsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    newsock.connect(('127.0.0.1', port))  # server ip, port

    print('successful connection')

    while True:
        type = 0
        type = input('Enter type(0-3):')
        subtype = 0
        len = 0
        sublen = 0
        if type == '0':  # request info
            subtype = input('Enter subtype(0-1):')
            data = struct.pack('>bbhh', int(type), int(subtype), len, sublen)
        elif type == '1':  # answer info
            subtype = input('Enter subtype(0-1)::')
            data = struct.pack('>bbhh', int(type), int(subtype), len, sublen)
        elif type == '2':  # define user
            subtype = input('Enter subtype(0-1):')
            data = struct.pack('>bbhh', int(type), int(subtype), len, sublen)
        elif type == '3':  # send message
            data = struct.pack('>bbhh', int(type), int(subtype), len, sublen)
        else:
            print("Wrong number, must be 0-3")
        # data = input('Enter message:').strip().encode()
        newsock.send(data)
        reply_data = newsock.recv(1024)
        print('server reply:', reply_data.decode())

while True:
    reply_data = sock.recv(1024)
    print('server reply:', reply_data.decode())
    index = input('Enter:')
    data = index.strip().encode()
    sock.send(data)
    #Enter index(0-4): (0:1111, 1:2222, 2:3333, 3:4444, 4:5555) :
    if index == '0':
        SecondaryClient(1111)
    elif index == '1':
        SecondaryClient(2222)
    elif index == '2':
        SecondaryClient(3333)
    elif index == '3':
        SecondaryClient(4444)
    elif index == '4':
        SecondaryClient(5555)
    else:
        print('index must be 0-4')

