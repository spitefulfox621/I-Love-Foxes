#### never importing on __init__ again #####
import os, asyncio, aiofiles, time, toml, json, pygame, logging, base64, inspect, random, uuid
from datetime import datetime
from colorama import Fore, Back, Style, init
from typing import Optional, Callable, Literal, Union
from rich.progress import track
from enum import Enum
init(autoreset=True)
pygame.mixer.init()
pygame.init()
######## biggest mistake of my life ########

class locations:
    spitefox_dir = os.path.join(os.getenv("APPDATA"), ".spitefox")
    spitefox_dir_p = os.path.join(os.getenv("LOCALAPPDATA"), ".spitefox-persistent")

    spitefox_data = os.path.join(spitefox_dir_p, "spiteƒox")
    spitefox_assets = os.path.join(spitefox_data, "assets")
    spitefox_logs = os.path.join(spitefox_data, "logs")

    spitefox_config = os.path.join(spitefox_data, "spitefox.toml")
    discord_tokens = os.path.join(spitefox_data, "tokens.json")
    furfag_colours = os.path.join(spitefox_data, "furfag_colours.json")
    furfag_instances = os.path.join(spitefox_data, "furfag_instances.json")

class furfag:
    """
    Furfag:
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡄⠀⠀⠀⠀⠀⢀⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⣠⠃⠇⢀⡠⠤⠖⠒⠉⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⣀⠠⠖⠊⠉⠀⠀⠈⠁⢀⡟⠁⠀⠀⠀⠀⠀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⢀⢀⡠⠔⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⢦⠀⠀⢀⣜⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⢣⡠⠔⢒⣆⡀⡀⠀⠀⠀⠀⢀⡀⠀⠉⠀⣸⠀⠀⠀⠀⠀⠈⠉⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠑⢤⡀⠁⣧⠆⠀⢠⣶⣿⣿⢢⠻⢤⡻⠆⠀⠀⠀⠀⠀⢀⠜⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠈⠣⢄⡀⠀⠟⠿⣿⠟⣬⡄⣿⣿⣤⡄⠂⣠⢆⡤⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⢧⠤⢤⣤⣙⣀⣈⣁⣸⡿⠥⣀⢻⠓⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⢀⡠⢼⣿⣿⣿⣿⡿⠿⠿⣿⢿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⣀⡀⠀⠲⣶⢄⣠⢶⠀⠀⠀
        ⠀⠀⠀⠀⢀⡴⠒⠉⠀⠀⠐⢿⣿⠇⠀⠀⠀⠀⠀⢳⠀⠀⠀⠀⠀⠀⠀⢀⡰⠊⠉⠀⠀⠀⠀⠀⠉⠐⠤⣸⠀⠛⢼⠀⠀⠀
        ⠀⠀⠀⡠⢿⣶⠔⠒⠒⠤⡀⠀⠀⠀⠀⣀⡀⠀⠀⠚⢆⠀⠀⠀⠀⠀⢠⡎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠽⠀⠀⡟⠀⠀⠀
        ⠀⠀⢠⠃⢸⣯⠀⠀⠀⠀⢼⡆⣰⠋⠁⠉⣛⡏⠑⣄⠈⡆⠀⠀⠀⠀⠀⠈⠉⣢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢧⠀⠀⠀
        ⠀⠀⣦⠀⠀⠙⠗⠢⢄⣸⡠⠃⢳⣤⣤⣴⡾⠀⠀⠘⡄⢰⡀⠀⠀⠀⠀⡠⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢇⠀⠀
        ⠀⠀⠇⠁⠀⠀⢸⣀⣾⠿⣷⣴⠾⣿⡍⠘⣄⣀⠀⠀⠹⠀⠃⠀⠀⠀⢰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢸⡆
        ⠀⠀⢰⡀⠀⢤⣾⡾⠃⠀⠀⠀⠀⠈⢿⡄⢈⠀⠀⠀⠀⠀⡀⠀⠀⠀⢰⡠⠺⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⢸⡞⢸
        ⠀⣀⣀⣙⠒⠺⡏⠀⠀⠀⠀⠀⠀⠀⠀⢻⢄⢣⣀⠀⢀⡴⠛⠦⣀⠀⠀⠁⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⠀⠀⠘⠁⡸
        ⠀⢹⢾⡉⠉⠓⠧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⡏⠑⠊⠀⠀⠀⠈⠉⠀⠒⠚⢆⠀⣦⡀⠀⠀⠀⠀⠀⢠⢆⢀⠇⠀⠀⢰⠃
        ⠀⢸⠄⠑⣆⡀⠀⠈⢢⣀⡀⠴⠀⠀⠀⠀⠀⠀⠙⠦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠟⠹⡄⠀⠀⠀⢀⠎⠈⠚⠀⢠⠶⠃⠀
        ⠀⠀⠀⠘⢻⠑⠢⣀⡘⡏⢸⢤⠀⠀⠀⠀⠀⠀⢠⠝⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⠀⣠⠖⠉⠀⠀⠀⣠⠋⠀⠀⠀
        ⠀⠀⠀⠀⡀⠀⠀⠸⡯⠼⢏⡤⠃⢤⣀⣀⣀⠀⠸⠀⠀⠑⡄⢰⢄⡀⠀⠀⠀⠀⠀⠀⠀⠸⠞⠁⠀⠀⢀⣠⠾⣻⠀⠀⠀⠀
        ⠀⠀⠀⠀⢷⣿⣿⣿⡿⠋⠏⠀⠀⠀⣿⣿⣿⣿⣿⠀⠀⠀⠸⡜⠀⠈⠉⠈⠉⠉⠳⣄⠀⠀⠀⠀⠀⠀⠈⢀⡴⠁⠀⠀⠀⠀
        ⠀⠀⠀⠀⢸⣿⣿⣿⣧⣀⢀⣤⣤⡴⠿⠿⠿⢿⣿⡄⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠒⠒⠒⠒⠋⠁⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⢸⠟⣋⣡⣤⣤⣍⣯⣴⣶⣿⣿⣿⣿⣶⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """
    def __init__(self, spitefoxclient):
        """
        Args:
            spitefoxclient (str): Path to the client file
        """
        self.startup = True
        self.firLoggers = furfag.firLoggers(self)
        self.firHelpers = furfag.firHelpers(self)
        self.firStartup = furfag.firStartup(self)
        self.firYappers = furfag.firYappers(self)
        self.firTimers = furfag.firTimers(self)

        self.client = os.path.splitext(os.path.basename(spitefoxclient))[0].lower()
        self.client_user = os.environ['USERPROFILE']
        self.client_root = os.path.dirname(os.path.abspath(spitefoxclient))
        self.client_dir = os.path.join(locations.spitefox_dir, self.client)
        self.client_dir_p = os.path.join(locations.spitefox_dir_p, self.client)
        self.client_id = base64.b64encode(self.client.encode('utf-8')).decode('utf-8')

        asyncio.run(self.spitefox_setup())

    ####################### functions #########################################

    async def spitefox_setup(self):
        self.firTimers.start('spitefox_setup')
        await self.firLoggers("spiteƒox", "I", f"initializing spitefox", self.firYappers.square)
        try:
            await self.selfcest()
            await self.firHelpers.furfag_instances_manager()
        except Exception as e:
            await self.firLoggers("spiteƒox", "E", f"failed to initialize spitefox: {e}")
            exit()
        finally:
            await self.firLoggers("spiteƒox", "D", f"spitefox initialized", self.firTimers.stop('spitefox_setup'))
            await self.spitefox_finalize()

    async def selfcest(self):
        try:
            client_config = os.path.join(self.client_dir_p, 'config.toml')
            spitef_config = locations.spitefox_config

            missing_paths = [
                path for path in [
                (self.client_dir),
                (self.client_dir_p),
                (locations.spitefox_dir),
                (locations.spitefox_dir_p),
                (locations.spitefox_data),
                (locations.spitefox_assets),
                (locations.spitefox_logs)
                ] if not os.path.exists(path)
                ]

            missing_files = [
                path for path in [
                (client_config),
                (spitef_config),
                (locations.discord_tokens),
                (locations.furfag_colours),
                (locations.furfag_instances),
                (os.path.join(locations.spitefox_assets, 'ready.mp3')),
                (os.path.join(locations.spitefox_assets, 'shutdown.mp3')),
                (os.path.join(locations.spitefox_assets, 'square.mp3')),
                (os.path.join(locations.spitefox_assets, 'startup.mp3')),
                ] if not os.path.exists(path)
                ]

            if missing_paths:
                await self.firHelpers.directory_manager(tree_list=missing_paths)
            if missing_files:
                await self.firStartup.create_spitfox_files(file_list=missing_files)

        except Exception as e:
            print(Fore.RED + "self_test", Fore.BLUE + "FAILED")
            print("ERROR:", e)
            exit()

        finally:
            spitefox_message = Fore.WHITE + Style.DIM + '| ' + Style.RESET_ALL + Fore.RED + Style.BRIGHT + 'spite' + Fore.WHITE +'ƒox' + Style.RESET_ALL + ' by ' + Fore.MAGENTA + Style.BRIGHT + 'Ayyvery~'
            print(Fore.GREEN + "self_test", Fore.BLUE + "OK", spitefox_message)
            self.config =           await self.firHelpers.load_toml(client_config)
            self.config_spitefox =  await self.firHelpers.load_toml(spitef_config)
            self.firYappers.startup()

    async def spitefox_finalize(self):
        if (self.config_spitefox["settings"]["enable_debug_logs"] and self.config_spitefox["settings"]["enable_xdebug_logs"]) is True:
            await self.firLoggers("spiteƒox", "W", f"warning! extended debug logs are enabled! these message tend to clog up the console/log quite a lot. not reccomended for regular use.")
        client_length = len(self.client)
        client_plus_spaces = self.client + ' ' * (8 - client_length)
        #         truncate client name if its longer than 8  else  add spaces if its less than 8   else    just client name if it matches 8 characters
        client_adjusted = (self.client[:8]) if client_length > 8 else client_plus_spaces if client_length < 8 else (self.client)
        print(f"|---------------------------------------------|")
        print(f"| \x1b[35m\x1b[1mfurfag \x1b[0minstance created for client \x1b[32m\x1b[2m{client_adjusted}\x1b[0m |")
        print(f"|---------------------------------------------|")
        self.startup = False

    async def spitefox_shutdown(self):
        await self.firLoggers("spiteƒox", "W", "💤 shutting down...", self.firYappers.shutdown)
        self.firLoggers.ffc.Colours['issuers'] = self.firLoggers.ffc.issuers
        self.firLoggers.ffc.Colours['modules'] = self.firLoggers.ffc.modules
        self.firLoggers.ffc.Colours['classes'] = self.firLoggers.ffc.classes
        self.firLoggers.ffc.Colours['statuses'] = self.firLoggers.ffc.statuses
        await self.firHelpers.save_json(locations.furfag_colours, self.firLoggers.ffc.Colours)
        while pygame.mixer.get_busy():
            await asyncio.sleep(0.0001)

    ####################### classes ##########################################

    class firLoggers:
        def __init__(self, parent):
            self.furfag = parent
            self.firLoggers_queue = asyncio.Queue() # printer queue, courtesy of risumies <3 (slightly rewritten)
            self.ffc = self.furfagColours(self)

        async def __call__(self, issuer:Literal['spiteƒox', 'DISCORD', 'SYSTEM'], status:Literal['I', 'W', 'E', 'D', 'X'], message: str, misc:Optional[Union[Callable, int, str]] = None, end: str = None) -> None:
            firloggers_timestamp = datetime.now().strftime("%H:%M:%S")

            # Inspect the previous stack frame
            frame = inspect.stack()[1].frame
            cls_name = None

            # Try to get the class name if `self` or `cls` is in locals
            if 'self' in frame.f_locals:
                cls_name = type(frame.f_locals['self']).__name__
            elif 'cls' in frame.f_locals:
                cls_name = frame.f_locals['cls'].__name__
            else:
                cls_name = 'CLS_MISSING'

            data = (
                firloggers_timestamp,
                issuer,
                cls_name,
                inspect.stack()[1].function,
                status,
                message,
                misc,
                end
                )

            await self.firLoggers_queue.put(data)

        async def furfag_colours_updater(self):
            """
            firLoggers colour values updater
                creates a loop to save ffc values to file - upon being started it waits 16 seconds before making it's first save - then sleeps for 609 seconds after every save
            """
            await self.furfag.firLoggers("spiteƒox", "I", "furfagColours updater started!")
            self.ffc.Colours = await self.furfag.firHelpers.load_json(locations.furfag_colours)
            await asyncio.sleep(16)
            while True:
                self.ffc.Colours['issuers'] = self.ffc.issuers
                self.ffc.Colours['modules'] = self.ffc.modules
                self.ffc.Colours['classes'] = self.ffc.classes
                self.ffc.Colours['statuses'] = self.ffc.statuses
                await self.furfag.firHelpers.save_json(locations.furfag_colours, self.ffc.Colours)
                await asyncio.sleep(609)

        async def firLoggers_queue_handler(self):
            """
            firLoggers log queue handler
                creates a loop to handle an asyncio queue of log messages - doesn't process the queue until furfag/spiteƒox is fully set up

            config options:
                enable_debug_logs (bool): wether or not to print/log messages marked as DEBUG(D) in ``status``
                enable_xdebug_logs (bool): wether or not to print/log messages marked as EXTENDED_DEBUG(X) in ``status`` (requires enable_debug_logs to be ``enabled``)
                show_hidden_messages (bool): wether or not to print messages marked as DEBUG(D) or EXTENDED_DEBUG(X) in ``status`` as ``(x) hidden messages``

            """
            await self.furfag.firLoggers("spiteƒox", "I", "firLoggers queue started!")
            log_map = {
            'I': lambda: self.firLogger.info(firLog),
            'W': lambda: self.firLogger.warning(firLog),
            'D': lambda: self.firLogger.debug(firLog),
            'X': lambda: self.firLogger.debug(firLog),
            'E': lambda: self.firLogger.error(firLog),
            }
            await asyncio.to_thread(self.setup_firlogs)
            debug_logs = self.furfag.config_spitefox["settings"]["enable_debug_logs"]
            xdebug_logs = self.furfag.config_spitefox["settings"]["enable_xdebug_logs"]
            show_hidden_msgs = self.furfag.config_spitefox["settings"]["show_hidden_messages"]
            hidden_messages = 0
            sleep_time = 0
            while True:
                try:
                    if self.furfag.startup is True:
                        pass
                    else:
                        firdata = await self.firLoggers_queue.get()                                                                 # 0 - timestamp | 1 - issuer | 2 - class | 3 - module | 4 - status | 5 - message | 6 - additional content | 7 - end
                        sleep_time = (0.1 if (firdata[4] == 'I' or firdata[4] == 'W' or firdata[4] == 'E') else 0.0001 if (firdata[4] == 'D' or firdata[4] == 'X') else 0)      # 0.1 for regular prints, 0.0001 for debug prints, 0 for unknown prints
                        is_message_hidden = (True if ((sleep_time == 0.0001) and (debug_logs is False or xdebug_logs is False)) else False)                                     # message will get hidden if debug logs are disabled
                        if is_message_hidden is True:                                                               # if message is hidden, dont process it and increase the counter
                            hidden_messages += 1
                            if show_hidden_msgs is True:
                                print(Style.DIM + f'{hidden_messages} hidden messages', end='\r')                   # show a little '(x) messages hidden' print
                            pass
                        else:
                            if show_hidden_msgs is True and hidden_messages > 1:                                    # once we finally get a non hidden message, print a final count of hidden messages and then move on to processing the non hidden one
                                print(Style.DIM + f'{hidden_messages} hidden messages.')
                                hidden_messages = 0                                                                 # also reset the hidden message counter
                            ########################
                            cons_formatted, cons_unformatted = await self.console_formatter(data=firdata)
                            ##############################################################################
                            firConsole = f"{cons_formatted}"
                            firLog = f"{cons_unformatted}"
                            ###############################
                            log_map[firdata[4]]()
                            print(firConsole, end=firdata[7])
                            ##################################
                except Exception as e:
                    print(Style.BRIGHT + Fore.RED + 'error in firPrinters queue:', e)
                finally:
                    await asyncio.sleep(sleep_time)

        async def console_formatter(self, data):
            ##################################################################################################################
            timestamp, issuer, module_cls, module, status, message, misc, _ = data
            ##################################################################################################################

            index_i = next((entry for entry in self.ffc.issuers if entry["issuer"] == issuer), None)
            index_m = next((entry for entry in self.ffc.modules if entry["module"] == module), None)
            index_c = next((entry for entry in self.ffc.classes if entry["class"] == module_cls), None)
            index_s = next((entry for entry in self.ffc.statuses if entry["status"] == status), None)

            if index_i is None:
                await self.ffc.new_ffc_issuer(issuer)

            if index_m is None:
                await self.ffc.new_ffc_module(module)

            if index_c is None:
                await self.ffc.new_ffc_class(module_cls)

            if index_s is None:
                await self.ffc.new_ffc_status(status)

            for entry in self.ffc.issuers:
                if entry["issuer"] == issuer:
                    issuer_ansi = entry["ffc_ansi"]

            for entry in self.ffc.modules:
                if entry["module"] == module:
                    module_ansi = entry["ffc_ansi"]

            for entry in self.ffc.classes:
                if entry["class"] == module_cls:
                    cls_ansi = entry["ffc_ansi"]

            for entry in self.ffc.statuses:
                if entry["status"] == status:
                    status_ansi = entry["ffc_ansi"]

            ##################################################################################################################
            pre_bracket = Fore.WHITE + Style.BRIGHT + "["
            mid_bracket = Fore.MAGENTA + Style.BRIGHT + "/"
            suf_bracket = Fore.WHITE + Style.BRIGHT + "]"
            ##################################################################################################################
            timestamp_f = pre_bracket + Fore.MAGENTA + timestamp + suf_bracket + Style.RESET_ALL
            issuer_f = issuer_ansi + issuer + Style.RESET_ALL
            module_cls_f = cls_ansi + module_cls + Style.RESET_ALL
            module_f = module_ansi + module + Style.RESET_ALL
            status_f = status_ansi + status + Style.RESET_ALL
            message_f = (Style.BRIGHT + Back.RED if message.startswith('warning! ') else Style.NORMAL) + message + Style.RESET_ALL
            #############################################################################################################################

            formatted_data = f"{timestamp_f} {pre_bracket}{issuer_f}.{module_cls_f}.{module_f}{mid_bracket}{status_f}{suf_bracket}: {message_f}"
            unformatted_data = f"[{timestamp}] [{issuer}.{module_cls}.{module}/{status}]: {message}"
            if misc is not None:
                try:
                    if inspect.ismethod(misc) or inspect.isfunction(misc): # functions !!! (apparently they're called methods? thats stupid)
                        additional_content_f, additional_content_u = Style.DIM + ' (🔉)', ' (🔉)'
                        misc()

                    elif isinstance(misc, Exception): # exception = error messages
                        additional_content_f, additional_content_u = Style.DIM + f" (ERROR: {misc})", f" (ERROR: {misc})"

                    elif isinstance(misc, float): # float = probably a timer
                        additional_content_f, additional_content_u = Style.DIM + f" (took {misc:.2f} seconds)", f" (took {misc:.2f} seconds)"

                    elif isinstance(misc, str): # str = catchall
                        additional_content_f, additional_content_u = Style.DIM + f" ({misc})", f" ({misc})"

                    else:
                        raise ValueError("unknown misc type")
                        additional_content_f, additional_content_u = None, None

                except Exception as e:
                    raise ValueError(f"uhh erm idk :3 ({e})")
                    return

                finally:
                    formatted_data += additional_content_f
                    unformatted_data += additional_content_u

            return formatted_data, unformatted_data

        def setup_firlogs(self):
            self.logs_path = os.path.join(locations.spitefox_logs, f"{self.furfag.client}.log")
            self.debug_logs_path = os.path.join(locations.spitefox_logs, f"{self.furfag.client}.debug.log")

            self.rootLogger = logging.getLogger()
            self.rootLogger.setLevel(logging.NOTSET)
            self.firLogger = logging.getLogger('firLoggers')
            self.firLogger.setLevel(logging.DEBUG)
            firlog_handler = logging.FileHandler(filename=self.logs_path, encoding='utf-8', mode='w')
            rootlog_handler = logging.FileHandler(filename=self.debug_logs_path, encoding='utf-8', mode='w')
            firlog_handler.setLevel(logging.DEBUG)
            rootlog_handler.setLevel(logging.DEBUG)
            firlog_handler.setFormatter(logging.Formatter('%(message)s'))
            rootlog_handler.setFormatter(logging.Formatter(f'[{datetime.now().strftime("%H:%M:%S")}] %(message)s'))

            logging.getLogger('discord').setLevel(logging.WARNING)
            self.firLogger.addHandler(firlog_handler)
            self.rootLogger.addHandler(rootlog_handler)
            for step in track(range(1600), description="starting...", refresh_per_second=165, transient=True):
                time.sleep(0.0001)

        class furfagColours:
            def __init__(self, firLogguhs):
                self.FL = firLogguhs
                self.Colours = {
                "issuers": [],
                "modules": [],
                "classes": [],
                "statuses": [],
                }
                self.issuers = self.Colours['issuers']
                self.modules = self.Colours['modules']
                self.classes = self.Colours['classes']
                self.statuses = self.Colours['statuses']

            async def new_ffc_issuer(self, ffc_issuer):
                issuer_color_style = {
                    "spiteƒox":     Fore.RED + Style.BRIGHT, # messages by spitefox
                    "DISCORD":      Fore.BLUE + Style.DIM, # messages by Discord Bot components
                    "SYSTEM":       Fore.WHITE + Style.DIM, # messages by the script itself
                    "CONFIG":       Fore.YELLOW + Style.DIM, # messages by the configuration
                    }

                ansi_code = (issuer_color_style[ffc_issuer] if ffc_issuer in issuer_color_style else Fore.CYAN + Style.DIM)
                data = {
                    "issuer": ffc_issuer,
                    "ffc_ansi": ansi_code
                }

                self.issuers.append(data)

            async def new_ffc_module(self, ffc_module):
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                ansi_code = f"\033[38;2;{r};{g};{b}m"
                data = {
                    "module": ffc_module,
                    "ffc_ansi": ansi_code
                }
                self.modules.append(data)

            async def new_ffc_class(self, ffc_class):
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                ansi_code = f"\033[38;2;{r};{g};{b}m"
                data = {
                    "class": ffc_class,
                    "ffc_ansi": ansi_code
                }
                self.classes.append(data)

            async def new_ffc_status(self, ffc_status):
                status_color_style = {
                    "I": Fore.GREEN + Style.BRIGHT,
                    "W": Fore.YELLOW + Style.BRIGHT,
                    "E": Fore.RED + Style.BRIGHT,
                    "D": Fore.BLUE + Style.BRIGHT,
                    "X": Fore.MAGENTA + Style.BRIGHT
                }
                ansi_code = (status_color_style[ffc_status] if ffc_status in status_color_style else Fore.CYAN + Style.DIM)
                data = {
                    "status": ffc_status,
                    "ffc_ansi": ansi_code
                }
                self.statuses.append(data)

    class firHelpers:
        def __init__(self, parent):
            self.furfag = parent
            self.ffi = []
            self.fft = []

        async def furfag_instances_manager(self):
            self.ffi = await self.load_json(locations.furfag_instances)

            async def update_entry():
                index = next((entry for entry in self.ffi if entry["client_id"] == self.furfag.client_id), None)
                if index is None:
                    await self.furfag.firLoggers("spiteƒox", "D", f"instance [{self.furfag.client}] not found in furfag_instances - creating new entry")
                    self.ffi.append(instance)
                    return

                configchanges = []
                for entry in self.ffi:
                    if entry["client_id"] == self.furfag.client_id: # if the entry's client_id matches the one of the current instance we continue with that
                        instance_config = self.furfag.config # for ease of use, store the config of the current instance
                        entry_config = entry["config"] # and the config of the entry as well
                        if self.furfag.client_root != entry["client_root"]: # if the client's root changed, update it as well(very important)
                            await self.furfag.firLoggers("spiteƒox", "D", f"client_root didnt match - updating")
                            entry["client_root"] = self.furfag.client_root
                        for k, v in instance_config.items(): # for every key/value in the instance's config
                            if k not in entry_config: # if the key doesnt exist in the entry's config, append it
                                await self.furfag.firLoggers("spiteƒox", "D", f"{k} not found in entry_config - adding new config entry")
                                entry_config[k] = v.copy()
                                configchanges.append(k)
                                continue
                            for k2, v2 in v.items(): # for every setting it also checks the individual key/value
                                if k2 not in entry_config[k]: # and if they don't exist, add them
                                    await self.furfag.firLoggers("spiteƒox", "D", f"{k2} not found in entry_config[{k}] - adding new config key")
                                    entry_config[k][k2] = v2
                                    configchanges.append((k, k2))
                                elif entry_config[k][k2] != v2: # or if they don't match, update them
                                    await self.furfag.firLoggers("spiteƒox", "D", f"{k2} didn't match {k} - updating entry")
                                    entry_config[k][k2] = v2
                                    configchanges.append((k, k2))

            try:
                error_raised = False
                instance = {
                    "client": self.furfag.client,
                    "client_id": self.furfag.client_id,
                    "client_root": self.furfag.client_root,
                    "client_dir": self.furfag.client_dir,
                    "client_dir_p": self.furfag.client_dir_p,
                    "config": self.furfag.config,
                }
                await update_entry()

                await self.save_json(locations.furfag_instances, self.ffi)

            except Exception as e:
                error_raised = True
                await self.furfag.firLoggers("spiteƒox", "E", f"an error occoured during instance checkup: {e}")

            finally:
                if error_raised is True:
                    exit()
                else:
                    await self.furfag.firLoggers("spiteƒox", "I", f"furfagInstances manager found no issues!")

        async def directory_manager(self, tree_list):
            try:
                for item in tree_list:
                    if not os.path.exists(item):
                        os.makedirs(item)
                        await self.furfag.firLoggers("spiteƒox", "X", f"created {os.path.relpath(item, self.furfag.client_user)}")

            except Exception as e:
                await self.furfag.firLoggers("spiteƒox", "E", f"failed to create one or more directories: {e}")

        async def load_json(self, file_path):
            try:
                async with aiofiles.open(file_path, "r", encoding='utf-8') as f:
                    file = await f.read()
                    data = json.loads(file)
                    await self.furfag.firLoggers("spiteƒox", "X", f"loaded json file", os.path.relpath(file_path, self.furfag.client_user))
                    return data
            except Exception as e:
                await self.furfag.firLoggers("spiteƒox", "E", f"failed to load json file", e)
                return None

        async def save_json(self, file_path, data):
            try:
                async with aiofiles.open(file_path, "w", encoding='utf-8') as f:
                    file = json.dumps(data, indent=2)
                    await self.furfag.firLoggers("spiteƒox", "X", f"saved json file", os.path.relpath(file_path, self.furfag.client_user))
                    await f.write(file)
            except Exception as e:
                await self.furfag.firLoggers("spiteƒox", "E", f"failed to save json file", e)

        async def load_toml(self, file_path):
            try:
                async with aiofiles.open(file_path, "r", encoding='utf-8') as f:
                    file = await f.read()
                    data = toml.loads(file)
                    await self.furfag.firLoggers("spiteƒox", "X", f"loaded toml file", os.path.relpath(file_path, self.furfag.client_user))
                    return data
            except Exception as e:
                await self.furfag.firLoggers("spiteƒox", "E", f"failed to load toml file", e)
                return None

        async def save_toml(self, file_path, data):
            try:
                async with aiofiles.open(file_path, "w", encoding='utf-8') as f:
                    file = toml.dumps(data)
                    await self.furfag.firLoggers("spiteƒox", "X", f"saved toml file", os.path.relpath(file_path, self.furfag.client_user))
                    await f.write(file)
            except Exception as e:
                await self.furfag.firLoggers("spiteƒox", "E", f"failed to save toml file", e)

        async def load_bytes(self, file_path):
            try:
                async with aiofiles.open(file_path, "rb", encoding='utf-8') as f:
                    data = await f.read()
                    await self.furfag.firLoggers("spiteƒox", "X", f"loaded bytes", os.path.relpath(file_path, self.furfag.client_user))
                    return data
            except Exception as e:
                await self.furfag.firLoggers("spiteƒox", "E", f"failed to load bytes", e)
                return None

        async def save_bytes(self, file_path, data):
            try:
                async with aiofiles.open(file_path, "wb") as f:
                    await self.furfag.firLoggers("spiteƒox", "X", f"saved bytes", os.path.relpath(file_path, self.furfag.client_user))
                    await f.write(data)
            except Exception as e:
                await self.furfag.firLoggers("spiteƒox", "E", f"failed to load bytes", e)

        def get_discord_bot_token(self):
            try:
                raise_your_yayaya = False
                with open(locations.discord_tokens, "r", encoding='utf-8') as f:
                    data = f.read()
                    tokens = json.loads(data)
                    returntoken = next((entry["token"] for entry in tokens if entry["name"] == self.furfag.client), None)

            except Exception as e:
                raise_your_yayaya = True
                print(Fore.MAGENTA + Style.BRIGHT + "furfag", Style.RESET_ALL + Fore.RED + f"an error occoured: {e}")

            finally:
                if raise_your_yayaya is True:
                    exit()
                else:
                    return returntoken

    class firStartup:
        def __init__(self, parent):
            self.furfag = parent

        async def create_spitfox_files(self, file_list):
            spitefox_config = {
                "super-duper-awesome-config": {
                    "signature": 'I love men',
                    "version": 3
                },
                "settings": {
                    "enable_firYappers": False, # sound effects
                    "enable_debug_logs": False, # debug logs
                    "enable_xdebug_logs": False, # extended debug logs()
                }
            }
            default_config = {
                "super-duper-awesome-config": {
                    "version": 3
                },
                "settings": {
                    "example_string": 'hello world',
                    "example_bool": True,
                    "example_int": 69,
                }
            }
            discord_tokens = [
                {
                    "name": "example_name",
                    "token": "example_token"
                },
                {
                    "name": "another_example_name",
                    "token": "another_example_token"
                }
            ]
            furfag_colours = {
                "issuers": [],
                "modules": [],
                "classes": [],
                "statuses": [],
                }

            furfag_instances = []

            from spiteƒox.spitefox_data import ready_mp3, shutdown_mp3, square_mp3, startup_mp3
            ready_mp3_decoded = await self.b64_str_to_bytes(ready_mp3)
            shutdown_mp3_decoded = await self.b64_str_to_bytes(shutdown_mp3)
            square_mp3_decoded = await self.b64_str_to_bytes(square_mp3)
            startup_mp3_decoded = await self.b64_str_to_bytes(startup_mp3)

            spf_file_paths = [
                (locations.spitefox_config, spitefox_config),
                (locations.discord_tokens, discord_tokens),
                (locations.furfag_colours, furfag_colours),
                (locations.furfag_instances, furfag_instances),
                (os.path.join(self.furfag.client_dir_p, "config.toml"), default_config),
                (os.path.join(locations.spitefox_assets, 'ready.mp3'), ready_mp3_decoded),
                (os.path.join(locations.spitefox_assets, 'shutdown.mp3'), shutdown_mp3_decoded),
                (os.path.join(locations.spitefox_assets, 'square.mp3'), square_mp3_decoded),
                (os.path.join(locations.spitefox_assets, 'startup.mp3'), startup_mp3_decoded)
            ]
            for path, data in spf_file_paths:
                if not os.path.exists(path):
                    if path.endswith('.json'):
                        await self.furfag.firHelpers.save_json(path, data)
                    elif path.endswith('.toml'):
                        await self.furfag.firHelpers.save_toml(path, data)
                    elif path.endswith('.mp3'):
                        await self.furfag.firHelpers.save_bytes(path, data)

        async def b64_str_to_bytes(self, provided_b64) -> bytes:
            data = base64.b64decode(provided_b64)
            return data

        async def bytes_to_b64_str(self, provided_bytes) -> str:
            data = base64.b64encode(provided_bytes).decode('ascii')
            return data

    class firTimers:
        def __init__(self, parent):
            self.furfag = parent
            self.timers = {}

        def start(self, name) -> None:
            self.timers[name] = time.time()

        def stop(self, name) -> int:
            if name not in self.timers:
                raise ValueError(f"No start time found for timer '{name}'")
            elapsed = (time.time() - self.timers[name])
            del self.timers[name]
            return elapsed

    class firYappers:
        def __init__(self, parent):
            self.furfag = parent
            self.startup_sound = os.path.join(locations.spitefox_data, "assets", "startup.mp3")
            self.ready_sound = os.path.join(locations.spitefox_data, "assets", "ready.mp3")
            self.square_sound = os.path.join(locations.spitefox_data, "assets", "square.mp3")
            self.shutdown_sound = os.path.join(locations.spitefox_data, "assets", "shutdown.mp3")

        def audino_handler(self, sound_to_play):
            if self.furfag.config_spitefox["settings"]["enable_firYappers"] is False:
                pass

            else:
                sound_map = {
                'startup': lambda: pygame.mixer.Sound(self.startup_sound),
                'ready': lambda: pygame.mixer.Sound(self.ready_sound),
                'square': lambda: pygame.mixer.Sound(self.square_sound),
                'shutdown': lambda: pygame.mixer.Sound(self.shutdown_sound),
                }
                sound = sound_map[sound_to_play]()
                sound.set_volume(0.1)
                channel = sound.play()

        def startup(self):
            self.audino_handler('startup')

        def ready(self):
            self.audino_handler('ready')

        def square(self):
            self.audino_handler('square')

        def shutdown(self):
            self.audino_handler('shutdown')