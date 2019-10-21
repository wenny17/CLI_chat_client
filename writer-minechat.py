import asyncio
import argparse
import logging
import json
import os
from dotenv import load_dotenv


async def write_and_logg(writer, message):
    writer.write(message.encode() + b'\n')
    logging.debug("SEND: {}".format(message))
    await writer.drain()


async def read_and_log(reader):
    message = (await reader.readline()).decode('utf-8')
    logging.debug("RECEIVE: {}".format(message))
    return message


async def register(host, port, login):
    try:
        reader, writer = await asyncio.open_connection(host, port)

        entry_message = await read_and_log(reader)
        await write_and_logg(writer, '')
        message = await read_and_log(reader)
        await write_and_logg(writer, login)
        user_data = await read_and_log(reader)
    finally:
        writer.close()

    return json.loads(user_data)


async def authorise(reader, writer, token):
    entry_message = await read_and_log(reader)
    await write_and_logg(writer, token)
    message = await read_and_log(reader)

    auth_response = json.loads(message)
    if not auth_response:
        return False

    message = await read_and_log(reader)
    return True


async def submit_message(reader, writer, message):
    message = ' '.join(message).replace('\n', ' ') + '\n'
    await write_and_logg(writer, message)
    message = await read_and_log(reader)


async def client_sender(token, login, message, host, port):
    if token is None:
        user_data = await register(host, port, login)
        token = user_data["account_hash"]

    try:
        reader, writer = await asyncio.open_connection(host, port)
        is_authorise = await authorise(reader, writer, token)
        if not is_authorise:
            exit("Unsuccessful Authorization. Invalid token")
        await submit_message(reader, writer, message)
    finally:
        writer.close()


def get_arguments():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("-token")
    parser.add_argument("-message", type=str, nargs="*")
    parser.add_argument("-host", default=os.getenv('HOST'))
    parser.add_argument("-port", type=int, default=os.getenv('PORT_WRITE'))
    parser.add_argument("-login")
    return parser.parse_args()


def main():
    args = get_arguments()

    if not args.login and not args.token:
        exit("Enter your token or preffered nickname to registration")

    logging.basicConfig(level = logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client_sender(
                                          token=args.token,
                                          login=args.login,
                                          message=args.message,
                                          host=args.host,
                                          port=args.port))
    loop.close()


if __name__ == '__main__':
    main()
