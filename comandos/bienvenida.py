from discord.ext import commands
from logger import logger

class Bienvenida(commands.Cog):
    def __init__(self, bot, channel_id, guild_id):
        self.bot = bot
        self.channel_id = channel_id
        self.guild_id = guild_id

        self.guild = None
        self.channel = None
        logger.info("Bienvenida...")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.guild is None:
            logger.info("Setting up guild")
            self.guild = self.bot.get_guild(self.guild_id)

        if self.channel is None and self.guild is not None:
            logger.info("Setting up channel")
            self.channel = self.guild.get_channel(self.channel_id)

        await self.channel.send(f'¡Hola {member.mention}! '
                                'Te damos la bienvenida a la PyConES\n'
                                    '¿Nos cuentas un poco de ti?')
