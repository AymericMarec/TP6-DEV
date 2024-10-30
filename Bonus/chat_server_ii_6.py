import asyncio
import random
import time
import datetime
async def SendBroadCastMessage(who,message):
    message+= '\033[0m'
    for client in CLIENTS :
        if client == who : 
            continue
        CLIENTS[client]["w"].write(message.encode())
        await CLIENTS[client]["w"].drain()

def GenerateColor():
    Colors = ['\033[31m','\033[32m','\033[33m','\033[34m','\033[35m','\033[36m','\033[37m','\033[90m','\033[91m','\033[92m','\033[93m','\033[94m','\033[95m','\033[96m']
    rand = random.randint(0, len(Colors)-1)
    return Colors[rand]

def GetTime():
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
    return date

async def handle_client_msg(reader,writer) :
    global CLIENTS
    addr = writer.get_extra_info('peername')
    #si il n'est pas deja connecté
    if not addr in CLIENTS :
        CLIENTS[addr] = {}
        CLIENTS[addr]["r"] = reader
        CLIENTS[addr]["w"] = writer
        CLIENTS[addr]["pseudo"] = ""
        CLIENTS[addr]["color"] = GenerateColor()
    while True:

        pseudo = CLIENTS[addr]["pseudo"]
        #Si l'utilisateur vient d'arriver
        if pseudo == "":
            LenPseudo = await reader.read(1)
            print(int.from_bytes(LenPseudo))
            pseudo = (await reader.read(int.from_bytes(LenPseudo))).decode()
            print(pseudo)
            CLIENTS[addr]["pseudo"] = pseudo
            message = "Annonce : " + pseudo + " a rejoint la chatroom"
            await SendBroadCastMessage(addr,message)
            continue

        header1 = await reader.read(1)#   on recupere le type de message
        if(int.from_bytes(header1) == 1):   #   si le message est court
            LenMess = await reader.read(1)
            data = await reader.read(int.from_bytes(LenMess))
        elif int.from_bytes(header1) == 2:  #   si le message est long 
            LenLen = await reader.read(1)
            LenMess = await reader.read(int.from_bytes(LenLen))
            data = await reader.read(int.from_bytes(LenMess))
        elif not header1 :  #   si on recoit juste aucune données
            message = f"Annonce : {pseudo} a quitté la chatroom"
            await SendBroadCastMessage(addr,message)
            CLIENTS.pop(addr)

            break
        #On envoie le message a tout le monde
        color = CLIENTS[addr]["color"]
        message = f"{color}{GetTime()} | {pseudo} a dit : {data.decode()}"
        print(f"Message received from {addr[0]}:{addr[1]} : {message}")
        await SendBroadCastMessage(addr,message)

async def main():
    server = await asyncio.start_server(handle_client_msg, '192.168.1.21', 13337)
    async with server:
        await server.serve_forever()

global CLIENTS
CLIENTS = {}

if __name__ == "__main__" :
    asyncio.run(main())