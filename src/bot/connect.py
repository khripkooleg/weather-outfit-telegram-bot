from __future__ import annotations

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

import logging
from typing import Optional

from src.config import config
from src.ai.connect import close_genai_client

logger = logging.getLogger(__name__)

_bot: Optional[Bot] = None
_dp: Optional[Dispatcher] = None

def get_bot() -> Bot:
    global _bot
    if _bot is None:
        token = config.bot.token.get_secret_value()
        _bot = Bot(
            token=token,
            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
        )
    return _bot

def get_dispatcher() -> Dispatcher:
    global _dp
    if _dp is None:
        _dp = Dispatcher()

        @_dp.shutdown()
        async def _on_shutdown(bot: Bot) -> None:
            logger.info("Closing Telegram Bot session...")
            await bot.session.close()
            logger.info("Closing Gemini AI Client...")
            await close_genai_client()
    return _dp

bot = get_bot()
dp = get_dispatcher()