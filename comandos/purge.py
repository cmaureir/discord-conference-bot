import asyncio

from discord.ext import commands
from discord import app_commands, Embed

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
        await ctx.message.delete()

        if n == -1:
            await ctx.channel.purge()
        else:
            await ctx.channel.purge(limit=n)

        embed = Embed(
            title=f"Purged '{n}' messages\n\n",
            description=f"Command performed by {ctx.author.mention}",
            colour=0x178D38,
        )

        await ctx.channel.send(embed=embed)
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=1)
