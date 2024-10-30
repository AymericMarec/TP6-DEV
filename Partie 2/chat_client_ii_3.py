import asyncio
import aioconsole

async def Listen(reader):
    while True:
        data = await reader.read(1024)
        if not data : continue
        msg = "Message recu : " + data.decode()
        print(msg)

async def SendInput(writer):
    while True:
        input = await aioconsole.ainput()
        msg = input.encode()
        writer.write(msg)
        await writer.drain()

async def main():
    reader, writer = await asyncio.open_connection(host="10.33.49.118", port=13337)

    tasks = [ Listen(reader), SendInput(writer) ]
    await asyncio.gather(*tasks)

if __name__ == "__main__" :
    asyncio.run(main())