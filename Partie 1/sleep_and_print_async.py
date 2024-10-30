import asyncio
import time

async def p1():
    for i in range(5):
        print(i)
        await asyncio.sleep(1)

async def p2():
    for i in range(5):
        print(i + 10)
        await asyncio.sleep(1)

async def main():
    tasks = [ p1(), p2() ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
