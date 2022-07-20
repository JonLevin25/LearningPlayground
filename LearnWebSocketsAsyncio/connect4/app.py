#!/usr/bin/env/python

import asyncio
import websockets


async def handler(websocket):
    while True:
        try:
            message = await websocket.recv()
            print(message)
            await websocket.send(message)
        except websockets.ConnectionClosedOK:
            break
    print('connection closed')


async def async_main():
    async with await websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(async_main())
