import logging
import os
import asyncio
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
import httpx

load_dotenv()

API_TOKEN = os.getenv('BOT')
FASTAPI_URL = os.getenv('URL')

# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class Token(StatesGroup):
    token = State()


@dp.message(Command('start'))
async def start_handler(message: types.Message):
    await message.answer("Привет! Используйте /register для регистрации.")


@dp.message(Command('register'))
async def register_handler(message: types.Message):
    username = message.from_user.username
    user_data = {
        "username": username,
        "email": f"{username}@example.com",
        "password": "qwerty",  # FIX: Нужно использовать механизм для получения пароля от пользователя
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{FASTAPI_URL}/api/v1/register", json=user_data)

    if response.status_code == 200:
        await message.answer("Вы успешно зарегистрированы!")
    else:
        await message.answer("Ошибка при регистрации.")


@dp.message(Command('login'))
async def login_handler(message: types.Message, state: FSMContext):
    username = message.from_user.username
    password = "qwerty"  # FIX: Нужно использовать механизм для получения пароля от пользователя

    login_data = {
        "username": username,
        "password": password,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{FASTAPI_URL}/api/v1/token", data=login_data)

    if response.status_code == 200:
        token = response.json().get("access_token")
        await state.update_data(token=token)
        await message.answer("Вы успешно вошли в систему!")
    else:
        await message.answer("Ошибка при входе. Неверный логин или пароль.")


@dp.message(Command('notes'))
async def notes_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    token = data.get('token')  # Получаем токен, сохраненный ранее

    if not token:
        await message.answer("Вы не авторизованы. Пожалуйста, используйте /login для входа.")
        return

    headers = {
        "Authorization": f"Bearer {token}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{FASTAPI_URL}/api/v1/notes/", headers=headers)

    if response.status_code == 200:
        notes = response.json()
        notes_text = "\n".join([f"{note['title']}: {note['content']}" for note in notes])
        await message.answer(f"Ваши заметки:\n{notes_text}")
    else:
        await message.answer("Ошибка при получении заметок.")


@dp.message(Command('create_note'))
async def create_note_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    token = data.get('token')  # Получаем токен, сохраненный ранее

    if not token:
        await message.answer("Вы не авторизованы. Пожалуйста, используйте /login для входа.")
        return

    await message.answer("Введите название заметки:")
    await state.set_state("awaiting_note_title")


@dp.message(StateFilter("awaiting_note_title"))
async def get_note_title(note_message: types.Message, state: FSMContext):
    note_title = note_message.text
    data = await state.get_data()
    token = data.get('token')

    note_data = {
        "title": note_title,
        "content": "Здесь будет содержимое заметки",  # Можно также запросить содержимое
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{FASTAPI_URL}/api/v1/notes/", json=note_data, headers=headers)

    if response.status_code == 200:
        await note_message.answer("Заметка успешно создана!")
    else:
        await note_message.answer("Ошибка при создании заметки.")

    await state.clear()  # Сбрасываем состояние после создания заметки


async def main():
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
