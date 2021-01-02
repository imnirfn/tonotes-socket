#!/usr/bin/env python3

import requests
import socket
import os
from _thread import *

class server(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))

    def listen(self):
        self.socket.listen(5)
        while True:
            client, addr = self.socket.accept()
            start_new_thread(self.listenToClient, (client, addr))

    def listenToClient(self, client, addr):
        sendmsg = self.server()
        bytes = sendmsg.encode()
        client.send(bytes)
        client.close()

    def server(self):
        # TO-DO
        return 'data'

if __name__ == '__main__':
    try:
        serve = server('localhost', 13337)
        serve.listen() 
    except socket.error as e:
        print("Error here: ", str(e))
