import discord
from utils import Status
from config import Config

class Embeds:
    def __init__(self, config: Config):
        self.config = config

    def error(self, message: str) -> discord.Embed:
        return discord.Embed(colour=discord.Colour.red()).add_field(name="Error", value=message, inline=False)

    def status(self, status: Status) -> discord.Embed:
        if status.status:
            return discord.Embed(colour=discord.Colour.green()).add_field(name="Success", value=status.message, inline=False)
        else:
            return discord.Embed(colour=discord.Colour.red()).add_field(name="Error", value=status.message, inline=False)
    
    def success(self, message: str) -> discord.Embed:
        return discord.Embed(colour=discord.Colour.green()).add_field(name="Success", value=message, inline=False)

    def base(self, title: str = "", description: str = "") -> discord.Embed:
        return discord.Embed(colour=discord.Colour.blurple()).add_field(name=title, value=description, inline=False)