# TP6 DEV : Chat room

## I. Faire joujou avec l'asynchrone


## 1. Premiers pas

- fonction sleep_and_print synchrone : [sleep_and_print](./Partie%201/sleep_and_print.py)

- fonction sleep_and_print asynchrone : [sleep_and_print](./Partie%201/sleep_and_print_async.py)

## 2. Web Requests

- fonction web_sync synchrone : [web_sync](./Partie%201/web_sync.py)

- fonction web_sync asynchrone : [web_async](./Partie%201/web_async.py)

- fonction web_sync multiple synchrone : [web_sync_multiple](./Partie%201/web_sync_multiple.py)

- fonction web_sync multiple asynchrone : [web_async_multiple](./Partie%201/web_async_multiple.py)

### 🌞 Mesure !

Temps de requete synchrone :

--- 3.081620216369629 seconds ---

Temps de requete asynchrone :

--- 1.3472027778625488 seconds ---

## II. Chat room

### 2. Première version

Mini ChatRoom Synchrone

- Coté serveur : [serveur](./Partie%202/chat_server_ii_2.py)

- Coté client : [client](./Partie%202/chat_client_ii_2.py)

### 3. Client asynchrone

Mini ChatRoom Asynchrone

- Coté serveur : [serveur](./Partie%202/chat_server_ii_3.py)

- Coté client : [client](./Partie%202/chat_client_ii_3.py)

### 4. Un chat fonctionnel

Chat entre différents users :

- Coté serveur : [serveur](./Partie%202/chat_server_ii_4.py)

### 5. Gérer des pseudos


- Coté serveur : [serveur](./Partie%202/chat_server_ii_5.py)

- Coté client : [client](./Partie%202/chat_client_ii_5.py)

### 6. Déconnexion


- Coté serveur : [serveur](./Partie%202/chat_server_ii_6.py)

- Coté client : [client](./Partie%202/chat_client_ii_6.py)

## Bonus :

Pour les bonus je vais juste montrer les parties de code rajoutés / modifiés , pour que ce soit un minimum lisible

### 1. Basic Cosmetic

J'ai juste ajouté les couleurs , le "vous avez dit" est simple a faire et met en doublon le message ce qui est moins beau a mon gout , donc j'ai juste fait les couleurs et le time stamp

- Couleurs :

```python
#Ceci retourne une couleur a print dans le terminal
def GenerateColor():
    Colors = ['\033[31m','\033[32m','\033[33m','\033[34m','\033[35m','\033[36m','\033[37m','\033[90m','\033[91m','\033[92m','\033[93m','\033[94m','\033[95m','\033[96m']
    rand = random.randint(0, len(Colors)-1)
    return Colors[rand]



#je l'ajoute donc au dictionnaire
CLIENTS[addr] = {}
CLIENTS[addr]["r"] = reader
CLIENTS[addr]["w"] = writer
CLIENTS[addr]["pseudo"] = ""
CLIENTS[addr]["color"] = GenerateColor()



# a l'envoie du message , je rajoute la couleur
message = f"{color}[{pseudo}] : {data.decode()}"


# et dans la fonction pour envoyer le message , je rajoute a la fin un couleur qui remet la couleur de base 
message+= '\033[0m'
# (sinon ca bloque le terminal en rouge violet ou bleu quoi , c'est drole mais 2m)
```

- Time :

```python
#On rajoute une fonction qui renvoie la date actuel
def GetTime():
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
    return date


#on envoie le message en rajoutant la date
message = f"{color}{GetTime()} [{pseudo}] : {data.decode()}"

```

## Voila le resultat :

![](./Image/ScreenColor.png) 

### 4. Encodage maison

Le protocole proposé etais plutot cool , donc je l'ai reppris

- Coté client :

```python
#la fonction est vraiment pas belle , mais elle retourne la taille en octet d'un nombre 
def CalculTailleOctet(Nb):
    bit = 0
    while True:
        bit+=1
        if Nb < 2**bit :
            if(bit%8==0):
                return int(bit/8)
            else: 
                return int((bit/8)+1)



#apres avoir empecher une taille de pseudo trop grande je l'envoie au serveur
pseudo = input("Choisir votre pseudo :\n\n")
if(len(pseudo)>15):
    print("pseudo trop long")
    return
reader, writer = await asyncio.open_connection(host="192.168.1.21", port=13337)
writer.write(len(pseudo).to_bytes())
writer.write(pseudo.encode())
await writer.drain()



#j'ai aussi une fonction que j'appelle pour envoyer un message
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
```

- Coté serveur :

```python
# si la personne n'est pas connecté , je lit la taille du pseudo qui ne depassera donc jamais 1 octet
# ensuite on lit juste le pseudo
# cela respecte pas trop le NTUI , mais je changerais ca plus tard
if pseudo == "":
    LenPseudo = await reader.read(1)
    print(int.from_bytes(LenPseudo))
    pseudo = (await reader.read(int.from_bytes(LenPseudo))).decode()
    print(pseudo)
    CLIENTS[addr]["pseudo"] = pseudo
    message = "Annonce : " + pseudo + " a rejoint la chatroom"
    await SendBroadCastMessage(addr,message)
    continue

#sinon , je lit le message normalement 
header1 = await reader.read(1)#   on recupere le type de message
if(int.from_bytes(header1) == 1):   #   si le message est court
    LenMess = await reader.read(1)
    data = await reader.read(int.from_bytes(LenMess))
elif int.from_bytes(header1) == 2:  #   si le message est long 
    LenLen = await reader.read(1)
    LenMess = await reader.read(int.from_bytes(LenLen))
    data = await reader.read(int.from_bytes(LenMess))

#je stock le message dans data , que j'envoie comme avant
```

### 5. Envoi d'image

Pour l'envoie d'image , j'ai pensé a un systeme de commande , qui sera surement utile pour plus de fonctionnalité , tel le changement de salon pour la Partie 7

```python
#Cette fonction est celle qui recupere l'input de l'utilisateur
async def SendInput(writer):
    while True:
        input = await aioconsole.ainput()
        try:
            if(input[0] == "/"):    #   Si le premier caractere est un "/"
                type,result = Command(input)    #   Command renvoie le type de la commande , et le contenu
                if type == None : continue #    Elle renvoie None si il y a une erreur
                if(type=="Image"):  #   Si l'utilisateur a donné une image valide
                    image = result.to_terminal()    #   Alors on l'envoie
                    await SendMessage(image,writer)
                continue
        except:
            continue
        await SendMessage(input,writer)


def Command(input):
    command = input[1:].split(" ")[0]   #   On prend la commande 
    match command :
        case "di":  #   di etant la commande pour afficher une image (Display Image)
            try:
                ImagePath = input[1:].split(" ")[1]
            except:
                print("Pas d'image donné")
                return None,None
            try:
                my_art = AsciiArt.from_image(ImagePath)
                return "Image",my_art   #   Si tout est valide , on renvoie l'image
            except:
                print("Mauvais chemin")
                return None,None
        case _:
            print("Commande inconnu")
            return None,None
```
# Voila un exemple d'image :

![](./Image/ShrekAscii.png)