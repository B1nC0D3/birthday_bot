import discord
from discord.ext import commands, tasks
from date_saver import add_date_to_json, check_today_birthdays
from datetime import timezone, time
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
HOUR = int(os.getenv('HOURS'))
MIN = int(os.getenv('MINS'))
intents = discord.Intents.default()
intents.message_content = True
utc = timezone.utc
time = time(hour=HOUR, minute=MIN, tzinfo=utc)
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.listen()
async def on_ready():
    check_date.start()


@bot.command()
async def add(ctx, date, user):
    print(date, user)
    response = add_date_to_json(date, user)
    await ctx.send(response)
    await ctx.send(ctx.channel.id)


@tasks.loop(time=time)
async def check_date():
    channel = bot.get_channel(1084154236427845792)
    birthday_people = check_today_birthdays()
    if not birthday_people:
        return
    birthday_people_str = ', '.join(birthday_people)
    await channel.send(
        f'Сегодня день рождения у {birthday_people_str}'
    )

bot.run(TOKEN)
