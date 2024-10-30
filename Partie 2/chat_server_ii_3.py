import asyncio

async def handle_client_msg(reader,writer) :
    while True:
        data = await reader.read(1024)
        addr = writer.get_extra_info('peername')
        if not data :break
        message = data.decode()
        print(f"Message received from {addr[0]}:{addr[1]} : {message}")
        writer.write(f"Hello {addr!r}".encode())
        await writer.drain()


async def main():
    server = await asyncio.start_server(handle_client_msg, '10.33.49.118', 13337)
    async with server:
        await server.serve_forever()


if __name__ == "__main__" :
    asyncio.run(main())