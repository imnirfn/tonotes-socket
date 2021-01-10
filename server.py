#!/usr/bin/env python3

import requests
import websockets
import asyncio
import socket
import os
from _thread import start_new_thread


class server(object):
    def __init__(self, host, port, wsport):
        self.host = host
        self.port = port
        self.wsport = wsport
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))

    def listen(self):
        self.socket.listen(7)
        while True:
            client, addr = self.socket.accept()
            start_new_thread(self.listenToClient, (client, addr))

    def listenToClient(self, client, addr):
        data = client.recv(1024)
        print('data', data)
        sendmsg = self.server()
        bytes = sendmsg.encode()
        self.sendOverWebsocket(bytes)

    def sendOverWebsocket(self, bytes):
        async def sendMsg(websocket, path):
            await websocket.send(bytes)

        start_server = websockets.serve(sendMsg, self.host, self.wsport)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    def server(self):
        # TO-DO
        url = 'http://localhost:3000/notes'
        response = requests.get(url)
        print(response.text)
        return response.text


if __name__ == '__main__':
    try:
        serve = server('localhost', 13337, 13338)
        print('Server started')
        serve.listen()
    except socket.error as e:
        print("Error here: ", str(e))
