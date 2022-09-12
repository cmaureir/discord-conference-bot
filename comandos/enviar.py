from discord.ext import commands
from discord import TextChannel

class Enviar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role("Organización")
    @commands.command(name="enviar", help="Envia un mensaje a un canal", pass_context=True)
    async def enviar(self, ctx, channel: TextChannel, *, msg: str):
        await channel.send(msg)
