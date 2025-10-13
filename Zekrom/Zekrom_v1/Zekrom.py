from spiteƒox import spitefox
import os, random, asyncio, aiohttp

import logging, logging.handlers
import discord
from discord import app_commands
from discord.ext import commands

from components.Zekrom_Furfag import furfag
from components.Zekrom_Extra_Functions_Squared import Zekrom_Extra_Functions_2
furfag.firTimers.start('startup')

class Zekrom(commands.Bot):
    def __init__(self, session):
        super().__init__(command_prefix=furfag.config["trigger-words"]["prefixes"], intents=discord.Intents.all(),tree_cls=Zekrom.ErrorHandler)
        self.status_cycle_wait_time = 600
        self.resshion = session # resshion was the best thing i came up with since firLoggers

    async def setup_hook(self):
        await self.zekrodirs()
        await self.the_cog_is_coming()
        await furfag.firLoggers("DISCORD", "I", f"setup_hook complete")
        furfag.firYappers.square()

    async def on_ready(self):
        furfag.firYappers.ready()
        await furfag.firLoggers("DISCORD", "I", f"{furfag.client} is Ready! ✅")
        await self.finalize()

    async def finalize(self):
        try:
            await self.setup_logs()
            ##############################################################################
            await furfag.firLoggers("DISCORD", "I", f"logged in as {self.user}")
            await furfag.firLoggers("DISCORD", "I", f"synced {len(await self.tree.sync())} command(s)")
            await furfag.firLoggers("DISCORD", "I", f"login took {self.latency:.2f} seconds")
            ##############################################################################
            self.syffyserver = self.get_guild(furfag.config["guild-ids"]["main_server"])
            self.syffycache = self.get_guild(furfag.config["guild-ids"]["cache_server"])
            self.syffycache2 = self.get_guild(furfag.config["guild-ids"]["icon_server"])
            self.zekrom_channel = self.get_channel(furfag.config["channel-ids"]["zekrom_channel"])
            self.zekrom_diary = self.get_channel(furfag.config["channel-ids"]["zekrom_error_channel"])
            ##############################################################################
            self.ZEF2 = Zekrom_Extra_Functions_2
            ##############################################################################
            self.reshiram_emoji = f"{await self.fetch_application_emoji(1369695170722795530)}"
            self.thefogiscoming = f"{discord.utils.get(self.syffyserver.emojis, name='thefogiscoming')}"
            ##############################################################################
            if self.syffyserver and self.syffycache and self.syffycache2:
                await furfag.firLoggers("DISCORD", "I", f"successfully loaded syffyserver ({self.syffyserver}), syffycache ({self.syffycache}) and syffyicons ({self.syffycache2})")
            else:
                await furfag.firLoggers("DISCORD", "E", f"couldn't load {'syffy' if self.syffyserver is None else 'syffycache' if self.syffycache is None else 'syffyicons' if self.syffycache2 is None else None}.")
            if self.guilds:
                for s in self.guilds:
                    if not os.path.exists(os.path.join(self.server_path, str(s.id))):
                        os.mkdir(os.path.join(self.server_path, str(s.id)))

            if furfag.config["settings"]["status_override_enabled"] is True:
                await self.change_presence(status=discord.Status.do_not_disturb, activity=discord.CustomActivity(name=furfag.config["status-config"]["status_override"]))
                await furfag.firLoggers("DISCORD", "W",  f"status overridden: {furfag.config["status-config"]["status_override"]}")
            else:
                self.loop.create_task(self.cycle_status(), name='reshiram_status_cycle')

        except Exception as e:
            await furfag.firLoggers("DISCORD", "E", f"an error occoured during finalization phase, {e}")

        finally:
            tasks = asyncio.all_tasks()
            for task in tasks:
                task.set_name(task.get_coro().__qualname__)

            task_names = [(t.get_name()) for t in tasks]
            task_names_formatted = ', '.join(task_names)
            await furfag.firLoggers("SYSTEM", "I",  f"running threads: {task_names_formatted}")
            elapsed = furfag.firTimers.stop('startup')
            await furfag.firLoggers("TIMER", "I", f"discord bot took {elapsed:.2f} seconds to fully set up")

    async def the_cog_is_coming(self):
        cog_files = [file for file in os.listdir(os.path.join(furfag.client_root, 'cogs')) if file.endswith('.py')]
        for file in cog_files:
            await self.load_extension(f'cogs.{file[:-3]}')
        await furfag.firLoggers("DISCORD", "I", f"the cog is coming. (loaded {len(cog_files)} cogs)")

    async def zekrodirs(self):
        ##############################################################################
        self.server_path = os.path.join(furfag.client_dir, 'servers')
        self.assets_path = os.path.join(furfag.client_dir, 'assets')
        self.cache_path = os.path.join(furfag.client_dir, 'cache')
        self.logs_path = os.path.join(furfag.client_dir, 'logs')
        ##############################################################################
        self.server_icons = os.path.join(self.cache_path, f'server-icons')
        ##############################################################################
        tree_list = [
            self.server_path,
            self.assets_path,
            self.cache_path,
            self.logs_path,
            self.server_icons
            ]
        await furfag.firHelpers.directory_manager(tree_list=tree_list)

    async def setup_logs(self):
        @staticmethod
        def clear_log_file(path):
            with open(path, 'w', encoding='utf-8'):
                pass
        ##############################################################
        discordlog = os.path.join(self.logs_path, "discord.log")
        systemlog = os.path.join(self.logs_path, "system.log")
        ##############################################################
        if furfag.config["settings"]["clear_logs_on_startup"] is True:
            clear_log_file(discordlog)
            clear_log_file(systemlog)
        ##############################################################
        logging.captureWarnings(True)
        ########################################################################################################
        discord_logger = logging.getLogger('discord')
        discord_logger.setLevel(logging.INFO)
        discord_handler = logging.handlers.RotatingFileHandler(
            filename=discordlog,
            encoding='utf-8',
            maxBytes=32 * 1024 * 1024,
            backupCount=5
        )
        discord_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        discord_logger.addHandler(discord_handler)
        ########################################################################################################
        system_logger = logging.getLogger()
        system_logger.setLevel(logging.DEBUG)
        system_handler = logging.handlers.RotatingFileHandler(
            filename=systemlog,
            encoding='utf-8',
            maxBytes=32 * 1024 * 1024,
            backupCount=5
        )
        system_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        system_logger.addHandler(system_handler)
        ########################################################################################################

    async def cycle_status(self):
        await furfag.firLoggers("DISCORD", "I", f"cycle_status has been started")
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
            await furfag.firLoggers("DISCORD", "I", f"status changed: {r_status["name"]}, {r_activity["name"]}, {r_text}")
            await asyncio.sleep(self.status_cycle_wait_time)

    class ErrorHandler(app_commands.CommandTree):
        async def on_error(self, interaction: discord.Interaction, error: Exception):
            if isinstance(error, app_commands.AppCommandError):
                await furfag.firLoggers("DISCORD", "E", f"app command error:\n{error}")
            elif isinstance(error, app_commands.CommandSyncFailure):
                await furfag.firLoggers("DISCORD", "E", f"command sylc failure:\n{error}")
            else:
                await   ("DISCORD", "E", f"unknown error occoured:\n{error}")

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
            self.loop.run_until_complete(Zekrom.FuckassAsyncioWrapper.run_parallel(
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

if __name__ == "__main__":
    with Zekrom.FuckassAsyncioWrapper() as a:
        Zekrofag = Zekrom(a.session) # a.session
        a.spawn(furfag.firHelpers.handle_printers_queue())
        a.spawn(furfag.firHelpers.handle_ffc())
        a.run(Zekrofag.start(furfag.firHelpers.get_discord_bot_token()))