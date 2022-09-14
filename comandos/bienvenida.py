from discord.ext import commands
from logger import logger


class Bienvenida(commands.Cog):
    def __init__(self, bot, channel_id):
        self.bot = bot
        self.channel_id = channel_id

        self.channel = None
        logger.info("Cog 'Bienvenida' ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):

        if self.channel is None and self.bot.guild is not None:
            logger.info("Setting up channel")
            self.channel = self.bot.guild.get_channel(self.channel_id)

        await self.channel.send(
            f"¡Hola {member.mention}! "
            "Te damos la bienvenida al server de la PyConES\n"
            "¿Nos cuentas un poco de ti?"
        )
