from discord import Intents
from discord.ext import commands, tasks
from services import add_user_birthday, create_msg_for_birthday_boys
from utils import get_exception_message
from datetime import timezone, time
from config import HOUR, MIN, CHANNEL_TO_POST, TOKEN

intents = Intents.default()
intents.message_content = True
utc = timezone.utc
time = time(hour=HOUR, minute=MIN, tzinfo=utc)
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.listen()
async def on_ready():
    check_date.start()


@bot.command()
async def add(ctx, date=None, user=None):
    response = get_exception_message(ctx.message.author.id)
    if date and user:
        response = await add_user_birthday(ctx, date, user)
    await ctx.send(response)


@bot.command()
async def test(ctx):
    for msg in create_msg_for_birthday_boys():
        await ctx.send(msg)


@tasks.loop(time=time)
async def check_date():
    channel = bot.get_channel(CHANNEL_TO_POST)
    for msg in create_msg_for_birthday_boys():
        await channel.send(msg)


bot.run(TOKEN)
