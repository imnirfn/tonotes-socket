import asyncio
import websockets

async def con():
    uri = "ws://localhost:13337" #
    async with websockets.connect(uri) as websocket :
        print ('Test')
        #start process to send and recv

asyncio.get_event_loop().run_until_complete(con())
