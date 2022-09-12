from discord.ext import commands
from discord import User
from datetime import datetime, timezone
import pandas as pd

class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role("Organización")
    @commands.command(name="warning", help="Asigna un warning a un user", pass_context=True, aliases=["warn", "advertencia"])
    async def agregar_warning(self, ctx, user: User, *, reason: str):
        timestamp = datetime.now(timezone.utc)

        row_data =  {
            "time": [timestamp],
            "reporter": [ctx.author],
            "reported": [user],
            "reason": [reason],
        }
        row_df = pd.DataFrame.from_dict(row_data)
        self.bot.warnings = pd.concat([self.bot.warnings, row_df]).reset_index()
        self.bot.warnings.to_csv("warnings.csv", index=False, sep=";")
        await ctx.channel.send("Advertencia registrada")

    @commands.has_role("Organización")
    @commands.command(name="warning_check", help="Verifica el estado de los warnings", pass_context=True, aliases=["warn_check", "advertencia_check"])
    async def verificar_warning(self, ctx, user: User=None):
        print(self.bot.warnings)
        if user is None:
            _df = self.bot.warnings
        else:
            print(user, str(user))
            _df = self.bot.warnings[self.bot.warnings["reported"] == str(user)]

        output = ""
        for idx, row in _df.iterrows():
            output += f"{idx}: {row['reported']} - {row['reason']}\n"

        if not output:
            await ctx.channel.send(f"No warnings for user: {user}")
        else:
            await ctx.channel.send(output)


    @commands.has_role("Organización")
    @commands.command(name="warning_remove", help="Elimina warning basado en índice", pass_context=True, aliases=["warn_remove", "advertencia_remove"])
    async def eliminar_warning(self, ctx, idx: int):
        if isinstance(idx, int):
            if idx in self.bot.warnings.index:
                self.bot.warnings = self.bot.warnings.drop(index=idx)
                await ctx.channel.send(f"Eliminada advertencia: {idx}")
            else:
                await ctx.channel.send(f"Índice incorrecto: {idx}\nOpciones disponibles:")
                output = ""
                for idx, row in _df.iterrows():
                    output += f"{idx}: {row['reported']} - {row['reason']}\n"
                await ctx.channel.send(output)
        else:
            await ctx.channel.send(f"Primer argumento debe ser el ID de la advertencia. Usaste: {idx}")
