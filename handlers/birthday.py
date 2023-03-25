from discord.ext import commands
from discord import Member, app_commands
from discord.ext.commands.context import Context
import datetime
from services import BirthdayService
import logging

logger = logging.getLogger(__name__)


class Birthdays(commands.Cog):

    def __init__(self, bot, service):
        self.bot = bot
        self.service = service

    async def cog_command_error(self, ctx: Context, error: commands.CommandError):
        if isinstance(error, (commands.BadArgument, commands.MissingRequiredArgument,
                              commands.CommandNotFound, commands.CommandInvokeError)):
            return await ctx.send('Кожаный, ты совсем дурачок?', ephemeral=True)
        else:
            logger.error(error)
            return await ctx.send('Молодец, ты мегамозг, ты все разъебал, вызывай главного', ephemeral=True)

    @staticmethod
    def _validate_date(date: str):
        if not date:
            return None
        try:
            date = datetime.datetime.strptime(date, '%d.%m')
        except ValueError:
            return None
        return date.strftime('%d.%m')

    @commands.hybrid_group(description='Команды связанные со списком дней рождения')
    async def birthday(self, ctx: Context):
        await ctx.send_help()

    @birthday.command(description='Добавление пользователя в список дней рождений')
    @app_commands.describe(
            raw_birth_date='Дата в формате дд.мм',
            user='Выберите пользователя которого хотите добавить')
    @app_commands.rename(
            raw_birth_date='дата',
            user='пользователь')
    async def add(self, ctx: Context, raw_birth_date: str, user: Member):
        response = 'Инвалидная дата, хватит ломать бота'
        birth_date = self._validate_date(raw_birth_date)
        if birth_date:
            response = self.service(user).add_user_birthday(birth_date)
        await ctx.send(response, ephemeral=True, delete_after=10)

    @birthday.command(description='Удаление пользователя из списка дней рождений')
    @app_commands.describe(
            user='Выберите пользователя которого хотите удалить')
    @app_commands.rename(user='пользователь')
    async def delete(self, ctx: Context, user: Member):
        response = self.service(user).delete_user_birthday()
        await ctx.send(response, ephemeral=True, delete_after=10)


async def setup(bot):
    b = Birthdays(bot, BirthdayService)
    await bot.add_cog(b)

