from discord.ext import commands
from discord import app_commands

from logger import logger


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        logger.info("Cog 'Ping' ready")

    @commands.has_role("Organización")
    @commands.hybrid_command(name="ping", description="Simple ping/pong command")
    async def ping_command(self, ctx: commands.Context) -> None:
        await ctx.send("pong")
