import asyncio

async def handle_client_msg(reader,writer) :
    global CLIENTS
    addr = writer.get_extra_info('peername')
    if not addr in CLIENTS :
        CLIENTS[addr] = {}
        CLIENTS[addr]["r"] = reader
        CLIENTS[addr]["w"] = writer
    while True:
        data = await reader.read(1024)

        if not data :break
        message = data.decode()
        print(f"Message received from {addr[0]}:{addr[1]} : {message}")
        for client in CLIENTS :
            print(client)
            if client == addr : break
            print("message envoyé a un autre !")
            CLIENTS[client]["w"].write(f"{addr[0]}:{addr[1]} a dit : {message}".encode())
            await CLIENTS[client]["w"].drain()


async def main():
    server = await asyncio.start_server(handle_client_msg, '10.33.49.118', 13337)
    async with server:
        await server.serve_forever()

global CLIENTS
CLIENTS = {}

if __name__ == "__main__" :
    asyncio.run(main())