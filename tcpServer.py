#  Name: Benny Shalom, ID: 203500780
import asyncio
import socket  # Server
import threading
import array as arr
import binascii
import struct
import sys
import time

ports = arr.array('i', [1111, 2222, 3333, 4444, 5555])
dict = {'benny': 9999, 'shalom': 1111, 'aaaa': 2222, 'bbbb': 1111}


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', 1111))
sock.listen(1)


def respond_to_client(conn_socket, client_address):
    try:
        print('start listening from', client_address)
        msg = str('Enter index(0-4): (0:1111, 1:2222, 2:3333, 3:4444, 4:5555) : ').strip().encode()
        start = time.time()
        conn.send(msg)
        data = conn.recv(1024)
        done = time.time()
        elapsed = done - start
        print("elapsted time:" + str(elapsed))
        print('received from', client_address, 'index chosen:', data.decode())
        chosenPort = ports[int(data.decode())]
        createNew(chosenPort)
        ports.pop(chosenPort)
        connectToRest(ports)
    except ConnectionResetError:
        print("Connection reset")
    except asyncio.TimeoutError:
        print("Connection Timeout")


def createNew(chosenPort):
    newsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    newsock.bind(('0.0.0.0', chosenPort))
    newsock.listen(1)
    while True:
        newconn, newclient_address = newsock.accept()
        print('new connection from', newclient_address)
        threading.Thread(target=newrespond_to_client, args=(newconn, newclient_address)).start()


def newrespond_to_client(newconn, newclient_address):
    while True:
        try:
            print('start listening from', newclient_address)
            start = time.time()
            newdata = newconn.recv(1024)
            print('received from', newclient_address)
            type, subtype, len, sublen = struct.unpack('>bbhh', newdata)
            if type == '0':  # request info
                data = str('none').strip().encode()
            elif type == '1':  # answer info
                if subtype == '0': # info on servers
                    data = dict.values().strip().encode()
                elif subtype == '1': # info on users
                    data = dict.keys().strip().encode()
            elif type == '2':  # define user
                if subtype == '0': # data = empty
                    data = str('empty').strip().encode()
                elif subtype == '1': # data = username
                    theport = newconn.getsockname()[1]
                    for key, value in dict.iteritems():
                        if value == theport:
                            data = key.strip().encode()
            elif type == '3':  # send message - didnt understood how, did copypaste of elif'2'
                if subtype == '0': # data = username
                    data = str('empty').strip().encode()
                elif subtype == '1': # data = empty
                    theport = newconn.getsockname()[1]
                    for key, value in dict.iteritems():
                        if value == theport:
                            data = key.strip().encode()
            else:
                data = str('empty').strip().encode()
            newconn.send(data)
            done = time.time()
            elapsed = done - start
            print("elapsted time:" + str(elapsed))
        except ConnectionResetError:
            print("Connection reset")
        except asyncio.TimeoutError:
            print("Connection Timeout")



def connectToRest(ports):
    for p in dict.values():
        newsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        newsock.bind(('0.0.0.0', p))
        newsock.listen(1)
        while True:
            newconn, newclient_address = newsock.accept()
            print('new connection from', newclient_address)
            threading.Thread(target=newrespond_to_client, args=(newconn, newclient_address)).start()


while True:
    conn, client_address = sock.accept()
    print('new connection from', client_address)
    threading.Thread(target=respond_to_client, args=(conn, client_address)).start()
