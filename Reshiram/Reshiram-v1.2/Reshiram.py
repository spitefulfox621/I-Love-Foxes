from spiteƒox import spitefox
import os, random, asyncio, aiohttp, aiofiles, json, logging

import discord
from discord import app_commands
from discord.ext import commands

from components.Reshiram_Furfag import furfag
from components.Reshiram_Voicemessage_Handler import VoiceMessageManager
from components.Reshiram_Extra_Functions_Squared import Reshiram_Extra_Functions_2, Reshiram_Web_Requests, Reshiram_Mcss_Requests

furfag.firTimers.start('startup')

# ⠀⠀⠀⠀⠀⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⣸⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⢻⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣠⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⡀⠴⣾⣿⣿⣿⣤⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀⠀⠀⣀⣤⣾⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣀⠀⠀⣤⣾⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⣿⢸⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⢻⣿⣿⡿⠿⠟⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣌⣃⣼⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⢀⣠⣤⣴⣿⣿⣍⣠⣶⣶⣶⣦⡈⢻⣿⣿⣿⣿⣿⣿⡿⠟⠋⠉⠋⠉⠛⢿⣿⣿⣿⣿⣿⠅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠈⠛⠛⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⠾⠿⣿⣿⣿⣿⣿⣤⣴⣶⣿⣿⣷⣶⣀⢹⣿⣿⣤⣶⣶⡶⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⣰⣯⣛⣉⢩⡟⠟⢿⣿⣿⣦⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⢰⠿⠿⠟⠳⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣍⣀⡤⠀⠝⢉⣹⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⠿⣿⣿⣦⣉⣡⣬⣙⣁⣼⣿⣿⣿⣿⣿⣿⣷⠾⠟⠻⢿⡿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢉⣹⣿⣿⣿⣿⣿⣿⣿⣉⣉⣭⣍⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⠿⣷⣾⣿⣿⣿⣿⣿⣿⡿⠟⣓⣈⣅⣙⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⡟⢋⣤⣴⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠾⠿⢿⣿⣿⣿⠏⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣦⠹⡇⣾⣿⣧⢹⣿⡿⠛⢻⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡆⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣶⣤⣀⣉⣁⠈⠠⣤⣶⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⣆⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡄⠀⢰⣿⣿⣧⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣧⢹⣿⣿⣿⣆⢻⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣧⠀⣾⣿⣿⣿⣧⡀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⣿⣿⣿⣿⣿⣿⡈⢿⣿⣿⣿⣦⣙⠛⠛⢋⡁⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣰⣿⣿⣿⣿⣿⣷⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⢀⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣁⡀⠀⠀⠀⠀⣀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⢰⣿⣿⣿⣿⣿⣿⣿⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⢡⣠⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
# ⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⡄⢽⣿⣿⣿⣿⣿⣿⢌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇

class Reshiram(commands.Bot):
    def __init__(self, session):
        super().__init__(command_prefix=furfag.config["trigger-words"]["prefixes"], intents=discord.Intents.all(), tree_cls=self.ErrorHandler)
        self.status_cycle_wait_time = 600
        self.resshion = session # resshion was the best thing i came up with since firLoggers
        self.vmm = VoiceMessageManager(self.http)

    async def setup_hook(self):
        await furfag.firLoggers("DISCORD", "D", "running reshidirs")
        await self.reshidirs()
        await furfag.firLoggers("DISCORD", "D", "running setup_logs")
        await self.setup_logs()
        await furfag.firLoggers("DISCORD", "D", "running the_cog_is_coming")
        await self.the_cog_is_coming()
        await furfag.firLoggers("DISCORD", "I", "setup_hook complete")
        furfag.firYappers.square()

    async def on_ready(self):
        furfag.firYappers.ready()
        await furfag.firLoggers("DISCORD", "I", f"{furfag.client} is ready")
        await self.finalize()

    async def finalize(self):
        try:
            ##############################################################################
            await furfag.firLoggers("DISCORD", "I", f"logged in as {self.user}")
            await furfag.firLoggers("DISCORD", "I", f"synced {len(await self.tree.sync())} command(s)")
            await furfag.firLoggers("DISCORD", "I", f"login took {self.latency:.2f} seconds")
            ##############################################################################
            self.syffyserver = self.get_guild(furfag.config["guild-ids"]["main_server"])
            self.syffycache = self.get_guild(furfag.config["guild-ids"]["cache_server"])
            self.syffycache2 = self.get_guild(furfag.config["guild-ids"]["icon_server"])
            self.reshiram_channel = self.get_channel(furfag.config["channel-ids"]["reshiram_channel"])
            ##############################################################################
            self.REF = self.get_cog('Reshiram_Extra_Functions')
            self.REF2 = Reshiram_Extra_Functions_2
            self.RWR = Reshiram_Web_Requests(self.resshion)
            self.RMR = Reshiram_Mcss_Requests(self.resshion)
            ##############################################################################
            self.reshiram_badge = f"{await self.fetch_application_emoji(1361771372170314118)}{await self.fetch_application_emoji(1361771381422817301)}{await self.fetch_application_emoji(1361771390478454944)}{await self.fetch_application_emoji(1361771404042833960)}{await self.fetch_application_emoji(1361771414365143221)}{await self.fetch_application_emoji(1361771422568939713)}{await self.fetch_application_emoji(1361771429275894172)}"
            self.reshiram_emoji = f"{await self.fetch_application_emoji(1361772894127915269)}"
            self.thefogiscoming = f"{discord.utils.get(self.syffyserver.emojis, name='thefogiscoming')}"
            ##############################################################################
            if self.guilds:
                for s in self.guilds:
                    await furfag.firLoggers("DISCORD", "I", f"successfully loaded {s.name} ({s.id})")
                    if furfag.config["settings"]["autogenerate_server_configs"] is True:
                        if not os.path.exists(os.path.join(self.server_path, str(s.id))):
                            os.mkdir(os.path.join(self.server_path, str(s.id)))
                            await furfag.firLoggers("SYSTEM", "D", f"created server directory for {s.name}")
                        server_config = os.path.join(os.path.join(self.server_path, str(s.id)), f"config.json")
                        if not os.path.exists(server_config):
                            server_config_file = {
                                "server_name": s.name,
                                "server_id": s.id,
                                "owner_id": s.owner_id,
                                "members": [(member.name) async for member in s.fetch_members(limit=200)],
                                "server_specific_config": {
                                    "example_setting" : {
                                        "example_string": "hello world",
                                        "example_integer": 69,
                                        "example_boolian": False
                                    },
                                    "example_setting_2" : {
                                        "example_string": "goodbye world",
                                        "example_integer": 420,
                                        "example_boolian": True
                                    }
                                }
                            }
                            async with aiofiles.open(server_config, "w", encoding='utf-8') as f:
                                data = json.dumps(server_config_file, indent=2)
                                await f.write(data)
                                await furfag.firLoggers("SYSTEM", "D", f"created server config for {s.name}")


                if not self.syffyserver or not self.syffycache or not self.syffycache2:
                    await furfag.firLoggers("DISCORD", "E", f"couldn't load {'syffy' if self.syffyserver is None else 'syffycache' if self.syffycache is None else 'syffyicons' if self.syffycache2 is None else None}.")

            if furfag.config["settings"]["status_override_enabled"] is True:
                await self.change_presence(status=discord.Status.do_not_disturb, activity=discord.CustomActivity(name=furfag.config["status-config"]["status_override"][0]))
                await furfag.firLoggers("DISCORD", "D",  f"status overridden: {furfag.config["status-config"]["status_override"][0]}")
            else:
                self.loop.create_task(self.cycle_status(), name='reshiram_status_cycle')

        except Exception as e:
            await furfag.firLoggers("DISCORD", "E", f"an error occoured during finalization phase: [{e}]")

        finally:
            tasks = asyncio.all_tasks()
            for task in tasks:
                task.set_name(task.get_coro().__qualname__)

            task_names = [(t.get_name()) for t in tasks]
            task_names_formatted = ', '.join(task_names)
            await furfag.firLoggers("SYSTEM", "D",  f"running threads: {task_names_formatted}")
            elapsed = furfag.firTimers.stop('startup')
            await furfag.firLoggers("TIMER", "I", f"discord bot took {elapsed:.2f} seconds to fully set up")
            await furfag.firLoggers("DISCORD", "I", f"{furfag.client} is ready to go!~")

    async def the_cog_is_coming(self):
        await furfag.firLoggers("DISCORD", "D", f"the cog is coming. (loading cogs)")
        cog_files = [file for file in os.listdir(os.path.join(furfag.client_root, 'cogs')) if file.endswith('.py')]
        for file in cog_files:
            await self.load_extension(f'cogs.{file[:-3]}')
        await furfag.firLoggers("DISCORD", "I", f"the cog is coming. (loaded {len(cog_files)} cogs)")

    async def reshidirs(self):
        await furfag.firLoggers("SYSTEM", "D", f"creating reshidirs")
        ##############################################################################
        self.server_path = os.path.join(furfag.client_dir, 'servers')
        self.cache_path = os.path.join(furfag.client_dir, 'cache')
        self.logs_path = os.path.join(furfag.client_dir, 'logs')
        ##############################################################################
        tree_list = [
            self.server_path,
            self.cache_path,
            self.logs_path,
            ]
        await furfag.firHelpers.directory_manager(tree_list=tree_list)

    async def setup_logs(self):
        await furfag.firLoggers("SYSTEM", "D", f"setting up more detailed logging")
        ##############################################################
        systemdebug = os.path.join(self.logs_path, "system_debug.log")
        systeminfo = os.path.join(self.logs_path, "system_info.log")
        systemwarning = os.path.join(self.logs_path, "system_warning.log")
        systemerror = os.path.join(self.logs_path, "system_error.log")
        systemcritical = os.path.join(self.logs_path, "system_critical.log")
        ##############################################################
        discordlog = os.path.join(self.logs_path, "discord.log")
        ##############################################################
        logging.captureWarnings(True)
        ##############################################################
        rootlogger = logging.getLogger()
        rootlogger.setLevel(logging.DEBUG)
        discordlogger = logging.getLogger('discord')
        discordlogger.setLevel(logging.INFO)
        ########################################################################################################
        debug_handler = logging.FileHandler(filename=systemdebug, encoding='utf-8', mode='w')
        info_handler = logging.FileHandler(filename=systeminfo, encoding='utf-8', mode='w')
        warning_handler = logging.FileHandler(filename=systemwarning, encoding='utf-8', mode='w')
        error_handler = logging.FileHandler(filename=systemerror, encoding='utf-8', mode='w')
        critical_handler = logging.FileHandler(filename=systemcritical, encoding='utf-8', mode='w')
        ########################################################################################################
        discord_handler = logging.FileHandler(filename=discordlog, encoding='utf-8', mode='w')
        ########################################################################################################
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        info_handler.setLevel(logging.INFO)      # only INFO+ go here
        info_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        warning_handler.setLevel(logging.WARNING)# only WARNING+ go here
        warning_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        error_handler.setLevel(logging.ERROR)    # only ERROR+ go here
        error_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        critical_handler.setLevel(logging.CRITICAL)
        critical_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        ########################################################################################################
        rootlogger.addHandler(debug_handler)
        rootlogger.addHandler(info_handler)
        rootlogger.addHandler(warning_handler)
        rootlogger.addHandler(error_handler)
        rootlogger.addHandler(critical_handler)
        discordlogger.addHandler(discord_handler)
        ########################################################################################################
        #discord.utils.setup_logging(level=logging.INFO, handler=discord_handler, root=False)

    async def cycle_status(self):
        await furfag.firLoggers("DISCORD", "D", f"cycle_status has been started")
        await self.change_presence(status=discord.Status.idle, activity=discord.CustomActivity(name=f'🌙 almost there...'))
        status_map = [
            {"name": "do not disturb", "value": discord.Status.dnd},
            {"name": "idle", "value": discord.Status.idle},
            {"name": "online", "value": discord.Status.online},
        ]

        activity_map = [
            {"name": "competing", "value": discord.ActivityType.competing, "reshivalue": furfag.config["status-config"]["competing_statuses"]},
            {"name": "custom", "value": discord.ActivityType.custom, "reshivalue": furfag.config["status-config"]["custom_statuses"]},
            {"name": "listening", "value": discord.ActivityType.listening, "reshivalue": furfag.config["status-config"]["listening_statuses"]},
            {"name": "playing", "value": discord.ActivityType.playing, "reshivalue": furfag.config["status-config"]["playing_statuses"]},
            {"name": "streaming", "value": discord.ActivityType.streaming, "reshivalue": furfag.config["status-config"]["streaming_statuses"]},
            {"name": "watching", "value": discord.ActivityType.watching, "reshivalue": furfag.config["status-config"]["watching_statuses"]},
        ]

        await asyncio.sleep(10)
        while True:
            r_status = random.choice(status_map)
            r_activity = random.choice(activity_map)
            r_text = random.choice(r_activity["reshivalue"])

            if r_activity["name"] != "custom":
                await self.change_presence(status=r_status["value"],activity=discord.Activity(type=r_activity["value"],name=r_text, url='https://www.twitch.tv/lucariofucker'))
            else:
                await self.change_presence(status=r_status["value"],activity=discord.CustomActivity(name=r_text))
            await furfag.firLoggers("DISCORD", "D", f"status changed: {r_status["name"]}, {r_activity["name"]}, {r_text}")
            await asyncio.sleep(self.status_cycle_wait_time)

    class ErrorHandler(app_commands.CommandTree):
        async def on_error(self, interaction: discord.Interaction, error: Exception):
            if isinstance(error, app_commands.AppCommandError):
                await furfag.firLoggers("DISCORD", "E", f"app command error: {error}")
            elif isinstance(error, app_commands.CommandSyncFailure):
                await furfag.firLoggers("DISCORD", "E", f"command sylc failure: {error}")
            else:
                await furfag.firLoggers("DISCORD", "E", f"unknown error occoured: {error}")

    class FuckassAsyncioWrapper:
        # with ris() as husband: frot()
        def __init__(self):
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.session = None

        def spawn(self, task):
            """for running in the bg"""
            self.loop.create_task(task)

        def run(self, *tasks):
            """for running and awaiting, if multiple provided they run in parallel"""
            self.loop.run_until_complete(Reshiram.FuckassAsyncioWrapper.run_parallel(
                *tasks
            ))

        def kms(self):
            if self.session and not self.session.closed:
                self.loop.run_until_complete(self.session.close())
            tasks = asyncio.all_tasks(self.loop)
            for task in tasks:
                task.cancel()
            self.loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
            self.loop.close()

        @staticmethod
        async def run_parallel(*tasks):
            await asyncio.gather(*tasks)

        def __enter__(self):
            self.session = self.loop.run_until_complete(self._create_session())
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.kms()

        async def _create_session(self):
            return aiohttp.ClientSession()

# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠛⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠛⢠⡀⠸⣆⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⡁⢰⣋⡇⠀⡿⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠁⣏⠉⠛⠳⢤⣟⠀⢧⠀⠀⣀⣤⣠⣤⣄⣀⠀⠀⢷⠀⠀⠈⠙⠢⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡔⠃⣀⠘⢆⣀⠀⠀⠉⠀⠘⠚⠉⠀⠀⢀⡀⠀⢸⠇⣀⢸⡀⠀⠀⠀⠀⠈⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⠙⡾⠟⣷⠂⠉⠀⠀⠀⠀⠀⠀⠀⢶⢚⣹⠃⢠⡏⠀⡏⠹⠃⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣼⠇⣰⠀⠀⠀⠠⠶⠳⣦⠀⠀⠀⠘⠲⠃⢠⠟⠁⠀⡏⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠈⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠏⡟⠷⠟⠁⠀⠀⣴⡆⠀⢸⡇⠀⠀⢠⣄⡴⠏⠀⡀⢰⠇⠀⠀⠀⠀⠀⠀⢠⡾⠚⠋⠉⠉⢳⡀⠀⠀⠀⠀⠀
# ⠀⢹⡌⠙⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⢧⡐⠶⠄⠀⠀⠻⣃⡀⠸⡷⠀⠀⠀⠹⣆⠀⢀⡿⡏⠀⠀⠀⠀⠀⠀⣠⡾⠀⠀⠀⢀⡴⠟⠁⠀⠀⠀⠀⠀
# ⠀⠀⢷⠀⠀⠻⣷⣄⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠙⠦⣤⣀⡀⠀⠘⠿⠇⠀⣤⠴⣶⣞⣁⣠⣾⡀⠀⠀⣤⣠⣴⠶⢾⣁⣧⠀⠀⠀⠈⢧⡤⠖⠚⠦⣄⡀⠀
# ⠀⠀⠘⡇⠀⠀⠈⠻⣷⡀⠀⠀⣠⢾⡉⢉⡍⠙⠳⣶⢟⣯⣭⠿⠷⣤⡀⣠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠛⠚⠻⠀⠀⠀⠀⠈⣇⠀⠀⠀⠀⠙⣦
# ⠀⠀⠀⢹⡀⠀⠀⠀⢿⣧⠀⠀⢧⣸⡀⠘⣇⣴⠀⠀⢘⠛⠛⠀⣰⠊⠻⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣤⣄⣄⡓⣶⠏
# ⠀⠀⠀⠀⣧⠀⠀⠀⠈⣿⣆⣠⣤⣭⡭⠿⣹⣿⡋⠉⠛⠓⠒⠴⠃⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣇⠈⠙⠛⠁⠀
# ⠀⠀⠀⠀⠈⠳⣄⠀⠀⠸⣿⠉⠀⠈⢻⠞⠙⡾⠁⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣀⣀⣀⣀⣀⣀⣀⣬⠷⠶⠤⢤⣤⣄⣀⣀⣤⣄⡀⣰⠤⢽⠆⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠈⠳⣄⠀⢿⣧⠀⠀⠘⠷⠾⠷⣼⣅⣀⣀⠀⠀⠀⠀⠀⠀⠸⡅⠀⠀⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠏⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠘⢧⡈⡿⣄⣀⣀⣀⣀⣀⣈⣳⣍⠉⠉⠛⢿⡛⢦⡼⠛⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⠻⠶⠿⠿⠷⠷⠿⠿⠾⠶⠶⠶⠶⠿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

if __name__ == "__main__":
    with Reshiram.FuckassAsyncioWrapper() as a:
        Reshifag = Reshiram(a.session)
        a.spawn(furfag.firHelpers.handle_printers_queue())
        a.spawn(furfag.firHelpers.handle_furfag_colours())
        a.run(Reshifag.start(token=furfag.firHelpers.get_discord_bot_token()))