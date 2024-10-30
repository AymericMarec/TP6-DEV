import asyncio
import aioconsole
import sys
from ascii_magic import AsciiArt

def CalculTailleOctet(Nb):
    bit = 0
    while True:
        bit+=1
        if Nb < 2**bit :
            if(bit%8==0):
                return int(bit/8)
            else: 
                return int((bit/8)+1)


async def Listen(reader):
    while True:
        data = await reader.read(1024)
        if not data :
            print("\nConnexion au serveur coupé")
            sys.exit("truc")
        if not data : continue
        msg = data.decode()
        print(msg)

def Command(input):
    command = input[1:].split(" ")[0]
    match command :
        case "di":
            try:
                ImagePath = input[1:].split(" ")[1]
            except:
                print("Pas d'image donné")
                return None,None
            try:
                my_art = AsciiArt.from_image(ImagePath)
                return "Image",my_art
            except:
                print("Mauvais chemin")
                return None,None
        case _:
            print("Commande inconnu")
            return None,None


async def SendInput(writer):
    while True:
        input = await aioconsole.ainput()
        try:
            if(input[0] == "/"):
                type,result = Command(input)
                if type == None : continue
                if(type=="Image"):
                    image = result.to_terminal()
                    await SendMessage(image,writer)
                continue
        except:
            continue
        await SendMessage(input,writer)

async def SendMessage(message,writer):
    LenMess = len(message) # on calcule la taille du message
    Header2 = CalculTailleOctet(LenMess) # on calcule la taille en octet de cette taille
    if Header2 == 1: # si la taille en octet de la taille du message est superieur a 1 octet (trop compliqué a comprendre comme phrase)
        writer.write(Header2.to_bytes())
        writer.write(LenMess.to_bytes())
        writer.write(message.encode())
        await writer.drain()
    else :
        deux = 2
        writer.write(deux.to_bytes())
        writer.write(Header2.to_bytes())
        writer.write(LenMess.to_bytes(Header2))
        writer.write(message.encode())
        await writer.drain()


async def main():
    pseudo = input("Choisir votre pseudo :\n\n")
    if(len(pseudo)>15):
        print("pseudo trop long")
        return
    reader, writer = await asyncio.open_connection(host="192.168.1.21", port=13337)
    writer.write(len(pseudo).to_bytes())
    writer.write(pseudo.encode())
    await writer.drain()
    tasks = [ Listen(reader), SendInput(writer) ]
    await asyncio.gather(*tasks)

if __name__ == "__main__" :
    asyncio.run(main())