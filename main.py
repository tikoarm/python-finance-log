import asyncio  # Добавляем импорт модуля asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules', 'database'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules', 'telegram'))

from SqlCode import db, dbmanager
import settings
import tg_bot

async def main():
    await asyncio.gather(
        tg_bot.start()
    )

if __name__ == '__main__':
    try:
        print("Запуск бота прошел успешно.")
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("Bot stopped.")