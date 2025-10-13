import os, discord

from discord.ext import commands
from discord import app_commands

from components.Zekrom_Furfag import furfag
from components.Zekrom_Autocomplete import DiscordAutocomplete, CustomAutocomplete

class Zekrom_Slash_Command_Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await furfag.firLoggers( "DISCORD", "I", f"{os.path.splitext(os.path.basename(__file__))[0].lower()} is ready")

    async def cog_load(self):
        await furfag.firLoggers( "DISCORD", "I", f"{os.path.splitext(os.path.basename(__file__))[0].lower()} loaded")

    @app_commands.command(name="deactivate", description="[ADMIN ONLY] deactivates the bot")
    @app_commands.checks.has_permissions(administrator=True)
    async def deactivate(self, interaction: discord.Interaction, deactivation_method: CustomAutocomplete.DeactivateMethod):
        await self.bot.change_presence(status=discord.Status.dnd,activity=discord.CustomActivity(name="💤 shutting down..."))
        await furfag.firLoggers("DISCORD", "W", "💤 shutting down...")
        try:
            if deactivation_method.value == 0:
                await interaction.response.send_message(f"{furfag.client}: deactivated", silent=False)
            elif deactivation_method.value == 1:
                await interaction.response.send_message(f"{furfag.client}: deactivated", silent=True)
            elif deactivation_method.value == 2:
                await interaction.response.send_message(f"{furfag.client}: deactivated", ephemeral=True)
        except Exception as e:
            await furfag.firLoggers("DISCORD", "E", f"error shutting down: {e}")
        finally:
            await self.bot.close()

    @app_commands.command(name="status-override", description="[ADMIN ONLY] override the status of the bot")
    @app_commands.describe(act_type="the status the bot should use", act_activity="the activity the bot should use", act_text="the custom text after the activity")
    @app_commands.checks.has_permissions(administrator=True)
    async def status_override(self, interaction: discord.Interaction, act_type: CustomAutocomplete.StatusMap, act_activity: CustomAutocomplete.ActivityMap, act_text: str):
        if act_activity.name.lower() != 'custom':
            await self.bot.change_presence(status=act_type.value, activity=discord.Activity(type=act_activity.value,name=act_text, url='https://www.twitch.tv/lucariofucker'))
        else:
            await self.bot.change_presence(status=act_type.value,activity=discord.CustomActivity(name=act_text))
        await interaction.response.send_message(content=f'{self.bot.zekrom_emoji}changed status to ``{act_type.name}, {act_activity.name}, {act_text}``', delete_after=60)

    @app_commands.command(name="reload-cog", description="[ADMIN ONLY] reload a cog")
    @app_commands.checks.has_permissions(administrator=True)
    async def reload_cog(self, interaction: discord.Interaction, cog_to_reload: app_commands.Transform[str, DiscordAutocomplete.AvailableCogs]):
        try:
            await self.bot.reload_extension(f"cogs.{cog_to_reload}")
            await interaction.response.send_message(f"reloaded my cock- I mean cog. (``{cog_to_reload}``)", delete_after=5)
        except Exception as e:
            await interaction.response.send_message(f"awh fuck dude, you broke my cog :C", delete_after=5)
            await furfag.firLoggers("DISCORD", "E", f"couldn't reload cogs 4 sum reason\n{e}")

async def setup(bot):
    await bot.add_cog(Zekrom_Slash_Command_Handler(bot))