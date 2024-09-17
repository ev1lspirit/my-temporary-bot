import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command, StateFilter, BaseFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from argparse import ArgumentParser
import json
import logging
import os

logging.basicConfig(level=logging.INFO)

json_file = os.path.join(os.getcwd(), 'profile.json')
parser = ArgumentParser()
parser.add_argument("--token")
args = parser.parse_args()

bot = Bot(args.token)
dispatcher = Dispatcher()
router = Router(name='dp')
dispatcher.include_router(router)

text = \
'''Даня, 21
Живу и учусь в Петербурге. Люблю этот город, а в особенности его окресности)\n
В своих путешествиях исследовал руины Карфагена, 
покорил горы Дагестана, кормил зубра в Беловежской пуще и
восхитился германской готикой Калининграда.
Посетил 4 страны и 10 регионов России.
Буду очень рад знакомству :)
'''


class OnlyMeFilter(BaseFilter):

    async def __call__(self, message: Message):
        if hasattr(message.from_user, "username"):
            return message.from_user.username == "sweeetferrero"
        return False


router.message.filter(OnlyMeFilter())

class UploadPhotoState(StatesGroup):
    upload_command_entered = State()

def get_from_json(filename, key: str):
    with open(filename, 'r+') as f:
        data = json.load(f)
        return data[key]

def update_json(filename, **kwargs):
    with open(filename, 'r+') as f:
        data = json.load(f)
        data.update(kwargs)
        f.seek(0)
        json.dump(data, f, indent=4)


@router.message(Command("start"), StateFilter(None))
async def start_message_handler(message: Message):
    await message.reply("Добро пожаловать. Этот бот используется для информирования ")


@router.message(Command("current"), StateFilter(None))
async def get_current_picture(message: Message):
    picture_id = get_from_json(json_file, "avatar_id")
    if picture_id:
        await message.reply_photo(picture_id)
    else:
        await message.reply("No photo saved! Load it first with the /avatar command.")


@router.message(Command("trigger"))
async def trigger_handler(message: Message):
    await message.reply(f"The new post is available in {'outlinesucks'} channel. Check it out.")
    photo_id = get_from_json(json_file, "avatar_id")
    if photo_id != 0:
        await message.answer_photo(photo_id)
    await message.answer(text)


@router.message(Command("avatar"), StateFilter(None))
async def send_avatar_handler(message: Message, state: FSMContext):
    await message.reply("Пришлите мне фото")
    await state.set_state(UploadPhotoState.upload_command_entered)


@router.message(UploadPhotoState.upload_command_entered,
                F.photo)
async def handle_photo(message, state):
    photo = message.photo[-1]
    file_id = photo.file_id
    update_json(json_file, avatar_id=file_id)
    await message.reply("Got it, the avatar has been updated.")
    await state.clear()


@router.message(UploadPhotoState.upload_command_entered, F.text == "Go Back")
async def going_back(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("The action is cancelled!", reply_markup=ReplyKeyboardRemove())


@router.message(UploadPhotoState.upload_command_entered)
async def no_photo_specified_handler(message):
    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Go Back")]],
                                 resize_keyboard=True,
                                 input_field_placeholder="Пришлите новй аватар")
    await message.reply("Send us the new avatar or simply press \"Go Back\"", reply_markup=markup)



if __name__ == "__main__":
    asyncio.run(dispatcher.start_polling(bot))