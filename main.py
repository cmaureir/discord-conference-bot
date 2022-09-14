import asyncio
import discord
import pandas as pd
from pathlib import Path
from ext import get_config_data
from discord.ext import commands
from comandos.ping import Ping
from comandos.purge import Purge
from comandos.programa import Programa
from comandos.bienvenida import Bienvenida
from comandos.enviar import Enviar
from comandos.warnings import Warnings
from comandos.programar_mensaje import ProgramarMensaje

from logger import logger

data = get_config_data()
logger.info("Got configuration data")

si_emoji = "\N{WHITE HEAVY CHECK MARK}"


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(command_prefix=commands.when_mentioned_or("$"), intents=intents)

        self.guild = None
        self.channels = dict()

    async def on_ready(self):
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        await self.tree.sync()
        if self.guild is None:
            self.guild = discord.utils.get(self.guilds, name="PyConES 2022")
            for channel in self.guild.text_channels:
                self.channels[channel.name] = channel.id
            logger.info(f"Found {len(self.channels)} channels")

    async def on_command_error(self, ctx, error):
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            logger.warning(f"Permission denied: on {ctx.channel} from {ctx.author}")
        else:
            logger.info(error)
            logger.info("Not handled")

    async def on_reaction_add(self, reaction, user):
        msg = reaction.message
        if msg.channel.id == 986704490470182912:
            if reaction.emoji != si_emoji:
                await msg.remove_reaction(reaction, user)


async def main():
    async with bot:
        await bot.add_cog(Ping(bot))
        await bot.add_cog(Purge(bot))
        await bot.add_cog(Bienvenida(bot, data["canal_bienvenida_id"], data["guild_id"]))
        await bot.add_cog(Enviar(bot))
        await bot.add_cog(Warnings(bot))
        await bot.add_cog(ProgramarMensaje(bot))
        # TODO
        # El funcionamiento de crear programas personalizados aún no está listo
        # await bot.add_cog(Programa(bot, data['canal_programa_id'], data['admin_role']))
        await bot.start(data["bot_token"])


if __name__ == "__main__":
    bot = Bot()

    warnings_records = Path(data["warnings_file"])
    if not warnings_records.is_file():
        with open(warnings_records, "w") as f:
            f.write("date;reporter;reported;reason\n")

    scheduled_records = Path(data["scheduled_messages_file"])
    if not scheduled_records.is_file():
        with open(scheduled_records, "w") as f:
            f.write("author;date;channel;message\n")

    bot.warnings = pd.read_csv(data["warnings_file"], sep=";")
    bot.scheduled = pd.read_csv(data["scheduled_messages_file"], sep=";")
    logger.info(f"Warnings: {bot.warnings.shape[0]}")
    logger.info(f"Scheduled messages: {bot.scheduled.shape[0]}")

    asyncio.run(main())
