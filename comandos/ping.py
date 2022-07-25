from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role("Organización")
    @commands.command(name="ping", help="Comando de prueba", pass_context=True)
    async def pingpong(self, ctx):
        await ctx.send("pong")
