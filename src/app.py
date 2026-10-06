from __future__ import annotations

import asyncio
import logging
import sys


from src.bot.connect import bot, dp
from src.bot.handlers import router as outfit_router


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )

    dp.include_router(outfit_router)

    await bot.delete_webhook(drop_pending_updates=True)

    logging.info("Starting bot polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot execution stopped.")