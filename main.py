from discord import Intents
from discord.ext import commands, tasks
from config import TOKEN, EXTENSIONS
from asyncio import run
from services import BirthdayService
from config import CHANNEL_TO_POST
from utils.time_utils import get_task_start_time, get_today_date


intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, owner_id=237542033697406986)


@tasks.loop(time=get_task_start_time())
async def check_date():
    channel = bot.get_channel(CHANNEL_TO_POST)
    for msg in BirthdayService('asd').create_msg_for_birthday_boys(get_today_date()):
        await channel.send(msg)


@bot.listen()
async def on_ready():
    check_date.start()


async def main():
    for extension in EXTENSIONS:
        await bot.load_extension(extension)


if __name__ == '__main__':
    run(main())
    bot.run(TOKEN)
