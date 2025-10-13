import os, sys; reshiram_arguments = sys.argv
from spitefox.bootstrap import (
    spitefox_bootstraplogger as spf_logger,
    spitefox_invenv as spf_isv,
    spitefox_error_handler as spf_erro,
    spitefox_installdeps as spf_insdp,
    spitefox_directorymanager as spf_dirmng
)
if spf_isv() is False:
    os.system("call start.bat")
    spf_erro(ValueError("not running in venv"))
    exit()
######################
os.system("call .venv\\Scripts\\activate.bat")
spf_dirmng(directories=['.venv', 'cogs', 'components', 'data'], headers={"mode":"relative", "root_dir":__file__})
spf_insdp(dependencies=['discord', 'aiohttp', 'aiofiles', 'asyncpraw', 'pydub', 'tkinter', 'pillow', 'keyboard', 'pywin32', 'pygame', 'translate'], issuer='Reshiram')
######################################################################################################################################################################

###########################################
from components.Reshiram_Commons import RCI
os.system("cls")
RCI.firLockers.acquire_lock()
###########################################
import asyncio

import ctypes

import discord

import json

import keyboard

import random

import shutil

import threading
import time
###########################################


########################
from components import (
    Reshiram_Manager as Reshiram_Manager,
    Reshiram_Voicemessage_Handler as Reshiram_Voicemessage_Handler,
    Reshiram_Extra_Functions_Squared as REF2
)
from datetime import (
    datetime,
    timezone,
    timedelta
)
from discord import (
    app_commands,
)
from discord.ext import (
    commands
)
from discord.ui import (
    Button,
    View
)
from discord.errors import *
from pathlib import (
    Path
)
from translate import (
    Translator
)
########################

class Reshiram:
    """
        ⠀⠀⠀⠀⠀⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⣸⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⢻⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣠⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⡀⠴⣾⣿⣿⣿⣤⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀⠀⠀⣀⣤⣾⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣀⠀⠀⣤⣾⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⣿⢸⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⢻⣿⣿⡿⠿⠟⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣌⣃⣼⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⢀⣠⣤⣴⣿⣿⣍⣠⣶⣶⣶⣦⡈⢻⣿⣿⣿⣿⣿⣿⡿⠟⠋⠉⠋⠉⠛⢿⣿⣿⣿⣿⣿⠅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠈⠛⠛⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⠾⠿⣿⣿⣿⣿⣿⣤⣴⣶⣿⣿⣷⣶⣀⢹⣿⣿⣤⣶⣶⡶⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⣰⣯⣛⣉⢩⡟⠟⢿⣿⣿⣦⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⢰⠿⠿⠟⠳⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣍⣀⡤⠀⠝⢉⣹⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⠿⣿⣿⣦⣉⣡⣬⣙⣁⣼⣿⣿⣿⣿⣿⣿⣷⠾⠟⠻⢿⡿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢉⣹⣿⣿⣿⣿⣿⣿⣿⣉⣉⣭⣍⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⠿⣷⣾⣿⣿⣿⣿⣿⣿⡿⠟⣓⣈⣅⣙⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⡟⢋⣤⣴⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠾⠿⢿⣿⣿⣿⠏⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣦⠹⡇⣾⣿⣧⢹⣿⡿⠛⢻⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡆⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣶⣤⣀⣉⣁⠈⠠⣤⣶⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⣆⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡄⠀⢰⣿⣿⣧⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣧⢹⣿⣿⣿⣆⢻⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣧⠀⣾⣿⣿⣿⣧⡀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⣿⣿⣿⣿⣿⣿⡈⢿⣿⣿⣿⣦⣙⠛⠛⢋⡁⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣰⣿⣿⣿⣿⣿⣷⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⢀⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣁⡀⠀⠀⠀⠀⣀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⢰⣿⣿⣿⣿⣿⣿⣿⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⢡⣠⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
        ⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⡄⢽⣿⣿⣿⣿⣿⣿⢌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇
    """
    def __init__(self):
        ####################################### root dir/file
        self.client = Path(__file__).absolute()
        self.client_root = Path(__file__).parent.absolute()
        ################################################### firSuite instances
        self.firLoggers = RCI.firLoggers
        self.firHelpers = RCI.firHelpers
        self.firTimers = RCI.firTimers
        self.firYappers = RCI.firYappers
        self.firWhiskers = RCI.firWhiskers
        ################################## vars
        self.activated = False
        self.cache_finished = False
        self._channel = None
        self.errors = []
        ############################################################# dirs
        self.venv_dir = self.client_root.joinpath('.venv').absolute()
        self.assets_dir = self.client_root.joinpath('assets').absolute()
        self.cogs_dir = self.client_root.joinpath('cogs').absolute()
        self.components_dir = self.client_root.joinpath('components').absolute()
        self.data_dir = self.client_root.joinpath('data').absolute()
        ################################################################################ asyncio loops
        self.main_loop = asyncio.new_event_loop(); asyncio.set_event_loop(self.main_loop)
        # self.background_loop = asyncio.new_event_loop(); asyncio.set_event_loop(self.background_loop)
        ####################################### component instances
        self.bot = ReshiramBot(self)
        self.reshiplus = ReshiramPlus(self)
        self.keyboard = ReshiramKeyboard(self)
        self.trans = "?" # I've no idea what goes here the line was empty when I opened the file
        ######################################
        self.reshithreadMain = threading.Thread(target=self._reshiram_thread, daemon=True, name='ReshiramThread')
        self.reshithreadKeyboard = threading.Thread(target=self._reshiram_keyboard_thread, daemon=True, name='ReshiramKeyboardThread')
        ############################################################

    def start(self):
        """starts reshiram(yeah)"""
        os.system("title Reshiram: starting")
        self.firLoggers("SYSTEM", "I", "Awakening the creature...", fc_issync=True)
        try:
            self.reshithreadMain.start()
            self.reshithreadKeyboard.start()
            self.main_loop.run_forever()
        except Exception as e:
            self.firLoggers("SYSTEM", "E", "keyboard interrupt received, shutting down...", fc_iss_override='matrix', fc_cls_override='Reshifag', fm_error=e, fc_issync=True)
        except KeyboardInterrupt:
            self.firLoggers("SYSTEM", "E", "keyboard interrupt received, shutting down...", fc_iss_override='matrix', fc_cls_override='Reshifag', fc_issync=True)
            self.stop()
        except BaseException:
            self.stop()

    def stop(self):
        """stops reshiram(shuts down threads and releases lockfile)"""
        try:
            asyncio.run_coroutine_threadsafe(self.bot.change_presence(status=discord.Status.dnd,activity=discord.CustomActivity(name="💤 shutting down...")), self.main_loop)
            os.system("title Reshiram: stopping")
            self.firLoggers("%CLIENT%", "W", "Reshiram: Deactivated", fc_issync=True)
            self.firLoggers("SYSTEM", "E", "error recap:", fm_list=self.errors, fc_issync=True) if len(self.errors) >= 1 else self.firLoggers("SYSTEM", "I", "no errors found!", fc_issync=True)
            while self._channel is not None and self._channel.get_busy():
                time.sleep(0.0001)
            asyncio.run_coroutine_threadsafe(self.bot.close(), self.main_loop)
            time.sleep(1)
            self.firLoggers.killFirLoggers()
            shutil.copy2(src=self.client_root.joinpath("Reshiram.log").absolute(), dst=self.logs_dir.joinpath(f"Reshiram-{len([past_log for past_log in self.logs_dir.iterdir()])}.log").absolute())
            self.main_loop.call_soon_threadsafe(self.main_loop.stop)
        except Exception as e:
            spf_erro(e)
            print("retrying shutdown..."); time.sleep(2)
            self.stop()
        except BaseException:
            exit()

    async def main(self):
        """the main function where MainThread is gonna run, waits until self.activated is set to True"""
        await self.firLoggers("%CLIENT%", "I", "Reshiram: Starting")
        try:
            await self.main_setup()
            self.firYappers.play(self.assets_dir.joinpath('snd_icespell.ogg'), volume=0.1)
            await asyncio.gather(self.bot.startup(), self.bot.wait_for_reshifag(), self.bot.setup_unhook())
        except Exception as WARNING:
            await self.reshiplus._error_handler(error=WARNING)
        except BaseException:
            spf_logger("CRITICAL ERROR")
            self.stop()

    async def main_setup(self):
        try: # directories
            await self.reshiplus.expose_the_reshifiles()
        except OSError as VAR_ERROR:
            await self.reshiplus._error_handler(error=VAR_ERROR)
        try: # configs
            self.firLoggers.startFirLoggers()
            await self.reshiplus.load_config()
        except Exception as CONF_ERROR:
            await self.reshiplus._error_handler(error=CONF_ERROR)
        try: # session stuff
            self.RWR = REF2.Reshiram_Web_Requests();await self.RWR.setup()
            self.RMR = REF2.Reshiram_Mcss_Requests();await self.RMR.setup()
            self.RAR = REF2.Reshiram_Any_Requests();await self.RAR.setup()
        except Exception as WEB_ERROR:
            await self.reshiplus._error_handler(error=WEB_ERROR)
        try:
            self.firTimers.start('cache_builder')
            self.main_loop.create_task(self.cache_handler())
        except Exception as CACHE_ERROR:
            await self.reshiplus._error_handler(error=CACHE_ERROR)
        try:
            await self.firLoggers("SYSTEM", "W", "waiting for cache creation...")
            while self.cache_finished is False:
                await asyncio.sleep(1)
            await self.daily_coffee()
            await self.firLoggers("SYSTEM", "W", "cache builder finished", fm_timer=self.firTimers.stop('cache_builder'))
            self.activated = True
        except TypeError as NOT_SESSION:
            await self.reshiplus._error_handler(error=NOT_SESSION)


    async def daily_coffee(self):
        try:
            coffee_data = self.coffees
            coffee_today = coffee_data[datetime.now().day]
            await self.firLoggers("SYSTEM", "I", f"today's coffee: {coffee_today.get("title")}, {self.trans.translate(coffee_today.get("description"))}")
        except Exception as COFFEE_ERROR:
            await self.reshiplus._error_handler(error=COFFEE_ERROR)

    def _reshiram_thread(self):
        self.firLoggers("SYSTEM", "I", "Reshiram Thread Started!", fc_issync=True)
        asyncio.run_coroutine_threadsafe(self.main(), self.main_loop)

    def _reshiram_keyboard_thread(self):
        self.firLoggers("SYSTEM","I",f"escape-thread running, press [{self.keyboard._escapekey}] {self.keyboard._escapecount} times to exit the script", fc_issync=True)
        while self.keyboard._escaped is False:
            keyboard.on_press_key(self.keyboard._escapekey, self.keyboard._pressed_callback)
            keyboard.wait()
        self.firLoggers("SYSTEM","I",f"bah bah bah", fc_issync=True)

class ReshiramBot(commands.AutoShardedBot):
    """
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠛⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠛⢠⡀⠸⣆⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⡁⢰⣋⡇⠀⡿⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠁⣏⠉⠛⠳⢤⣟⠀⢧⠀⠀⣀⣤⣠⣤⣄⣀⠀⠀⢷⠀⠀⠈⠙⠢⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡔⠃⣀⠘⢆⣀⠀⠀⠉⠀⠘⠚⠉⠀⠀⢀⡀⠀⢸⠇⣀⢸⡀⠀⠀⠀⠀⠈⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⠙⡾⠟⣷⠂⠉⠀⠀⠀⠀⠀⠀⠀⢶⢚⣹⠃⢠⡏⠀⡏⠹⠃⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣼⠇⣰⠀⠀⠀⠠⠶⠳⣦⠀⠀⠀⠘⠲⠃⢠⠟⠁⠀⡏⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠈⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠏⡟⠷⠟⠁⠀⠀⣴⡆⠀⢸⡇⠀⠀⢠⣄⡴⠏⠀⡀⢰⠇⠀⠀⠀⠀⠀⠀⢠⡾⠚⠋⠉⠉⢳⡀⠀⠀⠀⠀⠀
        ⠀⢹⡌⠙⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⢧⡐⠶⠄⠀⠀⠻⣃⡀⠸⡷⠀⠀⠀⠹⣆⠀⢀⡿⡏⠀⠀⠀⠀⠀⠀⣠⡾⠀⠀⠀⢀⡴⠟⠁⠀⠀⠀⠀⠀
        ⠀⠀⢷⠀⠀⠻⣷⣄⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠙⠦⣤⣀⡀⠀⠘⠿⠇⠀⣤⠴⣶⣞⣁⣠⣾⡀⠀⠀⣤⣠⣴⠶⢾⣁⣧⠀⠀⠀⠈⢧⡤⠖⠚⠦⣄⡀⠀
        ⠀⠀⠘⡇⠀⠀⠈⠻⣷⡀⠀⠀⣠⢾⡉⢉⡍⠙⠳⣶⢟⣯⣭⠿⠷⣤⡀⣠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠛⠚⠻⠀⠀⠀⠀⠈⣇⠀⠀⠀⠀⠙⣦
        ⠀⠀⠀⢹⡀⠀⠀⠀⢿⣧⠀⠀⢧⣸⡀⠘⣇⣴⠀⠀⢘⠛⠛⠀⣰⠊⠻⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣤⣄⣄⡓⣶⠏
        ⠀⠀⠀⠀⣧⠀⠀⠀⠈⣿⣆⣠⣤⣭⡭⠿⣹⣿⡋⠉⠛⠓⠒⠴⠃⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣇⠈⠙⠛⠁⠀
        ⠀⠀⠀⠀⠈⠳⣄⠀⠀⠸⣿⠉⠀⠈⢻⠞⠙⡾⠁⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣀⣀⣀⣀⣀⣀⣀⣬⠷⠶⠤⢤⣤⣄⣀⣀⣤⣄⡀⣰⠤⢽⠆⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠈⠳⣄⠀⢿⣧⠀⠀⠘⠷⠾⠷⣼⣅⣀⣀⠀⠀⠀⠀⠀⠀⠸⡅⠀⠀⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠏⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠘⢧⡈⡿⣄⣀⣀⣀⣀⣀⣈⣳⣍⠉⠉⠛⢿⡛⢦⡼⠛⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⠻⠶⠿⠿⠷⠷⠿⠿⠾⠶⠶⠶⠶⠿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """
    def __init__(self, reshifag):
        self.fag = reshifag
        self.fag.firLoggers("SYSTEM", "I", "Reshiram-Bot initialized", fc_issync=True)
        self.activated = False
        self.message_log = []
        self.cog_autocomplete_cache = [{"name": Path(file).stem.replace('_', ' ').title(),"value": Path(file).stem} for file in Path(self.fag.cogs_dir).iterdir() if Path(file).suffix == '.py']

    async def startup(self):
        """initiates the connection to discord"""
        # start a timer
        self.fag.firTimers.start('login')
        # super init
        super().__init__(
            application_id=1265643551023169611,
                assume_unsync_clock=False,
                    command_prefix=self.config.get("trigger-words").get("prefixes"),
                        description="I'm such a gay little faggot >w<",
                            intents=discord.Intents.all(),
                                status=discord.Status.dnd,
                                    activity=discord.CustomActivity(name="hello world! starting up..."),
                                        strip_after_prefix=True,
                                            help_command=None,
                                                tree_cls=self.Reshiram_Command_Tree)
        # get the token
        self.token = await self.fag.reshiplus._get_bot_token()
        # log into discord
        await self.login(self.token)
        # connect to discord
        await self.connect()

    async def wait_for_reshifag(self):
        """waits for the bot to finish the log-in process, basically acts as a login-timeout-wrapper"""
        await self.fag.firLoggers("DISCORD", "W", "Logging into Discord...")
        await asyncio.wait_for(self.wait_until_ready(), timeout=10)
        await self.fag.firLoggers("DISCORD", "I", f"Logged in as \x1b[35m{self.user.name}~", fm_timer=self.fag.firTimers.stop('login'), fm_tupl=(f"Shard-ID: {self.shard_id}", f"SHARDs: {self.shard_count}"))
        await self.change_presence(status=discord.Status.idle, activity=discord.CustomActivity(name="almost there..."))
        self.activated = True

    async def setup_unhook(self): # these methods aren't as critical and can(should) wait until the bot is ready
        while self.activated is False:
            await asyncio.sleep(1)
        try:
            self.vmm = Reshiram_Voicemessage_Handler.VoiceMessageManager(self.http)
            self.message_log_path = self.fag.logs_dir.joinpath(f"message_log-{datetime.now()}.json")
            self.servers_dir = self.fag.data_dir.joinpath('servers')
            reshiram_tree = [
                self.servers_dir,
                ]
            spf_dirmng(directories=reshiram_tree, headers={"mode":"absolute","root_dir":"None"})
            await self.fag.firLoggers("DISCORD", "D", "waiting for client login...")
            while self.activated is False:
                await asyncio.sleep(1)
            await self.fag.firLoggers("DISCORD", "D", "finishing setup...")
            # update status
            await self.change_presence(status=discord.Status.idle, activity=discord.CustomActivity(name='almost there...'))
            # define variables
            await self.fag.reshiplus.reshivars()
            # final destination
            await self.fag.reshiplus.final_destination()
            self.activated_full = True
            self.loop.create_task(self._status_cycle())
        except Exception as CFG_WARNING:
            await self.fag.reshiplus._error_handler(error=CFG_WARNING)

    async def _status_cycle(self):
        """cycles or overrides the status of the bot, waits for the `self.activated` flag to be True before doing so"""
        async def status_cycle_override(headers:dict=None):
            enabled = headers.get("enabled")
            index = headers.get("index")
            statuses = headers.get("statuses")
            status = headers.get("statuses")[index]
            if index == 0: # default
                await self.change_presence(status=discord.Status.idle, activity=discord.CustomActivity(name=f'status override is enabled! this is the default override message. configure additional messages in the config'))
            elif index == 1: # 1 = deltarune tommorow
                if await self.fag.reshiplus.is_deltarune_out_yet() is False: # deltarune isn't out yet
                    release_datetime = datetime(2025, 6, 4, 15, 0, 0, tzinfo=timezone.utc)
                    seconds_until_release = (release_datetime - datetime.now(timezone.utc)).total_seconds()
                    when_does_deltarune_finally_release = await self.reshiplus.deltarune_when(seconds_until_release)
                    release_timestamp = int(release_datetime.timestamp())
                    await self.reshiram_channel.send(f'GUys!! DELTARUNE <t:{release_timestamp}:R>')
                    await self.change_presence(status=discord.Status.do_not_disturb, activity=discord.CustomActivity(name=f'deltarune in {when_does_deltarune_finally_release}'))
                else:
                    await self.reshiram_channel.send(f'GUys!! DELTARUNE OUT NOW!! ``https://deltarune.com``')
                    await self.change_presence(status=discord.Status.do_not_disturb, activity=discord.CustomActivity(name=f'deltarune today | deltarune.com'))
            else: # everything else
                await self.change_presence(status=discord.Status.idle, activity=discord.CustomActivity(name=status))
            await self.fag.firLoggers("DISCORD", "D", f"status overriden: {status}")
        async def status_cycle_loop():
            while True:
                try:
                    RESHI_STATUS = random.choice(list(self.config.get("status-config").get("types").values())) # returns something like 'dnd', 'idle', etc
                    RESHI_STATUS = getattr(discord.Status, RESHI_STATUS.lower()) # convert to discord.Status (???) activity.type = awesome, uses integers, easy to understand, status = stupid, only accepts enums
                    RESHI_ACTIVITY = random.choice(list(self.config.get("status-config").get("random").values()))
                    RESHI_ACTIVITY_NAME, RESHI_ACTIVITY_TYPE = RESHI_ACTIVITY.get("discord")[0], RESHI_ACTIVITY.get("discord")[1]
                    RESHI_TEXT = random.choice(RESHI_ACTIVITY.get("statuses"))
                    if RESHI_ACTIVITY_NAME == 'custom':
                        await self.change_presence(status=RESHI_STATUS,activity=discord.CustomActivity(name=RESHI_TEXT))
                    else:
                        await self.change_presence(status=RESHI_STATUS,activity=discord.Activity(type=RESHI_ACTIVITY_TYPE,name=RESHI_TEXT, url='https://www.twitch.tv/lucariofucker'))
                except Exception as e:
                    return await self.fag.firLoggers("DISCORD", "E", f"failed to update status", fm_error=e)
                finally:
                    sleep_time = random.randint(10, 3600)
                    await self.fag.firLoggers("DISCORD", "D", f"status changed: {RESHI_STATUS}, {RESHI_ACTIVITY_NAME}, {RESHI_TEXT}", fm_str=f"sleeping for {timedelta(seconds=sleep_time)}")
                    await asyncio.sleep(sleep_time)
        await self.fag.firLoggers("SYSTEM", "D", f"cycle_status has been started")
        SO_headers = {
            "enabled": self.config.get("status_override_enabled"),
            "index": self.config.get("status_override_index"),
            "statuses": self.config.get("status-config").get("overrides")
            }
        if SO_headers.get("enabled") is True:
            await status_cycle_override(headers=SO_headers)
        else:
            await status_cycle_loop()


class ReshiramPlus:
    def __init__(self, reshifag):
        self.fag = reshifag
        self.bot = reshifag.bot
        self.fag.firLoggers("SYSTEM", "I", "ReshiramPlus initialized", fc_issync=True)

    async def _error_handler_discord(self, error:Exception, ctx_or_interaction):
        try:
            error_message = None
            if isinstance(error, ClientException):
                if isinstance(error, discord.InvalidData):
                    error_message = "DON'T LISTEN TO THE HATERS, DATA, YOUR VALID 💗"
                elif isinstance(error, discord.LoginFailure):
                    error_message = "LOGIN FAILURE :dface:"
                elif isinstance(error, discord.ConnectionClosed):
                    error_message = "DISCORD GATEWAY CLOSED FOR SOME REASON--FUCKASS LIBRARY"
                elif isinstance(error, discord.PrivilegedIntentsRequired):
                    error_message = "RESHIRAM IS CANONICALLY NOT A PRIVILEGED WHITE GUY"
                elif isinstance(error, discord.InteractionResponded):
                    error_message = "YOU ALREADY RESPONDED TO THAT INTERACTION. HEADASS."
                elif isinstance(error, discord.MissingApplicationID):
                    error_message = "IF YOU SEE MY ID, ID, ID, MORE THAN A PASSPORT, I'M UNIQUE 🎵"
                else:
                    error_message = "CLIENT??? EXCEPTION? ?? ?? ???? ???? ?? ? ??"
            elif isinstance(error, GatewayNotFound):
                error_message = "IM BLIND!! WHERES THE GATEWAY??"
            elif isinstance(error, HTTPException):
                error_message = "HTTP Request Failed"
            elif isinstance(error, RateLimited):
                error_message = "AAAAAAA WE ARE BEING RAPE LIMITED"
            elif isinstance(error, app_commands.AppCommandError):
                if isinstance(error, app_commands.CommandInvokeError):
                    error_message = "app_command is being a bitch."
                elif isinstance(error, app_commands.TransformerError):
                    error_message = "#TransRights"
                elif isinstance(error, app_commands.TranslationError):
                    error_message = "ching chang chong"
                elif isinstance(error, app_commands.CommandAlreadyRegistered):
                    error_message = "that command already exists. dumbass."
                elif isinstance(error, app_commands.CommandNotFound):
                    error_message = ":firHUH:"
                elif isinstance(error, app_commands.CommandLimitReached):
                    error_message = "what are you doing adding so many commands"
                elif isinstance(error, app_commands.CommandSignatureMismatch):
                    error_message = "upgrade from http to hhtps"
                elif isinstance(error, app_commands.CheckFailure):
                    error_message = "check failure? check deez nuts"
                    if isinstance(error, app_commands.NoPrivateMessage):
                        error_message = "do NOT take ts to dms 😭🙏"
                    elif isinstance(error, app_commands.MissingRole):
                        error_message = "missing the 'based' role"
                    elif isinstance(error, app_commands.MissingAnyRole):
                        error_message = "missing all the roles"
                    elif isinstance(error, app_commands.MissingPermissions):
                        error_message = "hey! you can't do that! >:c"
                    elif isinstance(error, app_commands.BotMissingPermissions):
                        error_message = "hey! I can't do that! >:c"
                    elif isinstance(error, app_commands.CommandOnCooldown):
                        error_message = "s-slow down senpai..~"
                    else:
                        error_message = "uhm ermmm uhh idk >~<"
                else:
                    error_message = "app_command error. nice one buddy."
            elif isinstance(error, app_commands.CommandSyncFailure):
                error_message = "couldn't sync commands AUASGHUASDGHSDIOHB"
            elif isinstance(error, commands.CommandError):
                if isinstance(error, commands.CommandNotFound):
                    error_message = "the fuck did you just say to me?"
                elif isinstance(error, commands.MissingRequiredArgument):
                    error_message = "what"
                elif isinstance(error, commands.MissingPermissions):
                    error_message = "hey! you can't do that! >:c"
                elif isinstance(error, commands.CommandOnCooldown):
                    error_message = f"s-slown down {ctx.author}-kun.. hngghh..."
                    retry_after_message = f"s-slown down {ctx.author}-kun.. hngghh... try again <t:{int(time.time() + error.retry_after)}:R>..."
                    await asyncio.sleep(error.retry_after)
                    await retry_after_message.delete()
                elif isinstance(error, commands.CommandRegistrationError):
                    error_message = f"command registration error(?)"
                else:
                    error_message = "erm, what the sigma..."
            elif isinstance(error, commands.ExtensionError):
                if isinstance(error, commands.ExtensionAlreadyLoaded):
                    error_message = "already loaded that extension. fucking idiot."
                elif isinstance(error, commands.ExtensionNotLoaded):
                    error_message = "didn't load that extension to begin with. can you do anything right?"
                elif isinstance(error, commands.NoEntryPointError):
                    error_message = "buddy. pal. friend. THERES NO ENTRYPOINT."
                elif isinstance(error, commands.ExtensionFailed):
                    error_message = "congratulations! your extension is a failure."
                elif isinstance(error, commands.ExtensionNotFound):
                    error_message = "keep looking boys, maybe we'll find out what goofy ahh extension boss is trying to load"
                else:
                    error_message = "extensoon error. alright pal."
            else:
                error_message = f"unknown error. dunno how to feel about that."
            if isinstance(ctx_or_interaction, discord.Interaction):
                interaction = ctx_or_interaction
                error_dict = {
                    "author": {
                        "name": f"{random.choice(interaction.client.config.get("miscellaneous").get("error_messages"))}",
                        "url": "",
                        "icon_url": "",
                    },
                    "body": {
                        "title": f"{interaction.client.reshiram_badge}",
                        "url": "",
                        "description": "",
                        "colour": 0x781313,
                    },
                    "images": {
                        "url": f"{random.choice(interaction.client.config.get("miscellaneous").get("error_images"))}",
                        "thumbnail_url": "",
                    },
                    "footer": {
                        "text": "❌ • AppCommand Failed",
                        "icon_url": ""
                    },
                    "fields": [
                        {"name": "an error occoured", "value": f"{error}", "inline": False}
                    ]
                }
                error_embed = await interaction.client.REF2.webhook_maker(headers=error_dict)
                if not interaction.response.is_done():
                    await interaction.response.send_message(content=error_message, embed=error_embed)
                elif interaction.response.is_done():
                    await interaction.edit_original_response(content=error_message, embed=error_embed)
                else:
                    await interaction.followup.send(content=error_message, embed=error_embed)
            elif isinstance(ctx_or_interaction, commands.Context):
                ctx = ctx_or_interaction
                error_dict = {
                    "author": {
                        "name": f"{random.choice(self.bot.config.get("miscellaneous").get("error_messages"))}",
                        "url": "",
                        "icon_url": "",
                    },
                    "body": {
                        "title": f"{ctx.bot.reshiram_badge}",
                        "url": "",
                        "description": "",
                        "colour": 0x781313,
                    },
                    "images": {
                        "url": f"{random.choice(self.bot.config.get("miscellaneous").get("error_images"))}",
                        "thumbnail_url": "",
                    },
                    "footer": {
                        "text": "❌ • Command Failed",
                        "icon_url": ""
                    },
                    "fields": [
                        {"name": "an error occoured", "value": f"{error}", "inline": False}
                    ]
                }
                error_embed = await self.bot.REF2.webhook_maker(headers=error_dict)
                await ctx.send(content=error_message, embed=error_embed)
            return error_message
        except Exception as e:
            raise ValueError(f"error in error handler--irony can be so painful. {e}")

    async def _error_handler(self, error:BaseException, interaction:discord.Interaction=None, ctx:commands.Context=None):
        if isinstance(error, Exception): # exceptions get handled
            if isinstance(error, TimeoutError):
                error_message = random.choice(self.fag.masterconfig.get("fun").get("taking_too_long"))
                error = TimeoutError("timed out")
                self.fag._channel = self.fag.firYappers.play(random.choice([TOOLONG for TOOLONG in self.fag.assets_dir.joinpath("TOO_LONG").iterdir()]))
            elif isinstance(error, DiscordException):
                error_message = await self._error_handler_discord(error=error, ctx_or_interaction=(interaction if interaction is not None else ctx if ctx is not None else None)) or "unknown error"
            elif isinstance(error, KeyError):
                error_message = "KEY ERROR 🔥"
            else:
                error_message = "Unknown Error"
        elif isinstance(error, BaseException): # base exceptions not LOL
            error_message = "you are not alone. help is available."
        await self.fag.firLoggers("%CLIENT%", "E", fl_message=error_message, fm_error=error, fc_iss_override='error_handler')
        self.fag.errors.append(f"{datetime.now().strftime("%H:%M:%S")} - {type(error)} - {error}")

    async def _get_bot_token(self):
        token_mode = self.fag.masterconfig.get("behaviour").get("token_mode")
        if token_mode == "CFG":
            token = self.bot.config.get("token")
        elif token_mode == "OS":
            token = self.fag.firWhiskers.spitevars.get("RESHIRAM_TOKEN")
        else:
            token = None
            await self._error_handler(KeyError(f"unknown token-mode '{token_mode}'"))
        return token

    async def expose_the_reshifiles(self):
        self.fag.persistent_dir = self.fag.data_dir.joinpath('.private').absolute()
        self.fag.cache_dir = self.fag.data_dir.joinpath('cache').absolute()
        self.fag.logs_dir = self.fag.data_dir.joinpath('logs').absolute()
        self.fag.config_path = self.fag.persistent_dir.joinpath('beta-config.json')
        self.bot.new_features_path = self.fag.persistent_dir.joinpath("new features.json")
        self.bot.pokemon_sprites_path = self.fag.cache_dir.joinpath("pokemon sprites.json")
        self.fag.coffee_path = self.fag.cache_dir.joinpath("coffee.json")
        reshiram_tree = [
            self.fag.assets_dir,
            self.fag.cogs_dir,
            self.fag.components_dir,
            self.fag.data_dir,
            self.fag.persistent_dir,
            self.fag.cache_dir,
            self.fag.logs_dir
        ]
        spf_dirmng(directories=reshiram_tree, headers={"mode":"absolute","root_dir":"None"})

    async def load_config(self):
        """
        Load Reshiram's config, creating it from backup if it doesn't exist
        `self.masterconfig` contains everything in the config file
        `self.config` contains just the config for Reshiram
        `self.bot.config` contains just the config for the Discord Bot
        """
        if not self.fag.config_path.exists():
            RCB = ReshiramCFGBackup()
            await RCB.backup()
            #os.system("python components\\Reshiram_Config_Backup.py")
        self.fag.masterconfig = await self.fag.firHelpers.aload(self.fag.config_path) or {}
        self.fag.config = self.fag.masterconfig.get("config")
        self.bot.config = self.fag.masterconfig.get("bot-config")
        await self.fag.firLoggers("SYSTEM", "I", f"loaded config for {self.fag.client.stem} - version {self.fag.masterconfig.get("meta").get("version")}")

    async def the_cog_is_coming(self):
        """handles cog(extension) loading and app_command syncing"""
        load_cogs = self.bot.config.get("load_cogs")
        sync_commands = self.bot.config.get("sync_commands")
        sync_to_guild_only = self.bot.config.get("sync_to_guild_only")
        if load_cogs is True:
            cogs = [Path(file).name for file in Path(self.fag.cogs_dir).iterdir() if Path(file).suffix == '.py' and not (file.name.startswith('_') or file.name.startswith('__'))]
            for cog in cogs:
                await self.bot.load_extension(f'cogs.{cog[:-3]}')
            await self.fag.firLoggers("DISCORD", "I", "the cog is coming.", fm_str=f'loaded {len(self.bot.extensions.keys())} cogs')
            await self.fag.firLoggers("DISCORD", "I", f"loaded {len(self.bot.commands)} command(s)", fm_list=[command.name for command in self.bot.commands])
        if sync_commands is True:
            if sync_to_guild_only is True:
                le_server = discord.Object(id=self.bot.config.get("guild-ids").get("stgo_server"))
                # app_commands = await self.bot.tree.sync(guild=discord.Object(id=self.bot.config.get("guild-ids").get("stgo_server")))
                self.bot.tree.copy_global_to(guild=le_server)
                await self.fag.firLoggers("DISCORD", "I", f"synced app command(s) to guild {le_server}")
            else:
                app_commands = await self.bot.tree.sync()
                await self.fag.firLoggers("DISCORD", "I", f"synced {len(app_commands)} app command(s)", fm_list=[app_command.name for app_command in app_commands])

    async def reshivars(self):
        self.bot.owner_id = self.bot.config["user-ids"]["user_avery"]
        self.bot.syffyserver = self.bot.get_guild(self.bot.config["guild-ids"]["main_server"])
        self.bot.syffycache = self.bot.get_guild(self.bot.config["guild-ids"]["cache_server"])
        self.bot.syffycache2 = self.bot.get_guild(self.bot.config["guild-ids"]["icon_server"])
        self.bot.reshiram_channel = self.bot.get_channel(self.bot.config["channel-ids"]["reshiram_channel"])
        self.bot.reshiram_diary = self.bot.get_channel(self.bot.config["channel-ids"]["reshiram_diary"])
        self.bot.reshiram_err_rep = self.bot.get_channel(self.bot.config["channel-ids"]["reshiram_error_report"])
        self.bot.reshiram_badge = f"{await self.bot.fetch_application_emoji(1361771372170314118)}{await self.bot.fetch_application_emoji(1361771381422817301)}{await self.bot.fetch_application_emoji(1361771390478454944)}{await self.bot.fetch_application_emoji(1361771404042833960)}{await self.bot.fetch_application_emoji(1361771414365143221)}{await self.bot.fetch_application_emoji(1361771422568939713)}{await self.bot.fetch_application_emoji(1361771429275894172)}"
        self.bot.reshiram_emoji = f"{await self.bot.fetch_application_emoji(1361772894127915269)}"
        self.bot.thefogiscoming = f"{discord.utils.get(self.bot.syffyserver.emojis, name='thefogiscoming')}"
        self.bot.REF = self.bot.get_cog('Extra Functions')
        self.bot.REF2 = self.bot.get_cog('Extra Functions²')
        self.bot.error_view = View()
        self.bot.message_log = []
        self.bot.server_configs = {}
        self.bot.server_members = {}
        self.bot.server_metas = {}

    async def final_destination(self):
        """final setup function to call"""
        #await self.open_manager_gui() if self.fag.config["behaviour"]["open_manager_gui_on_launch"] is True else None
        await self.fag.firLoggers("%CLIENT%", "I", f"{self.fag.client.stem} is fully set up and ready to go~")
        os.system("title Reshiram - Started!")
        await asyncio.sleep(5)
        os.system("title Reshiram")


class ReshiramKeyboard:
    """Reshiram Keyboard Listener, listenes for a key to be pressed multiple times in a row, the code is rly ugly so dont look at it too much ^~^"""
    def __init__(self, fag):
        self.fag = fag
        self.assets_dir = self.fag.client_root.joinpath('assets').absolute()
        self.firYappers = firSuite.firYappers()
        self.listening = True
        #########################################################################################################################
        self._timeout = 0.8
        ##################
        self._escaped = False
        self._escapekey = 'esc' # key to press
        self._escapecount = 5 # amount of times
        self._restartkey = 'ctrl'
        self._presstimes = [] # press times
        self._times_pressed = 0
        self._last_run = time.monotonic()
        self._esc_pressed = False
        ###############################
        self.timeout_thread = threading.Thread(target=self._timeout_thread, daemon=True, name='ReshiramTimeoutThread')
        self.timeout_thread.start()

    def logit(self, log_message, end):
        spf_logger(log_message=log_message, end=end, no_prefix=True)

    def _timeout_thread(self):
        while self._escaped is False:
            if self._esc_pressed is True:
                now = time.monotonic()

                if now - self._last_run >= self._timeout:
                    if random.randint(0, 100) < 25:
                        self.fag.firYappers.play(random.choice([TOOLONG for TOOLONG in self.fag.assets_dir.joinpath("TOO_LONG").iterdir()]), volume=random.random())
                        faggotini = random.choice(self.fag.masterconfig.get("fun").get("taking_too_long")) + "                                                                          "
                    else:
                        self.fag.firYappers.play(self.fag.assets_dir.joinpath("snd_battlefall.wav"))
                        faggotini = f"* you pressed [{self._escapekey}] {self._times_pressed} time(s)... but nothing happened."
                    self.logit(log_message=faggotini, end='\n')
                    self._last_run = now
                    self._esc_pressed = False
                    self._times_pressed = 0
            time.sleep(0.01)

    def _pressed_callback(self, event):
        if self._escaped is False:
            self.fag._channel = self.firYappers.play(self.assets_dir.joinpath('snd_noise.wav'))
            self._esc_pressed = True
            self._last_run = time.monotonic()
            self._times_pressed += 1
            now = time.time()
            self._presstimes = [t for t in self._presstimes if now - t <= self._timeout]
            self._presstimes.append(now)
            self._times_pressed = len(self._presstimes)
            self.logit(log_message=f"* you pressed [{self._escapekey}] {self._times_pressed} time(s)...", end='\r')
            if self._times_pressed >= self._escapecount:
                self._escaped = True
                while self.fag._channel.get_busy():
                    time.sleep(0.0001)
                self.fag._channel = self.firYappers.play(self.assets_dir.joinpath('snd_weaponpull.wav'))
                self.logit(log_message=f"* click!                                                                                                                     ", end='\n')
                self.fag.stop()
        else:
            pass

    def _is_window_focused(self):
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32

        # Get handle of the console window
        console_hwnd = kernel32.GetConsoleWindow()

        # Get handle of the foreground window
        foreground_hwnd = user32.GetForegroundWindow()

        return console_hwnd == foreground_hwnd

class ReshiramCFGBackup:
    def __init__(self):
        self.reshiram_config_beta = {
            "super-duper-awesome-config": {
                "signature": "I love men",
                "version": 3.1,
            },
            "meta": {
                    "owner": "Ayyvery",
                    "version": 1.20250614
            },
            "config": {
                "shutdown_on_exception": True,
                "use_cache": True,
            },
            "bot-config": {
                "token": "",
                "status_override_enabled": False,
                "status_override_index": 0,
                "reshi_ai_enabled": False,
                "reshi_ai_trigger_chance": 0.1,
                "random_actions_enabled": True,
                "random_actions_trigger_chance": 0.1,
                "load_cogs": True,
                "sync_commands": True,
                "sync_to_guild_only": False,
                "trigger-words": {
                    "prefixes": [
                        "r!",
                        "reshi"
                    ],
                    "weed_words": [
                        "weed",
                        "bunt",
                        "drugs",
                        "cocaine",
                        "meth",
                        "breaking bad",
                        "blunt",
                        "crack",
                        "tabacco",
                        "cannabis",
                        "heroin",
                        "lsd"
                    ],
                    "cat_words": [
                        "cat",
                        "car",
                        "kitty",
                        "kimty",
                        "gato",
                        "cato",
                        "chipflake"
                    ]
                },
                "guild-ids": {
                    "main_server": 1254174939003490334,
                    "cache_server": 1353461461091090453,
                    "icon_server": 1363646815529996371,
                    "stgo_server": 0000000000000000000,
                },
                "channel-ids": {
                    "reshiram_channel": 1352795719731380294,
                    "reshiram_diary": 1360205981300293673,
                    "reshiram_error_report": 1372212965306138717,
                    "minecraft_channel": 1352774690006896661,
                    "minecraft_news_channel": 1340091380273516554
                },
                "user-ids": {
                    "user_avery": 864240411656192000,
                    "user_reshiram": 1265643551023169611,
                    "user_zekrom": 1311376747132092426
                },
                "role-ids": {
                    "monster_energy": 1311392238538067980
                },
                "response-messages": {
                    "ask_responses": [
                        "yes",
                        "no",
                        "maybe",
                        "probably",
                        "probably not",
                        "oh for sure",
                        "oh hell nah",
                        "never ask me a god damn thing again",
                        "I don't wanna answer that",
                        "fuck off why don'tcha",
                        "yeah",
                        "nah",
                        "yup",
                        "nope",
                        "what are you yapping about",
                        "sometimes",
                        "always",
                        "never",
                        "hey OP, what the fuck does this mean"
                    ],
                    "ask_emotions": [
                        ":)",
                        ":(",
                        ":]",
                        ":[",
                        ":}",
                        ":{",
                        ":3",
                        "3:",
                        ":c",
                        "c:",
                        "^-^",
                        "^w^",
                        "OwO",
                        "owo",
                        "UwU",
                        "uwu",
                        ">w<",
                        ">.<",
                        ">~<",
                        ">///<",
                        ":D",
                        "D:",
                        ":^)",
                        ":^(",
                        "-w-",
                        "-.-",
                        "._.",
                        "O_o",
                        "o_O",
                        "(=^ ◡ ^=)",
                        "(ಥ﹏ಥ)"
                    ],
                    "random_messages": [
                        "I love men",
                        "bro what are you talking aaobuatsdo",
                        "RIGGED",
                        "alright buddy.",
                        "this map sucks",
                        "pokemon peaked with gen5",
                        "a chair is a PIGOASGIAHNP",
                        "hehehe... i'm pleasuring myself...",
                        "owo there's a wot to unpack here >~<",
                        "oh don't worry about your strong objections, they've been duly noted and promptly ignored"
                    ],
                    "reshiram_mentioned": [
                        "you called?",
                        "what is it",
                        "yeah?",
                        "reshiram!",
                        "Reshiram: Activated.",
                        "what is it you want",
                        "how can I help",
                        "?",
                        "Not now, I'm plowing my very hot wife",
                        "Not now, I'm plowing my very hot husband",
                        "Not now, I'm plowing your very hot wife",
                        "Not now, I'm plowing your very hot husband",
                        "ugh",
                        "if it's about catching me, the answer is no",
                        "I'm at the soup store rn, call me l8r",
                        "Seargent Reshiram, at your service!",
                        "Hewwo",
                        "Hello Unova!",
                        "'sup",
                        "Yes?",
                        "what now",
                        "that's me",
                        "was that a JoJo reference!?",
                        "don't tell MatPat about that one",
                        "the rizzler",
                        "SKIBIDI SIGMA!!!",
                        "she resh on my ri 'till I ram",
                        "I love weed", "<:Reshiram:1311331170109100124>"
                    ],
                    "zekrom_mentioned": [
                        "that's my husband!",
                        "that's my wife!",
                        "<:Zekrom:1311331297234386945>"
                    ],
                    "is_this_true": [
                        "yeah",
                        "nope",
                        "maybe",
                        "uhh idk",
                        "google it",
                        "ask ChatGPT",
                        "ask Grok",
                        "@grok is this true?",
                        "wouldn't you like to know, weather boy"
                    ]
                },
                "status-config": {
                    "random": {
                        0: {
                            "discord": discord.ActivityType.playing,
                            "statuses": [
                                "nothing",
                                "Minecraft",
                                "Garry's Mod",
                                "Team Fortress 2",
                                "Among Us",
                                "Minceraft",
                                "Half Life 2",
                                "Pokémon Black",
                                "Pokémon White",
                                "Pokémon Black 2",
                                "Pokémon White 2"
                            ]
                        },
                        1: {
                            "discord": discord.ActivityType.streaming,
                            "statuses": [
                                "nothing",
                                "my ass",
                                "my pussy",
                                "my dick",
                                "on Twitch",
                                "on YouTube",
                                "my source code"
                            ]
                        },
                        2: {
                            "discord": discord.ActivityType.listening,
                            "statuses": [
                                "nothing",
                                "Spotify",
                                "Apple Music",
                                "YouTube Music",
                                "Amazon Music",
                                "Deez (nuts)er",
                                "SoundCloud",
                                "Bandcamp"
                            ]
                        },
                        3: {
                            "discord": discord.ActivityType.watching,
                            "statuses": [
                                "nothing",
                                "porn",
                                "not porn",
                                "YouTube",
                                "Netflix",
                                "Disney+",
                                "Hulu",
                                "TV",
                                "pokemon",
                                "pokemon porn",
                                "femboy porn"
                            ]
                        },
                        4: {
                            "discord": discord.ActivityType.custom,
                            "statuses": [
                                "is this thing on?",
                                "hello unova!",
                                "another day another dollar",
                                "kissing Zekrom",
                                "I see you",
                                "r!help",
                                "ask me for the weather forecast"
                            ]
                        },
                        5: {
                            "discord": discord.ActivityType.competing,
                            "statuses": [
                                "nothing",
                                "jerkmate",
                                "boy kissing",
                                "ball touching",
                                "worst source code ever"
                            ]
                        },
                    },
                    "overrides": [
                        "status overridden!",
                        "deltarune tommorow"
                    ],
                    "types": {
                        0: 'dnd',
                        1: 'idle',
                        2: 'invisible',
                        3: 'offline',
                        4: 'online'
                    }
                },
                "miscellaneous": {
                    "blackout_messages": [
                        "blacked out for a sec.. what happened?!",
                        "'sup bitches i'm back",
                        "what did I miss",
                        "fuckass app🥀",
                        "``error code: 69``. fuck yourself"
                    ],
                    "error_messages": [
                        "why did you do that?",
                        "whoops!",
                        "errm, what the sigma",
                        "did you try restarting?",
                        "import FixEverything",
                        ":3c",
                        "sudo rm -rf /*",
                        "should've used Rust",
                        "still better than using JS",
                        "maybe try Frontend",
                        "maybe try Backend",
                        "apply at Microsoft",
                        "update your driversggfdhfdklnhfdg"
                    ],
                    "error_images": [
                        "https://iili.io/3cuA172.png",
                        "https://iili.io/3cJjdjj.png",
                        "https://iili.io/3cmNr3x.png",
                        "https://iili.io/3UNuEen.jpg",
                        "https://iili.io/3UNR2Mx.jpg",
                        "https://iili.io/3UN5WXa.jpg",
                        "https://iili.io/3UNcDcx.jpg",
                        "https://iili.io/3UNlp0G.jpg",
                        "https://iili.io/3UN1ln9.jpg",
                        "https://iili.io/3UNGe2a.jpg",
                        "https://iili.io/3UNWRXp.jpg",
                        "https://iili.io/3UNjWhv.png",
                        "https://iili.io/3UNwxGp.png",
                        "https://iili.io/3UNNvzG.png",
                        "https://iili.io/3UNOZvt.png",
                        "https://iili.io/3UNeSl2.png",
                        "https://iili.io/3UNkr1R.webp",
                        "https://iili.io/3UN83ap.webp",
                        "https://iili.io/3UNSskB.gif"
                    ],
                    "chair_message": [
                        "A Chair is a piece of furniture with a raised surface supported by legs, commonly used to seat a single person. Chairs are supported most often by four legs and have a back; however, a Chair can have three legs or can have a different shape. Chairs are made of a wide variety of materials, ranging from wood to metal to synthetic material (e.g. plastic), and they may be padded or upholstered in various colors and fabrics, either just on the seat (as with some dining room Chairs) or on the entire Chair. Chairs are used in a number of rooms in homes (e.g. in living rooms, dining rooms, and dens), in schools and offices (with desks), and in various other workplaces, such as the Black Mesa facility. A Chair without a back or arm rests is a stool, or when raised up, a bar stool. A Chair with arms is an armChair; one with upholstery, reclining action, and a fold-out footrest is a recliner.A permanently fixed Chair in a train or theater is a seat or, in an airplane, airline seat; when riding, it is a saddle or bicycle saddle; and for an automobile, a car seat or infant car seat. With wheels it is a wheelChair; or when hung from above, a swing. An upholstered, padded Chair for two people is a 'loveseat', while if it is for more than two person it is a couch, sofa, or settee; or if is not upholstered, a bench. A separate footrest for a Chair, usually upholstered, is known as an ottoman, hassock, or pouffe."
                    ]
                }
            },
            "behaviour": {
                "token_mode": "OS",
                "open_manager_gui_on_launch": False
            },
            "fun": {
                "taking_too_long": [
                    "YOUR TAKING TOO LONG",
                    "YOURTAKINGTOOLONG",
                    "YOUR            LONG",
                    "                LONG",
                    "YOUR TAKING TOO TOO",
                    "YOUR        TOO TOO",
                    "ʸᵒᵘʳ ᵗᵃᵏᶦⁿᵍ ᵗᵒᵒ ˡᵒⁿᵍ ",
                    "ʸᵒᵘʳ ᵗᵃᵏᶦⁿᵍ ᵗᵒᵒ ˡᵒⁿᵍ IS TAKING TOO LONG",
                    "        LOL        ",
                    "ʸᵒᵘʳ          ˡᵒⁿᵍ ",
                    "YOUR. TOO. BRIGHT!!!"
                ]
            },
            "debug": {
            }
        }

    async def backup(self):
        suggestion = "example suggestion that goes longer than 100 characters by just being really elaborate and in depth, good for getting the point across but not good if you have a byte limit when contacting discord's API"
        constructed_example_feature = {
            "aaaaaa0a0a000a00a000000a0aaa0000": {
                "user": "RESHIRAM_CONFIG_BACKUP",
                "suggestion": f"{suggestion}",
                "suggestion_short": f"{suggestion[:25]}",
                "suggestion_length": f"{len(suggestion)}",
                "status": None,
                "date_submitted": f"{time.strftime('%d.%m.%y - %H:%M:%S')}",
                "last_updated": f"{time.strftime('%d.%m.%y - %H:%M:%S')}"
            }
        }
        cfg_path = Path(__file__).parent.joinpath('data').joinpath('.private').joinpath("beta-config.json")
        with open(cfg_path, 'w', encoding='utf-8') as f:
            data = json.dumps(self.reshiram_config_beta, indent=4)
            f.write(data)

try:
    Reshifag = Reshiram()
    Reshifag.start()
except Exception as e:
    Reshifag.firLoggers("SYSTEM", "E", "AN ERROR HAPPENED. SOMEWHERE.", fm_error=e, fc_issync=True)
except BaseException:
    Reshifag.firLoggers("SYSTEM", "E", "CRITICAL ERROR", fc_issync=True)
    Reshifag.stop()
finally:
    RCI.firLockers.release_lock()