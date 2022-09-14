from discord.ext import commands
from discord import app_commands

from logger import logger

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("Cog 'Purge' ready")

    @commands.has_role("Organización")
    @commands.hybrid_command(name="purge", description="Remove messages in the channel")
    @app_commands.describe(
        n="Number of messages to remove (default: 5). If '-1' is passed, all messages are removed.",
    )
    async def purge(self, ctx: commands.Context, n: int = 5) -> None:
        if n == -1:
            await ctx.channel.purge()
        else:
            await ctx.channel.purge(limit=n + 1)
