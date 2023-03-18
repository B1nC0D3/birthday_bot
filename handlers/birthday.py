from discord.ext import commands, tasks
from discord import Member, app_commands
from discord.ext.commands.context import Context
import datetime
from config import HOUR, MIN, CHANNEL_TO_POST
from services import BirthdayService
import logging

logger = logging.getLogger(__name__)


class Birthdays(commands.Cog):

    def __init__(self, bot, service):
        self.bot = bot
        self.service = service

    # async def cog_command_error(self, ctx: Context, error: commands.CommandError):
    #     if isinstance(error, (commands.BadArgument, commands.MissingRequiredArgument, commands.CommandNotFound)):
    #         return await ctx.send('Кожаный, ты совсем дурачок?', ephemeral=True)
    #     else:
    #         logger.error(error)
    #         return await ctx.send('Молодец, ты мегамозг, ты все разъебал, вызывай главного', ephemeral=True)

    @staticmethod
    def _get_task_start_time():
        utc = datetime.timezone.utc
        time = datetime.time(hour=HOUR, minute=MIN, tzinfo=utc)
        return time

    @staticmethod
    def _validate_date(date: str):
        if not date:
            return None
        try:
            date = datetime.datetime.strptime(date, '%d.%m')
        except ValueError:
            return None
        return date.strftime('%d.%m')

    @staticmethod
    def _get_today_date() -> str:
        today_date = datetime.datetime.now().strftime('%d.%m')
        return today_date

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

    @tasks.loop(time=_get_task_start_time())
    async def check_date(self):
        channel = self.bot.get_channel(CHANNEL_TO_POST)
        for msg in self.service('asd').create_msg_for_birthday_boys(self._get_today_date()):
            await channel.send(msg)


async def setup(bot):
    b = Birthdays(bot, BirthdayService)
    await bot.add_cog(b)
    b.check_date.start()
