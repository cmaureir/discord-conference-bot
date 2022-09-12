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
from comandos.programar import Programar

from logger import logger

data = get_config_data()
logger.info("Got configuration data")

si_emoji = "\N{WHITE HEAVY CHECK MARK}"

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents)

    async def on_ready(self):
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')

    async def on_command_error(self, ctx, error):
        if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            logger.warning(f"Permission denied: on {ctx.channel} from {ctx.author}")
        else:
            logger.info(error)
            logger.info("Not handled")

    async def on_ready(self):
        channel = self.get_channel(986704490470182912)


        content = f"¿Te gustaría armar tu programa? Presiona el {si_emoji} de este mensaje"

        msg = await channel.send(content)
        await msg.add_reaction(si_emoji)

    async def on_reaction_add(self, reaction, user):
        msg = reaction.message
        if msg.channel.id == 986704490470182912:
            if reaction.emoji != si_emoji:
                await msg.remove_reaction(reaction, user)
            print(user)



async def main():
    async with bot:
        await bot.add_cog(Ping(bot))
        await bot.add_cog(Purge(bot))
        await bot.add_cog(Bienvenida(bot, data['canal_bienvenida_id'], data['guild_id']))
        await bot.add_cog(Programa(bot, data['canal_programa_id'], data['admin_role']))
        await bot.add_cog(Enviar(bot))
        await bot.add_cog(Warnings(bot))
        await bot.start(data['bot_token'])

if __name__ == "__main__":
    bot = Bot()

    warnings_records = Path(data["warnings_file"])
    if not warnings_records.is_file():
        with open(warnings_records, "w") as f:
            f.write("time;reporter;reported;reason\n")

    bot.warnings = pd.read_csv(data["warnings_file"], sep=";")
    logger.info(f"Warnings: {bot.warnings.shape[0]}")

    asyncio.run(main())
