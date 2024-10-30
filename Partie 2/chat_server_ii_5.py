import asyncio

async def handle_client_msg(reader,writer) :
    global CLIENTS
    addr = writer.get_extra_info('peername')
    if not addr in CLIENTS :
        CLIENTS[addr] = {}
        CLIENTS[addr]["r"] = reader
        CLIENTS[addr]["w"] = writer
        CLIENTS[addr]["pseudo"] = ""
    while True:
        
        data = await reader.read(1024)
        print(data)
        if not data :break
        if CLIENTS[addr]["pseudo"] == "":
            print("nouveau !")
            if not data[:6].decode() == "Hello|" :
                print("Le premier message n'est pas le pseudo")
                break
            CLIENTS[addr]["pseudo"] = data[6:].decode()
            for client in CLIENTS :
                if client == addr : break
                CLIENTS[client]["w"].write(f"Annonce : {data[6:].decode()} a rejoint la chatroom".encode())
                await CLIENTS[client]["w"].drain()
            continue

        message = data.decode()
        print(f"Message received from {addr[0]}:{addr[1]} : {message}")
        pseudomsg = CLIENTS[addr]["pseudo"]
        for client in CLIENTS :
            if client == addr : break
            CLIENTS[client]["w"].write(f"{pseudomsg} a dit : {message}".encode())
            await CLIENTS[client]["w"].drain()


async def main():
    server = await asyncio.start_server(handle_client_msg, '10.33.49.118', 13337)
    async with server:
        await server.serve_forever()

global CLIENTS
CLIENTS = {}

if __name__ == "__main__" :
    asyncio.run(main())