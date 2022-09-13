from discord.ext import commands
from discord import TextChannel, Embed

COLOR_MSG = 0x79093A


class Enviar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role("Organización")
    @commands.hybrid_command(name="send", help="Send message to a channel")
    async def send(self, ctx: commands.Context, channel: TextChannel, *, message: str):

        embed = Embed(
            title="Mensaje de la Organización",
            description=message,
            colour=COLOR_MSG,
        )

        await channel.send(embed=embed)
