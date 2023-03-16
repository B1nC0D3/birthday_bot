from discord import Intents, app_commands, Member
from discord.ext import commands, tasks
from services import add_user_birthday, create_msg_for_birthday_boys, get_paste
from datetime import timezone, time
from config import HOUR, MIN, CHANNEL_TO_POST, TOKEN
from discord.ext.commands.context import Context
from utils.date_utils import validate_date

intents = Intents.default()
intents.message_content = True
utc = timezone.utc
time = time(hour=HOUR, minute=MIN, tzinfo=utc)
bot = commands.Bot(command_prefix='/', intents=intents, owner_id=237542033697406986)


@bot.listen()
async def on_ready():
    check_date.start()


@bot.hybrid_command(name='add', description='Добавление пользователя в список дней рождений')
@app_commands.describe(
        birth_date='Дата в формате дд.мм',
        user='Выберите пользователя которого хотите добавить')
async def add(ctx: Context, birth_date: validate_date, user: Member):
    response = 'Инвалидная дата, хватит ломать бота'
    if birth_date:
        response = await add_user_birthday(birth_date, user)
    await ctx.send(response, ephemeral=True)


@bot.hybrid_command(hidden=True)
@commands.is_owner()
async def test(ctx: Context):
    for msg in create_msg_for_birthday_boys():
        await ctx.send(msg, ephemeral=True)


@bot.hybrid_command(hidden=True)
@commands.is_owner()
async def sync(ctx: Context):
    await bot.tree.sync()
    await ctx.send('Done!', ephemeral=True)


@bot.hybrid_command(name='pain', description='Для попускания клоунов')
@app_commands.describe(
        user='Выберите юзера с клоунской манерой речи')
async def pain(ctx, user: Member):
    await ctx.message.delete()
    response = await get_paste(user)
    await ctx.send(response)


@tasks.loop(time=time)
async def check_date():
    channel = bot.get_channel(CHANNEL_TO_POST)
    for msg in create_msg_for_birthday_boys():
        await channel.send(msg)

bot.run(TOKEN)
