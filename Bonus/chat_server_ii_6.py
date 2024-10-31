import asyncio
import random
import time
import datetime
import argparse
import re
import psutil
import aiofiles
import json

def GetInfos():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", action="store")
    parser.add_argument("-l", "--listen", action="store")
    parser.add_argument("-hp", "--path", action="store")
    args = parser.parse_args()
    if(args.port == None):
        port = 13337 
    else :
        ValidePort(args.port)
        port = args.port

    if(args.listen == None):
        host = ''
    else :
        ValideIP(args.listen)
        host = args.listen
    if args.path == None : historic = ""
    else : historic = args.path
    return port,host,historic

def ValidePort(port):
    try:
        port = int(port)
        if port < 0 or port > 65535:
            print(f"-p argument invalide. Le port spécifié {port} n'est pas un port valide (de 0 à 65535)")
            exit(1)
        elif port < 1024:
            print(f"ERROR -p argument invalide. Le port spécifié {port} est un port privilégié. Spécifiez un port au dessus de 1024.")
            exit(2)

    except:
        raise TypeError("Le port ca doit etre un nombre hein")

def ValideIP(ip):
    if not re.search(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$",ip) :
        print(f"ERROR -l argument invalide. L'adresse {ip} n'est pas une adresse IP valide.")
        exit(3)
    elif not ip in str(psutil.net_if_addrs()):
        print(f"ERROR -l argument invalide. L'adresse {ip} n'est pas l'une des adresses IP de cette machine.")
        exit(4)

async def GetHistoric(room):
    global historicPath
    try :
        async with aiofiles.open(historicPath+f"/{room}.json", "r",encoding="utf-8") as file:
            content = await file.read() #   On lit dans le fichier json
            try :   #   Si il y a du contenu
                data = json.loads(content)
            except :
                return None
        return data
    except :
        return None
    


async def AddHistoric(message,room):
    global historicPath
    Historic = await GetHistoric(room)
    if Historic == None:    #   Si le fichier est vide
        Historic = {}
        Historic["msg"] = []
    Historic["msg"].append(message)  
    async with aiofiles.open(historicPath+f"/{room}.json", "w",encoding="utf-8") as file:
        await file.write(json.dumps(Historic))
        await file.flush()

async def DisplayHistoric(writer,room):
    historic = await GetHistoric(room)
    if not historic : return
    if len(historic["msg"]) > 50:
        await DeletHistoric(room)
    for msg in historic["msg"]:
        writer.write((msg+"\n").encode())
        await writer.drain()

async def DeletHistoric(room):
    global historicPath
    Historic = await GetHistoric()
    Historic["msg"] = Historic["msg"][-50:] 
    print(Historic)
    async with aiofiles.open(historicPath+f"/{room}.json", "w",encoding="utf-8") as file:
        await file.write(json.dumps(Historic))
        await file.flush()

async def SendBroadCastMessage(who,message,room):
    message+= '\033[0m'
    for client in CLIENTS :
        if(CLIENTS[client]["room"] == room):
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
        CLIENTS[addr]["room"] = 1
    await DisplayHistoric(writer,1)
    while True:

        pseudo = CLIENTS[addr]["pseudo"]
        #Si l'utilisateur vient d'arriver
        if pseudo == "":
            LenPseudo = await reader.read(1)
            pseudo = (await reader.read(int.from_bytes(LenPseudo))).decode()
            CLIENTS[addr]["pseudo"] = pseudo
            message = "\033[38;5;208m"+"Annonce : " + pseudo + " a rejoint la chatroom"
            await AddHistoric(message,1)
            await SendBroadCastMessage(addr,message,1)
            continue

        header1 = await reader.read(1)#   on recupere le type de message
        headerNB = int.from_bytes(header1)
        if(headerNB == 1):   #   si le message est court
            LenMess = await reader.read(1)
            data = await reader.read(int.from_bytes(LenMess))
        elif headerNB == 2:  #   si le message est long 
            LenLen = await reader.read(1)
            LenMess = await reader.read(int.from_bytes(LenLen))
            data = await reader.read(int.from_bytes(LenMess))
        elif headerNB == 3:  #   Changement de room
            LenNB = await reader.read(2)
            print(int.from_bytes(LenNB))
            RoomNB = await reader.read(int.from_bytes(LenNB))
            RoomNB = int.from_bytes(RoomNB) 
            #On afficher le message de deconnexion          
            message = "\033[38;5;208m"+f"Annonce : {pseudo} a quitté la chatroom"
            await AddHistoric(message,CLIENTS[addr]["room"])
            await SendBroadCastMessage(addr,message,CLIENTS[addr]["room"])

            CLIENTS[addr]["room"] = RoomNB  #   On change la room

            #On affiche le message de connexion
            await DisplayHistoric(writer,RoomNB)
            message = "\033[38;5;208m"+"Annonce : " + pseudo + " a rejoint la chatroom"
            await AddHistoric(message,RoomNB)
            await SendBroadCastMessage(addr,message,RoomNB)

            continue
        elif not header1 :  #   si on recoit juste aucune données
            message = "\033[38;5;208m"+f"Annonce : {pseudo} a quitté la chatroom"
            await AddHistoric(message,CLIENTS[addr]["room"])
            await SendBroadCastMessage(addr,message,CLIENTS[addr]["room"])
            CLIENTS.pop(addr)

            break
        else :
            print("Message inconnu recu")
            continue
        #On envoie le message a tout le monde
        color = CLIENTS[addr]["color"]
        room = CLIENTS[addr]["room"]
        message = f"{color}{GetTime()} [{room}][{pseudo}] : {data.decode()}"
        await AddHistoric(message,CLIENTS[addr]["room"])
        print(f"Message received from {addr[0]}:{addr[1]} : {message}")
        await SendBroadCastMessage(addr,message,CLIENTS[addr]["room"])

async def main():
    global historicPath
    port,host,historicPath = GetInfos()
    server = await asyncio.start_server(handle_client_msg, host, port)
    async with server:
        await server.serve_forever()

global CLIENTS
CLIENTS = {}
global historicPath
historicPath = ""
if __name__ == "__main__" :
    asyncio.run(main())