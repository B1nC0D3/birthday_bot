from discord import Intents
from discord.ext import commands, tasks
from services import add_user_birthday, create_msg_for_birthday_boys, get_paste
from datetime import timezone, time
from config import HOUR, MIN, CHANNEL_TO_POST, TOKEN
from discord.ext.commands.context import Context

intents = Intents.default()
intents.message_content = True
utc = timezone.utc
time = time(hour=HOUR, minute=MIN, tzinfo=utc)
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.listen()
async def on_ready():
    check_date.start()


@bot.command()
async def add(ctx: Context, date=None, user=None):
    await ctx.message.delete()
    response = await add_user_birthday(ctx, date, user)
    await ctx.send(response)


@bot.command()
async def test(ctx: Context):
    await ctx.message.delete()
    # my discord id
    if ctx.message.author.id != 237542033697406986:
        return
    for msg in create_msg_for_birthday_boys():
        await ctx.send(msg)


@bot.command()
async def pain(ctx, user=None):
    await ctx.message.delete()
    response = await get_paste(ctx, user)
    await ctx.send(response)


@tasks.loop(time=time)
async def check_date():
    channel = bot.get_channel(CHANNEL_TO_POST)
    for msg in create_msg_for_birthday_boys():
        await channel.send(msg)


bot.run(TOKEN)
