from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.has_role("Organización")
    @commands.hybrid_command(name="ping")
    async def ping_command(self, ctx: commands.Context) -> None:
        await ctx.send("pong")
