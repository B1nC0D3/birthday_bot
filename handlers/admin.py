from discord.ext import commands
from discord.ext.commands.context import Context
import logging

logger = logging.getLogger(__name__)


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx: Context, error: commands.CommandError):
        await super().cog_command_error(ctx, error)
        if isinstance(error, (commands.BadArgument, commands.MissingRequiredArgument, commands.CommandNotFound)):
            return await ctx.send('Кожаный, ты совсем дурачок?', ephemeral=True)
        elif isinstance(error, commands.NotOwner):
            return await ctx.send('Кожаный, даже я понимаю что сюда не надо лезть')
        else:
            logger.error(error)
            return await ctx.send('Молодец, ты мегамозг, ты все разъебал, вызывай главного')

    @commands.hybrid_group(hidden=True)
    @commands.is_owner()
    async def adm(self, ctx: Context):
        await ctx.send('nope')

    @adm.command(hidden=True, description='admin commands')
    @commands.is_owner()
    async def test(self, ctx: Context):
        await ctx.send('test')

    @adm.command(hidden=True, description='admin commands')
    @commands.is_owner()
    async def sync(self, ctx: Context):
        await self.bot.tree.sync()
        await ctx.send('Done!', ephemeral=True, delete_after=10)


async def setup(bot):
    await bot.add_cog(Admin(bot))
