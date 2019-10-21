import asyncio
import datetime
import aiofiles
import argparse
import os
from dotenv import load_dotenv

async def write_to_file(data):
    async with aiofiles.open("chathistory.txt", 'a') as f:
        now = datetime.datetime.now()
        time = now.strftime("%d.%m.%Y %H:%M")
        message = "[{}] ".format(time) + data
        await f.write(message)


async def client_reader():
    connection_attempt = 0
    opened_connection = False
    while True:
        if not opened_connection:
            reader, writer = await asyncio.open_connection("minechat.dvmn.org", 5000)
            opened_connection = True
            await write_to_file("Установлено соединение\n")

        try:
            while True:
                data = await asyncio.wait_for(reader.readline(), timeout=3)
                if connection_attempt > 0:
                    await write_to_file("Установлено соединение\n")
                    connection_attempt = 0

                if not data:
                    break
                await write_to_file(data.decode("utf-8"))

        except (asyncio.TimeoutError,
                ConnectionRefusedError,
                ConnectionResetError):

            connection_attempt += 1
            if connection_attempt <= 2:
                await write_to_file("Нет соединения. Повторная попытка.\n")
            else:
                await write_to_file("Нет соединения. Повторная попытка через 3 сек.\n")
                await asyncio.sleep(3)
            continue

        writer.close()
        write_to_file("End connection")
        await writer.wait_closed()

def get_arguments():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("-host", default=os.getenv('HOST'))
    parser.add_argument("-port", type=int, default=5000)
    parser.add_argument("-history", default=os.getenv('PORT_READ'))
    return parser.parse_args()



def main():
    args = get_arguments()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client_reader())
    loop.close()




if __name__ == '__main__':
    main()
