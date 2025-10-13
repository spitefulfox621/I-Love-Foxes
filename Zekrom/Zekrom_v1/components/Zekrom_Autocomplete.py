from spiteƒox import spitefox
import os, json, aiofiles

from discord import Interaction, Status, ActivityType, app_commands

from components.Zekrom_Furfag import furfag

from enum import Enum

class DiscordAutocomplete:
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
                await furfag.firLoggers("DISCORD", "E", f"autocomplete AvailableCogs failed\n{e}")


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