from components.Zekrom_Furfag import furfag
import discord
import asyncio
import random
import aiohttp
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
from pathlib import Path

class Zekrom(commands.Bot):
    def __init__(self, aiohttpsession):
        super().__init__(
            application_id=1311376747132092426,
            assume_unsync_clock=False,
            command_prefix=furfag.config["trigger-words"]["prefixes"],
            description="I'm NOT such a gay little faggot >w<",
            intents=discord.Intents.all(),
            shard_id=420,
            status=discord.Status.dnd,
            strip_after_prefix=True,
            tree_cls=self.ErrorHandler,
            )
        self.token = furfag.config["super-duper-awesome-config"]["token"]
        self.zesshion = aiohttpsession # resshion was the best thing i came up with since firLoggers
        self.activated = False
        self.zekroplus = self.ZekromPlus(self)
        furfag.firTimers.start('startup')

    async def startup(self):
        # start a login timer
        furfag.firTimers.start('login')
        # log into discord
        await self.login(Zekrofag.token)
        # connect to discord
        await self.connect()

    async def wait_for_zekrofag(self):
        # define paths
        await self.zekroplus.zekropaths()
        # create directories
        await self.zekroplus.zekrodirs()
        # load files
        await self.zekroplus.zekrofiles()

        # wait for client
        await furfag.firLoggers("DISCORD", "W", "Logging into Discord...", end='\r')
        await self.wait_until_ready()
        await furfag.firLoggers("DISCORD", "I", f"Logged in as \x1b[35m{self.user.name}~", furfag.firTimers.stop('login'))

        # sync cogs
        await self.zekroplus.the_cog_is_coming()
        # running tasks?
        await self.zekroplus.get_running_tasks()
        # ready
        await furfag.firLoggers("SYSTEM", "I", f"{furfag.client} is fully set up and ready to go~", furfag.firYappers.ready)
        self.activated = True
        self.error_view = View()

    async def status_cycle(self):
        while self.activated is False:
            await asyncio.sleep(1)
        await furfag.firLoggers("SYSTEM", "D", f"cycle_status has been started")
        while self.activated is True:
            await self.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.streaming,name='deez nuts', url='https://www.twitch.tv/lucariofucker'))
            await asyncio.sleep(random.randint(10, 3600))

    class ZekromPlus:
        def __init__(self, reshifag):
            self.bot = reshifag

        def __getattr__(self, name):
            return getattr(self.bot, name)

        async def zekropaths(self):
            self.bot.servers_path = Path(furfag.client_dir).joinpath('servers')
            self.bot.cache_path = Path(furfag.client_dir).joinpath('cache')
            self.bot.logs_path = Path(furfag.client_dir).joinpath('logs')
            self.bot.components_dir = Path(furfag.client_root).joinpath('components')
            self.bot.cogs_dir = Path(furfag.client_root).joinpath('cogs')

        async def zekrodirs(self):
            tree_list = [
                self.bot.components_dir,
                self.bot.cogs_dir,
                self.bot.servers_path,
                self.bot.cache_path,
                self.bot.logs_path,
                ]
            await furfag.firHelpers.directory_manager(tree_list=tree_list)

        async def zekrofiles(self):
            self.bot.cog_files = [Path(file).name for file in Path(self.bot.cogs_dir).iterdir() if Path(file).suffix == '.py']

        async def the_cog_is_coming(self):
            if furfag.config["debug-settings"]["load_cogs"] is True:
                for file in self.bot.cog_files:
                    await self.bot.load_extension(f'cogs.{file[:-3]}')
                await furfag.firLoggers("DISCORD", "I", "the cog is coming.", f'loaded {len(self.bot.extensions.keys())} cogs')
            if furfag.config["debug-settings"]["sync_commands"] is True:
                await furfag.firLoggers("DISCORD", "I", f"synced {len(await self.bot.tree.sync())} command(s)")

        async def get_running_tasks(self):
            tasks = asyncio.all_tasks()
            for task in tasks:
                new_name = task.get_coro().__qualname__
                task.set_name(new_name)
                await furfag.firLoggers("SYSTEM", "D",  f"running threads: {task.get_name()}", end='\r')

            task_names = [(t.get_name()) for t in tasks]
            task_names_formatted = ', '.join(task_names)
            await furfag.firLoggers("SYSTEM", "D",  f"running threads: {task_names_formatted}")

    class ErrorHandler(app_commands.CommandTree):
        async def on_error(self, interaction: discord.Interaction, error: Exception):
            try:
                if isinstance(error, app_commands.AppCommandError):
                    if isinstance(error, app_commands.CommandInvokeError):
                        await furfag.firLoggers("DISCORD", "E", "app_command is being a bitch.", error)
                    elif isinstance(error, app_commands.TransformerError):
                        await furfag.firLoggers("DISCORD", "E", "#TransRights", error)
                    elif isinstance(error, app_commands.TranslationError):
                        await furfag.firLoggers("DISCORD", "E", "ching chang chong", error)
                    elif isinstance(error, app_commands.CommandAlreadyRegistered):
                        await furfag.firLoggers("DISCORD", "E", "that command already exists. dumbass.", error)
                    elif isinstance(error, app_commands.CommandNotFound):
                        await furfag.firLoggers("DISCORD", "E", ":firHUH:", error)
                    elif isinstance(error, app_commands.CommandLimitReached):
                        await furfag.firLoggers("DISCORD", "E", "what are you doing adding so many commands", error)
                    elif isinstance(error, app_commands.CommandSignatureMismatch):
                        await furfag.firLoggers("DISCORD", "E", "upgrade from http to hhtps", error)
                    elif isinstance(error, app_commands.CheckFailure):
                        await furfag.firLoggers("DISCORD", "E", "check failure? check deez nuts", error)
                        if isinstance(error, app_commands.NoPrivateMessage):
                            await furfag.firLoggers("DISCORD", "E", "do NOT take ts to dms 😭🙏", error)
                        elif isinstance(error, app_commands.MissingRole):
                            await furfag.firLoggers("DISCORD", "E", "missing the 'based' role", error)
                        elif isinstance(error, app_commands.MissingAnyRole):
                            await furfag.firLoggers("DISCORD", "E", "missing all the roles", error)
                        elif isinstance(error, app_commands.MissingPermissions):
                            await furfag.firLoggers("DISCORD", "E", "hey! you can't do that! >:c", error)
                        elif isinstance(error, app_commands.BotMissingPermissions):
                            await furfag.firLoggers("DISCORD", "E", "hey! I can't do that! >:c", error)
                        elif isinstance(error, app_commands.CommandOnCooldown):
                            await furfag.firLoggers("DISCORD", "E", "s-slow down senpai..~", error)
                        else:
                            await furfag.firLoggers("DISCORD", "E", "uhm ermmm uhh idk >~<", error)
                    else:
                        await furfag.firLoggers("DISCORD", "E", "app_command error. nice one buddy.", error)
                elif isinstance(error, app_commands.CommandSyncFailure):
                    await furfag.firLoggers("DISCORD", "E", f"couldn't sync commands AUASGHUASDGHSDIOHB", error)
                else:
                    await furfag.firLoggers("DISCORD", "E", f"unknown error. dunno how to feel about that.", error)
            finally:
                interaction.client.error_view.clear_items()

                async def report_error(interaction):
                    interaction.client.error_view.remove_item(report_button)
                    await interaction.client.reshiram_err_rep.send(f'Error Report: {error}')
                    await interaction.response.edit_message(view=interaction.client.error_view)

                error_author=(f"{random.choice(furfag.config["miscellaneous"]["error_responses"])}", "", f"")
                error_body=(f"{interaction.client.reshiram_badge}", "", "", 0x781313)
                error_fields=[("an error occoured", f"{error}", False)]
                error_images=("", f"{random.choice(furfag.config["miscellaneous"]["error_images"])}")
                error_footer=(f"❌ • Interaction Failed", "")

                report_button = Button(label='Report Error', style=discord.ButtonStyle.blurple)
                report_button.callback = report_error
                interaction.client.error_view.add_item(report_button)

                error_embed = await interaction.client.REF2.Webhook_Maker(error_author, error_body, error_fields, error_images, error_footer)
                if interaction.response.is_done():
                    await interaction.edit_original_response(embed=error_embed, view=interaction.client.error_view)
                elif not interaction.response.is_done():
                    await interaction.response.send_message(embed=error_embed, view=interaction.client.error_view)
                else:
                    await interaction.followup.send(embed=error_embed, view=interaction.client.error_view)


class FuckassAsyncioWrapper:
    # with ris(leaking) as husband: frot() * 300
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.session = None

    def spawn(self, task, name: str = None):
        """for running in the bg"""
        self.loop.create_task(task, name=name)

    def run(self, *tasks):
        """for running and awaiting, if multiple provided they run in parallel"""
        self.loop.run_until_complete(self.main(
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

    #@staticmethod
    async def main(self, *tasks):
        await furfag.firLoggers("SYSTEM", "I", "Started!")
        await asyncio.gather(*tasks)

    def __enter__(self):
        self.session = self.loop.run_until_complete(self._create_session())
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.run(furfag.spitefox_shutdown())
        self.kms()

    async def _create_session(self):
        return aiohttp.ClientSession()

if __name__ == "__main__":
    with FuckassAsyncioWrapper() as a:
        Zekrofag = Zekrom(a.session)
        a.run(
            furfag.firLoggers.firLoggers_queue_handler(),
            furfag.firLoggers.furfag_colours_updater(),
            Zekrofag.startup(),
            Zekrofag.wait_for_zekrofag(),
            Zekrofag.status_cycle(),
        )