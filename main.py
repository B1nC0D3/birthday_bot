from discord import Intents
from discord.ext import commands
from config import TOKEN, EXTENSIONS

from asyncio import run

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, owner_id=237542033697406986)


async def main():
    for extension in EXTENSIONS:
        await bot.load_extension(extension)


if __name__ == '__main__':
    run(main())
    bot.run(TOKEN)
