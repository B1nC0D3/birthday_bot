from discord import Intents, app_commands, Member
from discord.ext import commands, tasks
from services import add_user_birthday, create_msg_for_birthday_boys, get_paste
from datetime import timezone, time
from config import HOUR, MIN, CHANNEL_TO_POST, TOKEN
from discord.ext.commands.context import Context
from discord.ext.commands.errors import NotOwner
from utils.date_utils import validate_date

intents = Intents.default()
intents.message_content = True
utc = timezone.utc
time = time(hour=HOUR, minute=MIN, tzinfo=utc)
bot = commands.Bot(command_prefix='/', intents=intents, owner_id=237542033697406986)


@bot.listen()
async def on_ready():
    check_date.start()


@bot.listen()
async def on_command_error(ctx: Context, error):
    msg = f'Технические шоколадки, пиши <@237542033697406986> ошибка {error}'
    if isinstance(error, NotOwner):
        msg = 'Не лезь куда не надо, дам по жопе'
    await ctx.send(msg, ephemeral=True)


@bot.hybrid_command(name='add', description='Добавление пользователя в список дней рождений')
@app_commands.describe(
        birth_date='Дата в формате дд.мм',
        user='Выберите пользователя которого хотите добавить')
async def add(ctx: Context, birth_date: validate_date, user: Member):
    response = 'Инвалидная дата, хватит ломать бота'
    if birth_date:
        response = await add_user_birthday(birth_date, user)
    await ctx.send(response, ephemeral=True)


@bot.command(hidden=True)
@commands.is_owner()
async def test(ctx: Context):
    for msg in create_msg_for_birthday_boys():
        await ctx.send(msg, ephemeral=True)


@bot.command(hidden=True)
@commands.is_owner()
async def sync(ctx: Context):
    await bot.tree.sync()
    await ctx.send('Done!', ephemeral=True)


@bot.hybrid_command(name='pain', description='Для попускания клоунов')
@app_commands.describe(
        user='Выберите юзера с клоунской манерой речи')
async def pain(ctx, user: Member):
    response = await get_paste(user)
    await ctx.send(response)


@bot.hybrid_command(name='gay', desctiprion='Отпустить гейскую шуточку')
@app_commands.describe(user='Выберите юзера со странными наклонностями')
async def gay(ctx, user: Member):
    msg = f'Одним прекрасным вечером плавают два гея: <@{user.id}> и <@406759059866255370>, в дорогущем бассейне, ' \
          f'решили устроить себе романтик - свечи все дела. <@{user.id}> смотрит - сперма плавает ' \
          'на поверхности и спрашивает у <@406759059866255370>: "Дорогой, ты кончил?", а тот ему отвечает: "Нет, пернул". \n' \
          'P.S. Зефир не заготовил контента.'
    await ctx.send(msg)

@tasks.loop(time=time)
async def check_date():
    channel = bot.get_channel(CHANNEL_TO_POST)
    for msg in create_msg_for_birthday_boys():
        await channel.send(msg)

bot.run(TOKEN)
