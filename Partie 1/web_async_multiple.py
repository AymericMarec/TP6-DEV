from sys import argv
import aiofiles
import aiohttp
import asyncio
from datetime import datetime
startTime = datetime.now()

#fonction qui recupere le contenu html de la page
async def get_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp = await resp.read()
            return resp
#fonction qui créer un fichier html et met le contenu dedans
async def write_content(content, file):
    async with aiofiles.open(file, "w",encoding="utf-8") as file:
        await file.write(content)
        await file.flush()
        print("fichier html créer !")
#fonction qui lit toutes les urls du fichier donné en argument
async def read_url(file):
    global List_url_glob
    async with aiofiles.open(file, "r",encoding="utf-8") as file:
        async for url in file:
            List_url_glob.append(url)
        print(List_url_glob)
#fonction qui lit la lecture de contenu et l'ecriture
#il faudra donc appelé cette fonction pour chaque page lu dans le fichier
async def Process(url,index):
    content = await get_content(url)
    content = content.decode()
    await write_content(content,str(index)+".html")  

async def main():
    try :
        file = argv[1]
    except :
        print("Faut donner le nom du fichier en argument hein")
        exit(0)
    await read_url(file)
    index = 0
    global List_url_glob
    tasks = []
    for url in List_url_glob:
        index+=1
        tasks .append(Process(url,index)) # on ajoute la tache process qui lit et ecrit le contenu html 
    await asyncio.gather(*tasks) # on execute nos n fonctions qui ecrivent le fichier html


List_url_glob = []

if __name__ == "__main__":
    asyncio.run(main())
    print(datetime.now() - startTime)