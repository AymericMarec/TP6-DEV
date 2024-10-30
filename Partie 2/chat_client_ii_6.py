import asyncio
import aioconsole
import sys

async def Listen(reader):
    while True:
        data = await reader.read(1024)
        if not data :
            print("\nConnexion au serveur coupé")
            sys.exit("truc")
        if not data : continue
        msg = data.decode()
        print(msg)

async def SendInput(writer):
    while True:
        input = await aioconsole.ainput()
        msg = input.encode()
        writer.write(msg)
        await writer.drain()

async def main():
    pseudo = input("Choisir votre pseudo :\n\n")

    reader, writer = await asyncio.open_connection(host="10.33.49.118", port=13337)
    writer.write(f"Hello|{pseudo}".encode())
    await writer.drain()
    tasks = [ Listen(reader), SendInput(writer) ]
    await asyncio.gather(*tasks)

if __name__ == "__main__" :
    asyncio.run(main())