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
CHANNEL_TO_POST = int(os.getenv('CHANNEL_ID'))

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
    response = add_date_to_json(date, user)
    await ctx.send(response)


@tasks.loop(time=time)
async def check_date():
    channel = bot.get_channel(CHANNEL_TO_POST)
    birthday_boys = check_today_birthdays()
    if not birthday_boys:
        return
    for birthday_boy in birthday_boys:
        msg = 'Друзья, а вы знаете, что сегодня особенный день? ' \
              f'Ведь именно сегодня на свет появился/лась чудесный/я, удивительный/я и неповторимый/я - {birthday_boy}. ' \
              'Так давайте же дружно поздравим его/её и пожелаем всего самого лучшего! ' \
              f'С праздником, {birthday_boy}, спасибо, что ты есть!'
        await channel.send(msg)

bot.run(TOKEN)
