from discord.ext import commands
from discord import Member, app_commands
from discord.ext.commands.context import Context
from services import PasteService
import logging

logger = logging.getLogger(__name__)


class Pastes(commands.Cog):

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

    @commands.hybrid_group(description='Команды связанные с пастами')
    async def paste(self, ctx: Context):
        await ctx.send_help()

    @paste.command(name='pain', description='Для попускания клоунов')
    @app_commands.describe(
            user='Выберите юзера с клоунской манерой речи')
    @app_commands.rename(user='пользователь')
    async def pain(self, ctx: Context, user: Member):
        msg = self.service.get_paste('pain', [user])
        await ctx.send(msg)

    @paste.command(name='gay', description='Отпустить гейскую шуточку')
    @app_commands.describe(
            first_user='Выберите юзера со странными наклонностями',
            second_user='Выберите второго юзера со странными наклонностями')
    @app_commands.rename(first_user='пользователь', second_user='второй_пользователь')
    async def gay(self, ctx: Context, first_user: Member, second_user: Member):
        msg = self.service.get_gay_joke([first_user, second_user])
        await ctx.send(msg)


async def setup(bot):
    await bot.add_cog(Pastes(bot, PasteService))
