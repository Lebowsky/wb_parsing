from aiogram import types


async def config(message: types.Message):
    await message.answer(message.text)
