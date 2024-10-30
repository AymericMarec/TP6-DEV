import asyncio

async def SendBroadCastMessage(who,message):
    for client in CLIENTS :
        if client == who : 
            continue
        CLIENTS[client]["w"].write(message.encode())
        await CLIENTS[client]["w"].drain()
async def handle_client_msg(reader,writer) :
    global CLIENTS
    addr = writer.get_extra_info('peername')
    if not addr in CLIENTS :
        CLIENTS[addr] = {}
        CLIENTS[addr]["r"] = reader
        CLIENTS[addr]["w"] = writer
        CLIENTS[addr]["pseudo"] = ""
    while True:
        pseudo = CLIENTS[addr]["pseudo"]
        data = await reader.read(1024)
        if not data :
            pseudo = CLIENTS[addr]["pseudo"]
            message = f"Annonce : {pseudo} a quitté la chatroom"
            await SendBroadCastMessage(addr,message)
            CLIENTS.pop(addr)

            break
        #Arrivé de l"utilisateur
        if pseudo == "":
            print("nouveau !")
            if not data[:6].decode() == "Hello|" :
                print("Le premier message n'est pas le pseudo")
                break
            pseudo = data[6:].decode()
            CLIENTS[addr]["pseudo"] = pseudo
            message = "Annonce : " + pseudo + " a rejoint la chatroom"
            await SendBroadCastMessage(addr,message)
            continue

        #gestions des messages de l'utilisateurs
        pseudo = CLIENTS[addr]["pseudo"]
        message = pseudo + " a dit : "+ data.decode()
        print(f"Message received from {addr[0]}:{addr[1]} : {message}")
        await SendBroadCastMessage(addr,message)

async def main():
    server = await asyncio.start_server(handle_client_msg, '10.33.49.118', 13337)
    async with server:
        await server.serve_forever()

global CLIENTS
CLIENTS = {}

if __name__ == "__main__" :
    asyncio.run(main())