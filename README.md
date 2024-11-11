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

### 3. Config et arguments

Pour cette partie j'ai juste reprit un ancien code :

```python

def GetInfos():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", action="store")
    parser.add_argument("-l", "--listen", action="store")
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
    return port,host

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



# Et je lance le serveur dans mon main :

port,host = GetInfos()
server = await asyncio.start_server(handle_client_msg, host, port)
```

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

Apres avoir tapé : "/di shrek.jpg"


![](./Image/ShrekAscii.png)


### 6. Gestion d'historique

Tout d'abord , j'ai rajouté le chemin du dossier .json a mettre dans les arguments 

```python
parser.add_argument("-hp", "--path", action="store")
#   hp pour HistoricPath , -h et -p etant deja prit
#   et par defaut la valeur est ""  , le fichier sera donc créer la ou le serveur a été éxecuté
```

Pour avoir un historique , il va falloir deja ajouté des messages !

```python
#On lit le fichier main.json ( main car plus tard il y aura un systeme de salon avec a chacun son historique)
async def GetHistoric():
    global historicPath
    async with aiofiles.open(historicPath+"/main.json", "r",encoding="utf-8") as file:
        content = await file.read() #   On lit dans le fichier json
        try :   #   Si il y a du contenu
            data = json.loads(content)
        except :
            return None
    return data

async def AddHistoric(message):
    global historicPath
    Historic = await GetHistoric()
    if Historic == None:    #   Si il y a pas d'historique ( fichier vide )
        Historic = {}
        Historic["msg"] = []
    Historic["msg"].append(message)  
    async with aiofiles.open(historicPath+"/main.json", "w",encoding="utf-8") as file:
        await file.write(json.dumps(Historic))
        await file.flush()

#fonction appelé quand un user se connecte 
async def DisplayHistoric(writer):
    historic = await GetHistoric()
    if not historic : return
    if len(historic["msg"]) > 50:   #   Si il y a plus de 50 message dans le fichier json , on supprime ceux en trop
        await DeletHistoric()       #   pour pas créer un fichier gigantesque ou les 50 messages seront utiles sur 10000
        print("delete")
    for msg in historic["msg"][-50:]:
        writer.write((msg+"\n").encode())
        await writer.drain()

async def DeletHistoric():
    global historicPath
    Historic = await GetHistoric()
    Historic["msg"] = Historic["msg"][-20:] 
    print(Historic)
    async with aiofiles.open(historicPath+"/main.json", "w",encoding="utf-8") as file:
        await file.write(json.dumps(Historic))
        await file.flush()


# j'ai juste appelé la fonction DisplayHistoric quand la personne se connecte 
# et j'ai rajouté cette ligne pour a chaque envoie de message :
await AddHistoric(message)
```

### 7. Plusieurs rooms

J'ai ajouté une commande a l'utilisateur /room \[numero de room\]
Par defaut , ils seront dans la room 1


- Coté client :

```python
    #   J'ai rajouté ceci a mon switch pour essayer de connaitre la commande 
    
        case "room":
            try:
                NbRoom = input[1:].split(" ")[1]    #   Je recupere donc le numero de la room
            except:
                print("Pas de numéro de room donné")
                return None,None
            try:
                NbRoom = int(NbRoom)
            except:
                print("La room donné n'est pas un nombre !")
                return None,None
            if(NbRoom > 999999):
                print("Numéro de room trop grand")
                return None,None
            return "room",NbRoom    #   Si il a passé tout les tests , on passe a la suite

    if(input[0] == "/"):
        type,result = Command(input)
        if type == None : continue
        if(type=="Image"):
            image = result.to_terminal()
            await SendMessage(image,writer)
        elif(type=="room"):     #   Si la commande est un changement de room
            LenNb = CalculTailleOctet(result)
            writer.write((3).to_bytes())    #   On envoie avec un header numero 3
            writer.write((LenNb).to_bytes(2))   #   La taille en octet du numero de room
            writer.write(result.to_bytes(LenNb))    #   Et on envoie le numero de room
            await writer.drain()
            print("--------------------------------\n")
            print(f"          Room n°{result}")
            print("\n--------------------------------")
        continue
```

- Coté serveur :
  
Pour gérer les room , j'ai préféré juste rajouter un parametre a chaque client , j'ai trouvé ca plus simple a gérer et a parcourir


```python
    #On ajoute la section room
    if not addr in CLIENTS :
        CLIENTS[addr] = {}
        CLIENTS[addr]["r"] = reader
        CLIENTS[addr]["w"] = writer
        CLIENTS[addr]["pseudo"] = ""
        CLIENTS[addr]["color"] = GenerateColor()
        CLIENTS[addr]["room"] = 1   #   Par defaut a 1



    #   Quand je recois mon numero de header , j'ajoute cette partie : 
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

#   Et on modifie juste la fonction pour envoyer le message pour envoyer a la bonne room !
async def SendBroadCastMessage(who,message,room):
    message+= '\033[0m'
    for client in CLIENTS :
        if(CLIENTS[client]["room"] == room):
            CLIENTS[client]["w"].write(message.encode())
            await CLIENTS[client]["w"].drain()

```

### 8. NTUI ( oui c'est moi qui ai créer cette partie)

Je vais essayer de régler le plus de probleme par rapport aux users inputs 

```python
#   Cette fonction va juste print dans la console serveur qu'il a détécté un clien bizzare , et cela envoie un message au vilain hackerz
async def DeleteHacker(addr,writer):
    print(f"Client suspect : {addr[0]} : {addr[1]} ")
    writer.write(("C'est pas bien de tricher , modifie pas le code , c'est pas bien").encode())  #   on lui empeche l'acces avec un message
    await writer.drain()
```

J'ai modifié quelque partie de code pour en ajoutant  cette fonction , et si message bizzare est recu , alors on l'appelle  
J'ai très surement oublié de régler pleins de probleme , mais le serveur est deja un "minimum" sécurisé face aux inputs en modifiant le code client 


## Voila le resultat final :

- fichier serveur : [serveur](./Bonus/server/chat_server_ii_6.py)

- fichier client : [client](./Bonus/chat_client_ii_6.py)