from __future__ import annotations

import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from src.weather import get_today_weather
from src.ai.service import generate_outfit_recommendation

logger = logging.getLogger(__name__)

router = Router()

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👕 Get Outfit Suggestion")]
    ],
    resize_keyboard=True,
    persistent=True
)


@router.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    greeting = (
        "**Вітаю до Помічника з підбору одягу!**\n\n"
        "*Будь ласка зауважте:* Цей бот працює та надає рекомендації спеціально для мешканців **Вінниці**.\n\n"
        "**Доступні команди:**\n"
        "• `/outfit` - отримати рекомендації щодо вбрання від ШІ з урахуванням погоди\n"
        "• `/start` - показати це повідомлення\n\n"
        "Натисність кнопку нижче або введіть `/outfit` щоб почати роботу!"
    )
    await message.answer(greeting, reply_markup=MAIN_KEYBOARD)


@router.message(Command("outfit"))
@router.message(lambda msg: msg.text == "👕 Get Outfit Suggestion")
async def cmd_outfit(message: types.Message) -> None:
    await message.answer("Перевіряємо погоду Вінниці та підбираємо образ...")
    
    try:
        weather = await get_today_weather(lat=49.2331, lon=28.4682)
        
        outfit_advice = await generate_outfit_recommendation(weather=weather)
        await message.answer(outfit_advice, reply_markup=MAIN_KEYBOARD)
        
    except Exception as err:
        logger.error(f"Не вдалося згенерувати образ: {err}")
        await message.answer(
            "Вибачте, нажаль не вдалося отримати інформацію про погод або згенерувати рекомендації щодо образу.",
            reply_markup=MAIN_KEYBOARD
        )