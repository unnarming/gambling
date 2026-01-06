from discord.ext import commands
from embeds import Embeds
from config import Config
from sql import Sql

class MiscCog(commands.Cog):
    def __init__(self, bot: commands.Bot, config: Config, sql: Sql):
        self.bot = bot
        self.config: Config = config
        self.sql: Sql = sql
        self.embeds: Embeds = Embeds(config)

    def check_permission(self, ctx: commands.Context) -> bool:
        return ctx.author.id in self.config.permission_whitelist_uids

    @commands.command(name="test", description="Test the bot")
    async def ping(self, ctx: commands.Context):
        await ctx.send(embed=self.embeds.error("Test"))