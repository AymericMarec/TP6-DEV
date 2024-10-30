from sys import argv
import aiohttp
import aiofiles
import asyncio

async def get_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp = await resp.read()
            return resp

async def write_content(content, file):
    async with aiofiles.open(file, "w",encoding="utf-8") as file:
        await file.write(content)
        await file.flush()
        print("fichier html créer !")

async def main():
    try :
        weblink = argv[1]
    except :
        print("Faut donner le lien en argument hein")
        exit(0)
    content = await get_content(weblink)
    content = content.decode()
    print(content)
    await write_content(content,"ynov.html")

if __name__ == "__main__":
    asyncio.run(main())
