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
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))

    def listen(self):
        self.socket.listen(7)
        while True:
            client, addr = self.socket.accept()
            print('Connection from: ' str(addr))
            start_new_thread(self.listenToClient, (client, addr))

    def listenToClient(self, client, addr):
        val = client.recv(1024).decode('utf-8')
        if val != None:
            sendmsg = self.handler(val)
            bytes = sendmsg.encode()
            # upgrade raw socket connection to ws
            sendOverWebsocket(bytes)

    def sendOverWebsocket(self, bytes):
        async def sendMsg(websocket, path):
            await websocket.send(bytes)

        start_server = websockets.serve(sendMsg, self.host, self.wsport)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    def handler(self, val):
        # TO-DO
        url = 'http://localhost:3000/notes'
        if val.type == 'gn':
            res = requests.get(url)
            return res.text
        elif val.type == 'pn':
            requests.patch(url, data = {
                title: val.title,
                description: val.description,
                isComplete: val.isComplete,
                userId: val.userId
            })
            res = requests.get(url)
            return res.text
        elif data.type == 'an':
            requests.post(url, data = {
                title: val.title,
                description: val.description,
                isComplete: val.isComplete,
                userId: val.userId
            })
            res = requests.get(url)
            return res.text

if __name__ == '__main__':
    try:
        serve = server('localhost', 13337, 13338)
        serve.listen()
    except socket.error as e:
        print("Error here: ", str(e))
