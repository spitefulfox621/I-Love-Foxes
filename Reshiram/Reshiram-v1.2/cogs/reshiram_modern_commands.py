"""
slash commands for Reshiram\n
"""
from spiteƒox import spitefox
import os, json, time, uuid, asyncio, aiofiles

import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from components.Reshiram_Autocomplete import DiscordAutocomplete, CustomAutocomplete

from components.Reshiram_Furfag import furfag
view = View()

class Reshiram_Modern_Init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await furfag.firLoggers("DISCORD", "I", f"{os.path.splitext(os.path.basename(__file__))[0].lower()} is ready")

    async def cog_load(self):
        await furfag.firLoggers("DISCORD", "I", f"{os.path.splitext(os.path.basename(__file__))[0].lower()} loaded")

class Reshiram_Modern_Minecraft_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="get-server-list", description="get the server list")
    async def get_mc(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            server_list, status_code, reason = await self.bot.RMR.get_server_list(0)
            if status_code == 200:
                await interaction.edit_original_response(content=f"server responded, constructing server list...\n-# {status_code} {reason}")
                keys_to_remove = {"creationDate", "isSetToAutoStart", "forceSaveOnStop", "keepOnline", "javaAllocatedMemory", "javaStartupLine", "serverPermissions"}
                server_list_new = [{k: v for k, v in server.items() if k not in keys_to_remove} for server in server_list]
                missing_icons = []
                for s in server_list_new:
                    server_id = s["serverId"]
                    server_id_truncated = s['serverId'][:8]
                    server_emoji = discord.utils.get(self.bot.syffycache.emojis, name=server_id_truncated) or 'SYFFYCACHE_iconMissing'
                    if server_emoji == 'SYFFYCACHE_iconMissing':
                        missing_icons.append(server_id)

                if missing_icons:
                    await interaction.edit_original_response(content=f"``{len(missing_icons)}`` icons weren't cached, attempting a cache rebuild...")
                    await self.bot.REF.cache_server_icons(missing_icons)

                server_details = []
                for server in server_list_new:
                    server_id = server['serverId']
                    server_status = server['status']
                    server_name = server['name']
                    server_description = server['description']
                    server_type = server["type"]
                    server_id_truncated = server['serverId'][:8]

                    server_icon = discord.utils.get(self.bot.syffycache.emojis, name=server_id_truncated) or discord.utils.get(self.bot.syffycache2.emojis, name='SYFFYCACHE_iconMissing')
                    status_icon = discord.utils.get(self.bot.syffycache2.emojis, name=f'SYFFYCACHE_{server_status}')
                    type_icon = discord.utils.get(self.bot.syffycache2.emojis, name=f'SYFFYCACHE_{server_type}')

                    line1 = f"{server_icon} {server_name}"
                    line2 = f"**TYPE**: {type_icon}\n**STATUS**: {status_icon}\n*{server_description}*"
                    line3 = True

                    server_details.append((line1, line2, line3))
                if server_details:
                    e_author=(f"Local Foxgames", "https://awooga.free.nf/localfoxgames.net", "https://iili.io/3cuA172.png")
                    e_body=(f"{self.bot.reshiram_badge}", "", "", 0x13781a)
                    e_fields=server_details
                    e_images=("", "https://iili.io/3cJwzU7.png")
                    e_footer=(f"{status_code} {reason}", "https://iili.io/3AE69YG.png")

            elif status_code == 408:
                async def fuckyou(interaction):
                    view.remove_item(fuckyoubutton)
                    await interaction.response.edit_message(content=f"-# couldn't contact server {status_code} {reason}\n:(", view=view, delete_after=1)
                fuckyoubutton = Button(label="Fuck You", style=discord.ButtonStyle.primary)
                fuckyoubutton.callback = fuckyou
                view.add_item(fuckyoubutton)
                await interaction.edit_original_response(content=f"couldn't contact server\n-# {status_code} {reason}", view=view)
                await asyncio.sleep(5)
                raise ValueError(f"{status_code} {reason}")

        except Exception as e:
            e_author=(f"Local Foxgames", "https://awooga.free.nf/localfoxgames.net", "https://iili.io/3cuA172.png")
            e_body=(f"{self.bot.reshiram_badge}", "", "", 0x781313)
            e_fields=[("an error occoured", f"error message: {e}", True)]
            e_images=("", "https://iili.io/3cmNr3x.png")
            e_footer=(f"❌", "https://iili.io/3AE69YG.png")

        finally:
            await interaction.edit_original_response(content="building embed...")
            embed = await self.bot.REF2.Webhook_Maker(author=e_author,body=e_body,fields=e_fields,images=e_images,footer=e_footer)
            await interaction.edit_original_response(content=None,embed=embed,view=None)

    @app_commands.command(name="post-server-action", description="send a server action")
    @app_commands.describe(server="the server to send an action to",action="what action to send")
    async def post_mc(self, interaction: discord.Interaction, server: app_commands.Transform[dict, DiscordAutocomplete.ServerChoice], action: CustomAutocomplete.ServerActions):
        await interaction.response.defer()
        if server['status'] == '0' and action.value != 2:
            await interaction.edit_original_response(content=f"server is already offline!")
        elif server['status'] == '1' and action.value == 2:
            await interaction.edit_original_response(content=f"server is already online!")
        else:
            action_verb_map = {1:"stopped",2:"started",3:"killed",4:"restarted"}
            action_verb = (action_verb_map[action.value])
            _, status_code, reason = await self.bot.RMR.post_server_action(server['serverId'], action.value)
            if status_code == 200:
                await furfag.firLoggers("SYSTEM", "I", f"server {server['name']} was {action_verb}")
                await interaction.edit_original_response(content=f"server ``{server['name']}`` was ``{action_verb}``\n-# {status_code} {reason}")
            else:
                view = View()
                fu_button = Button(label="Fuck You", style=discord.ButtonStyle.primary)
                async def fuckyou(interaction):
                    view.remove_item(fu_button)
                    await interaction.response.edit_message(content=f"-# couldn't contact server {status_code or None} {reason or None}\n:(", view=view, delete_after=1)
                fu_button.callback = fuckyou
                view.add_item(fu_button)
                await interaction.edit_original_response(content=f"couldn't contact server\n-# {status_code or None} {reason or None}", view=view)

class Reshiram_Slash_Command_Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="suggest-feature", description="suggest a feature for the bot")
    @app_commands.describe(feature="new command, custom response, technical change, etc")
    async def suggest_feature(self, interaction: discord.Interaction, feature: str):
        await furfag.firLoggers("DISCORD", "I", f"got a new feature!\n'{feature[:200]}'\n    |- submitted by {interaction.user.name}")
        new_features_file_path = os.path.join(spitefox.locations.spitefox_dir_p, furfag.client, "new features.json")

        entry = {
            "id": uuid.uuid4().hex,
            "user": interaction.user.name,
            "suggestion": feature[:200],
            "status": "💭 pending",
            "date_submitted": time.strftime('%d.%m.%y - %H:%M:%S'),
            "last_updated": time.strftime('%d.%m.%y - %H:%M:%S')
        }

        try:
            async with aiofiles.open(new_features_file_path, "r", encoding='utf-8') as f:
                file = await f.read()
                data = json.loads(file)

        except (json.JSONDecodeError, FileNotFoundError):
            data = []

        data.append(entry)
        async with aiofiles.open(new_features_file_path, "w", encoding='utf-8') as f:
            file = json.dumps(data, indent=2)
            await f.write(file)

        await interaction.response.send_message(content=f'feature submitted! thanks!', ephemeral=True)

    @app_commands.command(name="send-to-firlogger", description="send a message to the custom log handler")
    async def send_msg_to_fl(self, interaction: discord.Interaction, message: str):
        await furfag.firLoggers("DISCORD", "I", f"{interaction.user.name} lets you know: {message}")
        loggingemoji = discord.utils.get(self.bot.syffyserver.emojis, name='firLoggers')
        await interaction.response.send_message(f"{loggingemoji}sent ``{message}`` to firLoggers", ephemeral=True)

class Reshiram_Modern_System_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO: convert to context menu command
    @app_commands.command(name="addvote", description="[ADMIN ONLY] add vote reactions to a message")
    @app_commands.checks.has_permissions(administrator=True)
    async def addvote(self, interaction: discord.Interaction, message_id: str):
        await interaction.response.defer()
        try:
            message = await interaction.channel.fetch_message(int(message_id))
            upvote = await self.bot.fetch_application_emoji(1369456781129945088)
            downvote = await self.bot.fetch_application_emoji(1369456815867166750)
            await message.add_reaction(upvote)
            await message.add_reaction(downvote)
        except Exception as e:
            await interaction.edit_original_response(content=f"something went wrong(you were born). also the command failed(idk why(that was a lie, I do, but I'm not telling you.)).")
            await furfag.firLoggers("RESHIRAM", "E", f"error adding vote reactions: {e}")
        finally:
            await interaction.edit_original_response(content=f"added your stupid ass vote reactions you dumb faggot next time do it yourself, KYS")
            asyncio.sleep(10)
            await interaction.delete_original_response()

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
        await interaction.response.send_message(content=f'{self.bot.reshiram_emoji}changed status to ``{act_type.name}, {act_activity.name}, {act_text}``', delete_after=60)

    @app_commands.command(name="reload-cog", description="[ADMIN ONLY] reload a cog")
    @app_commands.checks.has_permissions(administrator=True)
    async def reload_cog(self, interaction: discord.Interaction, cog_to_reload: app_commands.Transform[str, DiscordAutocomplete.AvailableCogs]):
        try:
            await self.bot.reload_extension(f"cogs.{cog_to_reload}")
            await interaction.response.send_message(f"reloaded my cock- I mean cog. (``{cog_to_reload}``)", delete_after=5)
        except Exception as e:
            await interaction.response.send_message(f"awh fuck dude, you broke my cog :C", delete_after=5)
            await furfag.firLoggers("DISCORD", "E", f"couldn't reload cogs 4 sum reason: {e}")

    @app_commands.command(name="update-feature", description="[ADMIN ONLY] update a suggested feature")
    @app_commands.checks.has_permissions(administrator=True)
    async def update_feature(self, interaction: discord.Interaction, feature_to_change: app_commands.Transform[str, DiscordAutocomplete.FeatureList], new_status: CustomAutocomplete.ChangeStatus, custom_status: str = None):

        async def save_nffp(data):
            async with aiofiles.open(new_features_file_path, "w", encoding='utf-8') as f:
                file = json.dumps(data, indent=2)
                await f.write(file)

        async def load_nffp():
            async with aiofiles.open(new_features_file_path, "r", encoding='utf-8') as f:
                file = await f.read()
                data = json.loads(file)
                return data

        try:
            new_features_file_path = os.path.join(spitefox.locations.spitefox_dir_p, furfag.client, "new features.json")

            featurelist = await load_nffp()
            feature = next((f for f in featurelist if f["id"] == feature_to_change), None)
            original_suggestion = (f"original suggestion by ``{feature['user']}``:",f"- {feature['suggestion']} • (``{feature['status']}``)", False)

            if new_status.value == '.deleteentry':
                feature['status'] = f"🗑️ deleted"
                featurelist = [entry for entry in featurelist if entry.get('id') != feature_to_change]

            elif new_status.value == '.customstatus':
                feature['status'] = f"🦊 {custom_status}"

            else:
                feature['status'] = new_status.value

            feature['last_updated'] = time.strftime('%d.%m.%y - %H:%M:%S')

            updated_suggestion = (f"updated suggestion by ``{feature['user']}``:",f"- {feature['suggestion']} • (``{feature['status']}``)", False)
            faggots = [original_suggestion, updated_suggestion]
            await save_nffp(featurelist)

            uf_author=("Pending Features", "https://awooga.free.nf", "https://iili.io/3cuA172.png")
            uf_body=("", "", f"you updated a suggestion from ``{feature['user']}``", 0xdb1a1f)
            uf_fields=faggots
            uf_images=("", "")
            uf_footer=("", "")


        except Exception as e:
            await furfag.firLoggers("DISCORD", "E", f"{e}")
            uf_author=(f"New Features", "https://awooga.free.nf", "https://iili.io/3cuA172.png")
            uf_body=(f"{self.bot.reshiram_badge}", "", "", 0x781313)
            uf_fields=[("an error occoured", f"error message: {e}", False)]
            uf_images=("", "https://iili.io/3cmNr3x.png")
            uf_footer=(f"❌", "")

        finally:
            embed = await self.bot.REF2.Webhook_Maker(
                author=uf_author,
                body=uf_body,
                fields=uf_fields,
                images=uf_images,
                footer=uf_footer,
            )
            await interaction.response.send_message(embed=embed,delete_after=15)


async def setup(bot):
    await bot.add_cog(Reshiram_Modern_Init(bot))
    await bot.add_cog(Reshiram_Slash_Command_Handler(bot))
    await bot.add_cog(Reshiram_Modern_Minecraft_Commands(bot))
    await bot.add_cog(Reshiram_Modern_System_Commands(bot))