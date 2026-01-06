import discord
import os
from discord.ext import commands

from config import *
from embeds import Embeds
from cogs import *
from sql import Sql

class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, config: Config, sql: Sql):
        super().__init__(command_prefix="$", intents=intents)
        self.config = config
        self.sql = sql

    async def setup_hook(self) -> None:
        await self.add_cog(EventsCog(self, self.config, self.sql))
        await self.add_cog(MiscCog(self, self.config, self.sql))
        await self.add_cog(CoinflipCog(self, self.config, self.sql))
        await self.add_cog(EconomyCog(self, self.config, self.sql))

class Main:
    def __init__(self):
        self.config = Config()
        self.sql: Sql = Sql(self.config.DB_URL, self.config)
        self.sql.create_tables()
        self.embeds: Embeds = Embeds(self.config)

        intents = discord.Intents.default()
        intents.message_content = True
        
        self.bot = Bot(intents, self.config, self.sql)

    def run(self) -> None:
        os.system("cls")
        self.bot.run(self.config.TOKEN)

if __name__ == "__main__":
    main = Main()
    main.run()