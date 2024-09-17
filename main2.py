# This is a sample Python script.
import json
import statistics
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from argparse import ArgumentParser
import telethon
from aiogram.fsm.state import StatesGroup, State
from telethon.events import NewMessage
import handlers
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

parser = ArgumentParser()
parser.add_argument("--id", help="Your API ID")
parser.add_argument("--hash", help="Your API hash")
parser.add_argument("--phone", help="Phone number")
parser.add_argument("--token", help="Your bot token")
args = parser.parse_args()
phone_number = args.phone


client = telethon.TelegramClient("client", api_id=args.id,
                      api_hash=args.hash,
                      system_version="4.16.30-vxCUSTOM",
                      device_model="Windows 11",
                      app_version='4.10.2 x64',
                      lang_code='ru',
                      system_lang_code='ru-RU')
client.start(phone=phone_number)


class UploadPhotoState(StatesGroup):
    upload_command_entered = State()


@client.on(NewMessage(chats="outlinesucks"))
async def new_channel_message_handler(event: NewMessage.Event):
    total_sum, accept = await handlers.calculate_weights_handler(event)
    logging.info(f"Weight sum: {total_sum}, is accepted: {bool(accept)}")
    if accept:
        await client.send_message("TelePortEchoBot", "/trigger")


if __name__ == '__main__':
    asyncio.gather(
        client.run_until_disconnected()
    )





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
