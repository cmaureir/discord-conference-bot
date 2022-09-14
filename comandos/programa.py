from discord.ext import commands
import discord


# Define a simple View that gives us a confirmation menu
class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Confirming", ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Cancelling", ephemeral=True)
        self.value = False
        self.stop()


class Programa(commands.Cog):
    def __init__(self, bot, programa_id, admin_role):
        self.bot = bot
        self.programa_id = programa_id
        self.admin_role = admin_role

    @commands.command(name="programa", help="Comenzar configuración programa", pass_context=True)
    async def comienza_programa(self, ctx):
        print("programa")


#        guild = ctx.message.guild
#        category = ctx.channel.category
#        author_name = ctx.message.author
#
#        logger.info(f"Creación programa '{author_name}'")
#        if ctx.channel.id != self.programa_id:
#            print("nope")
#            logger.warning(f"{author_name} usó canal incorrecto {ctx.channel.name}")
#            return
#
#        # FIXME: This might be a problem if two users exists with username#XXXX and username#YYYY
#        channel_name = f"programa_{author_name.name}"
#        channel = utils.get(category.channels, name=channel_name)
#        channels = [i.name for i in category.channels]
#        # Verificar si el canal #programa-username existe si no, se crea.
#        if channel_name is None or channel_name not in channels:
#            logger.info(f"Creando canal {channel_name}")
#            channel = await guild.create_text_channel(channel_name, category=category, topic="lala")
#        else:
#            logger.warning(f"Canal '{channel_name}' ya existe")
#
#        view = Confirm()
#        mensaje = await channel.send(f"Hola {author_name.mention} "
#                           "¿Te gustaría comenzar a configurar tu programa?",
#                           view=view)
#
#        await view.wait()
#        if view.value is None:
#            print('Timed out...')
#        elif view.value:
#            print('Confirmed...')
#        else:
#            print('Cancelled...')
#
#        await discord.Message.delete(mensaje)

# Enviar mensaje en el nuevo canal para comenzar la selección de charlas
# Preguntar qué día de la conferencia se quiere configurar
# Enviar lista de charlas por bloque de horario
# Agregar reacciones para las charlas que se seleccionarán
# Agregar opción de no seleccionar ninguna
