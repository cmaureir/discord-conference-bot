from discord.ext import commands
from discord import TextChannel, Embed, app_commands

from logger import logger

COLOR_MSG = 0x79093A


class Enviar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("Cog 'Enviar' ready")

    @commands.has_role("Organización")
    @commands.hybrid_command(name="send", description="Send message to a channel")
    @app_commands.describe(
        channel="Channel name (using '#') to send the message",
        message="Message content, without quotes",
    )
    async def send(self, ctx: commands.Context, channel: TextChannel, *, message: str):

        reply_embed = Embed(
            title=f"Mensaje enviado a {channel}",
            description=f"{channel.mention}:\n{message}",
            colour=COLOR_MSG,
        )

        try:
            await ctx.reply(embed=reply_embed)
        except AttributeError:
            await ctx.channel.send(embed=reply_embed)

        embed = Embed(
            title="Mensaje de la Organización",
            description=message,
            colour=COLOR_MSG,
        )

        # Send the command to the channel passed to the command
        await channel.send(embed=embed)
