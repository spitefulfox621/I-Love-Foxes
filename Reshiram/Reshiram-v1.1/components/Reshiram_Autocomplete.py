"""
autocomplete for Reshiram\n
discord autocomplete for some, enum autocomplete for others
"""

from spiteƒox import spitefox
import os, json, aiofiles

from discord import Interaction, Status, ActivityType, app_commands

from components.Reshiram_Furfag import furfag

from enum import Enum

class DiscordAutocomplete:
    class ServerChoice(app_commands.Transformer):
        async def transform(self, interaction: Interaction, value: str):
            serverId, status, name = value.split("||") # splits name||id||status into variables
            return {
                "name": name,
                "serverId": serverId,
                "status": status
            }
            # returns a dictionairy

        async def autocomplete(self, interaction: Interaction, current: str):
            try:
                server_list, status_code, reason = await interaction.client.RMR.get_server_list(1) # minimal server list
                keys_to_remove = {"description", "creationDate", "serverPermissions"} # filters out these keys
                server_list_filtered = [{k: v for k, v in server.items() if k not in keys_to_remove} for server in server_list]

                if status_code == 200:
                    options = [
                        app_commands.Choice(
                            name=s['name'],
                            value=
                            f"{s['serverId']}||{s['status']}||{s['name']}"
                        )
                        for s in server_list_filtered
                        if current.lower() in s['name'].lower()
                    ]
                    return options
            except Exception as e:
                await furfag.firLoggers("DISCORD", "E", f"autocomplete ServerChoice failed: {e}")

    class AvailableCogs(app_commands.Transformer):
        async def transform(self, interaction: Interaction, value: str):
            return value

        async def autocomplete(self, interaction: Interaction, current: str):
            try:
                available_cogs = [
                    {
                        "name": os.path.splitext(file)[0].replace('_', ' ').capitalize(), # capitalize file name and remove _
                        "value": os.path.splitext(file)[0] # value is just the file name
                        }
                    for file in os.listdir(os.path.join(furfag.client_root + '\\cogs')) # directory to search in(client_root + 'cogs')
                    if file.endswith('.py') # only add files that end with .py
                ]
                response = [
                    app_commands.Choice(name=cog["name"], value=cog["value"])
                    for cog in available_cogs
                    if current.lower() in cog["name"].lower()
                ]
                return response
            except Exception as e:
                await furfag.firLoggers("DISCORD", "E", f"autocomplete AvailableCogs failed: {e}")

    class FeatureList(app_commands.Transformer):
        async def transform(self, interaction: Interaction, value: str):
            return value

        async def autocomplete(self, interaction: Interaction, current: str):
            new_features_file_path = os.path.join(spitefox.locations.spitefox_dir_p, furfag.client, "new features.json")
            async def load_nffp():
                async with aiofiles.open(new_features_file_path, "r", encoding='utf-8') as f:
                    file = await f.read()
                    data = json.loads(file)
                    return data, 200
            try:
                featurelist, status_code = await load_nffp()
                if status_code == 200:
                    options = [
                        app_commands.Choice(
                            name=f['suggestion'][:60],
                            value=f['id']
                            )
                        for f in featurelist
                        if current.lower() in f['suggestion'].lower()
                    ]
                    return options
            except Exception as e:
                await furfag.firLoggers("DISCORD", "E", f"autocomplete ServerChoice failed: {e}")

class CustomAutocomplete:
    class StatusMap(Enum):
        Dnd = Status.dnd
        Idle = Status.idle
        Invisible = Status.invisible
        Offline = Status.offline
        Online = Status.online

    class ActivityMap(Enum):
        Competing = ActivityType.competing
        Custom = ActivityType.custom
        Listening = ActivityType.listening
        Playing = ActivityType.playing
        Streaming = ActivityType.streaming
        Watching = ActivityType.watching

    class ServerActions(Enum):
        Stop = 1
        Start = 2
        Kill = 3
        Restart = 4

    class ChangeStatus(Enum):
        Done = "✅ done"
        WIP = "⏳ work in progress"
        WontFix = "🙂‍↔️ won't fix"
        Denied = "❌ denied"
        Pending = "💭 pending"
        Other = ".customstatus"
        Deleted = ".deleteentry"

    class DeactivateMethod(Enum):
        Blatant = 0
        Silent = 1
        p_Silent = 2