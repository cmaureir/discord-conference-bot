from discord.ext import commands
from discord import User
from datetime import datetime, timezone
import pandas as pd

COLOR_OK = 0x178D38
COLOR_ERROR = 0xFF0000


class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role("Organización")
    @commands.hybrid_group(name="warning", help="Adds a warning to a certain user", fallback="add")
    async def warning_command(self, ctx: commands.Context, user: User, *, reason: str):
        timestamp = datetime.now(timezone.utc)

        row_data = {
            "date": [timestamp],
            "reporter": [ctx.author],
            "reported": [user],
            "reason": [reason],
        }
        row_df = pd.DataFrame.from_dict(row_data)
        self.bot.warnings = pd.concat([self.bot.warnings, row_df]).reset_index(drop=True)
        self.bot.warnings.to_csv("warnings.csv", index=False, sep=";")

        embed = Embed(
            title="Advertencia registrada",
            description=f"Reporter: `{ctx.author}`\nUser: `{user}`\nReason: `{reason}`",
            colour=COLOR_OK,
        )

        try:
            await ctx.reply(embed=embed)
        except AttributeError:
            await ctx.channel.send(embed=embed)

    @commands.has_role("Organización")
    @warning_command.command(name="list", help="List warnings")
    async def list_command(self, ctx: commands.Context, user: User = None):
        _output = ""

        if user is None:
            _df = self.bot.warnings
            for idx, row in _df.iterrows():
                _output += f"`{idx}`: {row['reported']} - {row['reason']}\n"
        else:
            _df = self.bot.warnings[self.bot.warnings["reported"] == str(user)]
            for idx, row in _df.iterrows():
                _output += f"`{idx}`: {row['reason']}\n"

        if not _output:
            embed = Embed(
                title=f"No warnings for user: {user}",
                description="",
                colour=COLOR_ERROR,
            )
        else:
            embed = Embed(
                title=f"Warnings for user: {user}",
                description=_output,
                colour=COLOR_OK,
            )

        try:
            await ctx.reply(embed=embed)
        except AttributeError:
            await ctx.channel.send(embed=embed)

    @commands.has_role("Organización")
    @warning_command.command(name="remove", help="Remove warnings by ID")
    async def remove_command(self, ctx: commands.Context, idx: int):
        if idx in self.bot.warnings.index:
            row = self.bot.warnings.iloc[idx]
            self.bot.warnings = self.bot.warnings.drop(index=idx)
            _title = f"Eliminada advertencia: {idx}"
            _description = (
                f"Date: `{row['date']}`\n"
                f"Reporter: `{row['reporter']}`\n"
                f"User: {row['reported']}\n"
                f"Reason:\n{row['reason']}\n"
            )
            _color = COLOR_OK
        else:
            _title = f"Índice incorrecto: {idx}"
            _description = "Utilice `$warning list` para listar"
            _color = COLOR_ERROR

        embed = Embed(
            title=_title,
            description=_description,
            colour=_color,
        )

        try:
            await ctx.reply(embed=embed)
        except AttributeError:
            await ctx.channel.send(embed=embed)
