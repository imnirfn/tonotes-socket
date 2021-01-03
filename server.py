#!/usr/bin/env python3

import requests
import websockets
import asyncio
import socket
import os
from _thread import start_new_thread
from requests.exceptions import HTTPError

class server(object):
    def __init__(self, host, port, wsport):
        self.host = host
        self.port = port
        self.wsport = wsport
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
        self.sendOverWebsocket(bytes)

    def sendOverWebsocket(self, bytes):
        async def sendMsg(websocket, path):
            await websocket.send(bytes)

        start_server = websockets.serve(sendMsg, self.host, self.wsport)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    def server(self):
        # TO-DO

    def HTTPRequest (addr):
        try:
            receive = requests.get(addr)

        except HTTPError as httperr:
            print (f'HTTP error occured : {httperr}')
            msg = "Unsucessfull to get HTTP Request !"

        except Exception as err:
            print (f'Other error occured : {err}')
            msg = "Unsuccessfull to get HTTP Request !"

        else:
            msg = "Sucessfully get Http Request ! "

        return msg

if __name__ == '__main__':
    try:
        serve = server('localhost', 13337, 13338)
        serve.listen()
    except socket.error as e:
        print("Error here: ", str(e))
