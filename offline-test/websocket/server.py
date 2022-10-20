import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def main():
    async with websockets.serve(echo, "0.0.0.0", 9000):
        await asyncio.Future()  # run forever

asyncio.run(main())