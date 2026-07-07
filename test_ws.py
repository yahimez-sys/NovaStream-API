import asyncio
import websockets


async def main():

    uri = "ws://127.0.0.1:8000/ws"

    async with websockets.connect(uri) as ws:

        print("Conectado correctamente")

        await ws.send("hola")

        while True:

            msg = await ws.recv()

            print(msg)


asyncio.run(main())