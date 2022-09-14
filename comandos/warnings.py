from discord.ext import commands
from discord import User, Embed, app_commands
from datetime import datetime, timezone
import pandas as pd

from logger import logger

COLOR_OK = 0x178D38
COLOR_ERROR = 0xFF0000


class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("Cog 'Warnings' ready")

    @commands.has_role("Organización")
    @commands.hybrid_group(name="warning", description="Adds a warning to a certain user", fallback="add")
    @app_commands.describe(
        user="User to add warning, using '@'",
        reason="Reason for the warning",
    )
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
            colour=COLOR_OK,
        )
        embed.add_field(name="Author", value=ctx.author, inline=False)
        embed.add_field(name="Reported User", value=user, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)

        try:
            await ctx.reply(embed=embed)
        except AttributeError:
            await ctx.channel.send(embed=embed)

    @commands.has_role("Organización")
    @warning_command.command(name="list", description="List warnings")
    @app_commands.describe(
        user="(optional) User to list warnings, using '@'",
    )
    async def list_command(self, ctx: commands.Context, user: User = None):

        # Filter DataFrame
        if user is None:
            _df = self.bot.warnings
        else:
            _df = self.bot.warnings[self.bot.warnings["reported"] == str(user)]

        if _df.empty:
            if user is None:
                _title = "No warnings"
            else:
                _title=f"No warnings for user: {user}"

            embed = Embed(
                title=_title,
                description="",
                colour=COLOR_ERROR,
            )
        else:
            if user is None:
                _title = "List of warnings"
                embed = Embed(
                    title=_title,
                    description="",
                    colour=COLOR_OK,
                )
                for idx, row in _df.iterrows():
                    embed.add_field(name=f"ID: {idx} - {row['reported']}", value=row['reason'], inline=False)
            else:
                _title = f"List of warnings for user {user}"
                embed = Embed(
                    title=_title,
                    description="",
                    colour=COLOR_OK,
                )
                for idx, row in _df.iterrows():
                    embed.add_field(name=f"ID: {idx}", value=row['reason'], inline=False)

        try:
            await ctx.reply(embed=embed)
        except AttributeError:
            await ctx.channel.send(embed=embed)

    @commands.has_role("Organización")
    @warning_command.command(name="remove", description="Remove warnings by ID")
    @app_commands.describe(
        idx="Removes the warning from an ID value. Try '/warnings list' to see IDs.",
    )
    async def remove_command(self, ctx: commands.Context, idx: int):
        _fields = tuple()
        if idx in self.bot.warnings.index:
            row = self.bot.warnings.iloc[idx]
            self.bot.warnings = self.bot.warnings.drop(index=idx)
            _title = f"Eliminada advertencia: {idx}"
            _description = "--"
            _fields = (
                ("Date:", row['date']),
                ("Reporter", row['reporter']),
                ("User:", row['reported']),
                ("Reason:", row['reason']),
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

        if _fields:
            for _name, _value in _fields:
                embed.add_field(name=_name, value=_value, inline=False)

        try:
            await ctx.reply(embed=embed)
        except AttributeError:
            await ctx.channel.send(embed=embed)
