from discord.ext import commands, tasks
from discord import User, Embed, TextChannel, utils
from datetime import datetime, timezone

import pytz
import pandas as pd

COLOR_OK = 0x178D38
COLOR_ERROR = 0xFF0000


class ProgramarMensaje(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.envia_mensajes_programados.start()

    @commands.has_role("Organización")
    @commands.hybrid_group(
        name="schedule", help="Schedules a message in the future", fallback="create"
    )
    async def schedule_command(
        self, ctx: commands.Context, channel: TextChannel, date: str, time: str, *, message: str
    ):
        print(date, time, message)
        # TODO
        # - Check if date and time are in the future
        # - Show ID when the message was created

        _title = "\N{CALENDAR} Mensaje programado"
        _description = "Detalles"
        _error = False
        _color = COLOR_OK

        # Check splits work
        try:
            day, month, year = date.strip().split("-")
            hour, minutes = time.strip().split(":")
        except ValueError:
            _title = "\N{CROSS MARK} Error de formato de argumentos"
            _description = "Usar\ndate: DD-MM-YYY\ntime: HH:MM"
            _error = True

        # Check date is in the future
        if not _error:
            # NOTE
            # We will do calculations in UTC
            # but when a user enters a date it will highly probable be in UTC+2
            # which is CEST before October 30th.
            # When notifying the date we need to take care of the current difference
            # because after October 30th, it will be UTC+1
            now_date = datetime.now(timezone.utc)
            _date = f"{day}-{month}-{year} {hour}:{minutes}"
            scheduled_date = pytz.timezone("Europe/Madrid").localize(
                datetime.strptime(_date, "%d-%m-%Y %H:%M")
            )

            if now_date >= scheduled_date:
                _title = "\N{CROSS MARK} Error de fecha"
                _description = "La fecha debe estar en el **futuro**."
                _error = True

        if _error:
            _color = COLOR_ERROR

        embed = Embed(
            title=_title,
            description=_description,
            colour=_color,
        )

        if not _error:
            row_data = {
                "author": [ctx.author],
                "date": [scheduled_date],
                "channel": [channel],
                "message": [message],
            }
            row_df = pd.DataFrame.from_dict(row_data)
            self.bot.scheduled = pd.concat([self.bot.scheduled, row_df]).reset_index(drop=True)
            self.bot.scheduled.to_csv("scheduled.csv", index=False, sep=";")

            embed.add_field(name="Fecha", value=scheduled_date, inline=False)
            embed.add_field(name="Contenido", value=message, inline=False)

        try:
            await ctx.reply(embed=embed)
        except AttributeError:
            await ctx.channel.send(embed=embed)

    @commands.has_role("Organización")
    @schedule_command.command(name="remove", help="Removes scheduled message")
    async def remove_command(self, ctx: commands.Context, idx: int):

        _color = COLOR_OK
        _title = "Mensaje eliminado"

        if idx in self.bot.scheduled.index:
            row = self.bot.scheduled.iloc[idx]
            if self.bot.guild is not None:
                channel = utils.get(self.bot.guild.text_channels, name=row["channel"])
            else:
                channel = f"#row['channel']"
            _response = (
                f"Eliminado mensaje: {idx}\n"
                f"Date: `{row['date']}`\n"
                f"Author: `{row['author']}`\n"
                f"Channel: {channel.mention}\n"
                f"Message:\n{row['message']}\n"
            )

            self.bot.scheduled = self.bot.scheduled.drop(index=idx)
            self.bot.scheduled.to_csv("scheduled.csv", index=False, sep=";")
        else:
            _title = f"Índice incorrecto: {idx}"
            _response = "Verifica con `$schedule list`"
            _color = COLOR_ERROR

        embed = Embed(
            title=_title,
            description=_response,
            colour=_color,
        )

        try:
            await ctx.reply(embed=embed)
        except AttributeError:
            await ctx.channel.send(embed=embed)

    @commands.has_role("Organización")
    @schedule_command.command(name="list", help="Lists scheduled message")
    async def list_command(self, ctx: commands.Context):

        embed = Embed(
            title="\N{SPIRAL NOTE PAD} Mensajes programados\n\n",
            description="Use the ID as a reference to remove messages",
            colour=0x178D38,
        )

        for idx, row in self.bot.scheduled.iterrows():
            _date = row["date"]
            _author = row["author"]
            _channel = row["channel"]
            _message = row["message"]
            embed.add_field(
                name=f"ID {idx}: {_date}",
                value=f"(by {_author} in {_channel})\n{_message}",
                inline=False,
            )

        try:
            await ctx.reply(embed=embed)
        except AttributeError:
            await ctx.channel.send(embed=embed)

    @tasks.loop(minutes=1)
    async def envia_mensajes_programados(self):
        # TODO
        # Ordenar 'self.bot.scheduled' por fecha de menor a mayor.
        # Comparar el tiempo actual, con el objecto 'datetime'
        # que está en la columna 'date'
        now_date = datetime.now(timezone.utc)
        print("Mirando mensajes", now_date)
        for idx, row in self.bot.scheduled.iterrows():
            _date = pd.to_datetime(row['date'])
            print(_date)
            if _date < now_date:
                if self.bot.guild is None:
                    # TODO
                    # Enviar mensaje de error al canal #bot-admin
                    # diciendo que hubo un problema con el estado
                    # de la instancia de server del Bot.
                    # No debería pasar...
                    print("programar_mensaje: self.bot.guild not ready")
                else:
                    channel = utils.get(self.bot.guild.text_channels, name=row["channel"])
                    message = row['message']

                    embed = Embed(
                        title="Mensaje de la Organización\n\n",
                        description=message,
                        colour=COLOR_OK,
                    )

                    # Enviar mensaje
                    await channel.send(embed=embed)

                    # Borrar mensaje
                    self.bot.scheduled = self.bot.scheduled.drop(index=idx)
                    self.bot.scheduled.to_csv("scheduled.csv", index=False, sep=";")
