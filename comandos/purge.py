from discord.ext import commands

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role("Organización")
    @commands.command(name="purge", help="Elimina mensajes", pass_context=True)
    async def purge(self, ctx, n: int=None):
        if n is None:
            await ctx.channel.purge(limit=5)
        elif n == -1:
            await ctx.channel.purge()
        else:
            await ctx.channel.purge(limit=n+1)
