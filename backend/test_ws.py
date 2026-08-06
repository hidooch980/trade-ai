import asyncio
import websockets

async def main():
    uri="ws://127.0.0.1:8000/ws/market"
    async with websockets.connect(uri, origin="http://localhost") as ws:
        print("CONNECTED")
        while True:
            print(await ws.recv())

asyncio.run(main())
