import tkinter as tk
import sys
import os
import colorama
import json
import toml
import subprocess
import requests
import time
import ctypes
import minecraft_rcon
import ddnsupdater
import serverpanelcreds
import psutil
import asyncio
import itertools
import time
import random
from threading import Event, Thread
from pygame import mixer
from minecraft_rcon import MinecraftRCON
from requests.auth import HTTPBasicAuth
from colorama import Fore, Back, Style, init
from tkinter import messagebox
from itertools import cycle
from pathlib import Path
from datetime import datetime
from functools import partial
from PIL import Image, ImageTk

class ServerStatusUpdater:
    def __init__(self, stop_event):
        self.stop_event = stop_event

    def serverstopped(self): #mine
        global serverstarting, serverstatus, serverplayercount, serverplayernames, serverwasstopped
        print(ssuconsole, Fore.RED + Style.DIM + "Server was shut down recently. stopping update thread.")
        serverstarting = 0
        serverstatus = "Offline"
        serverplayercount = 0
        serverplayernames = ""
        serverwasstopped = True
        self.stop_event.set()
        return

    def update_status(self, server): #mine >:3
        global serverstatus, serverstarting, server_ping_attempts, player_ping_attempts, serverplayercount, serverplayernames, sleeptime, sleeptimesmall, serverwasstopped, prelaunchsleeptime
        current_time = time.strftime("[%H:%M:%S]")
        ssuconsole = f"{current_time} " + Fore.WHITE + Style.BRIGHT + "[SSU]:"
        prelaunchsleeptime = 30 if server.get('system') == 'modern' else 60
        time.sleep(prelaunchsleeptime)  # Wait a bit for the server to start
        while not self.stop_event.is_set():
            if serverwasstopped is True:
                self.serverstopped()
                return
            try:
                rcon_instance = self.get_rcon_instance()
                serveronlineresponse, playercountresponse, playernamesresponse = self.get_server_status(rcon_instance)

                if serveronlineresponse is True and serverstarting == 1: # if server is online and serverstarting is 1, it probably just started
                    serverstarting = 0
                    serverstatus = "Started!"
                    time.sleep(sleeptimesmall)
                    if RCON_PASSWORD == serverpanelcreds.MODERNRCONPASSWORD:
                        levelnameentry = get_level_dir(server.get('location') + "/server.properties", "level-name")
                    else:
                        levelnameentry = "world folder name entry not available in legacy systems"
                    print(ssuconsole, Fore.CYAN + Style.DIM + f"server just started! hello [{levelnameentry}]")

                if serveronlineresponse is True and serverstarting == 0: # if server is online and serverstarting is 0, continue as normal
                    serverstatus = "Online"
                    time.sleep(sleeptimesmall)
                    print(ssuconsole, Fore.CYAN + Style.DIM + "everything operational, first test passed.")

                if serveronlineresponse is False and serverstarting == 0: # if server didn't respond but already started, speak up in console, also only care about this stuff if you have to
                    server_ping_attempts += 1
                    time.sleep(sleeptimesmall)
                    print(ssuconsole, Fore.RED + Style.DIM + f"server didn't respond. Server Ping Attempt: {server_ping_attempts}")

                if serveronlineresponse is False and serverstarting == 1: # if server didnt respond but is still starting, change serverstatus
                    serverstatus = next(status_cycle)
                    time.sleep(sleeptimesmall)
                    print(ssuconsole, Fore.RED + Style.DIM + "server didn't respond. still starting?")

                if playercountresponse >= 1 and playernamesresponse: # if server is online and player count is more tha 0, reflect that in the vars
                    player_ping_attempts = 0
                    serverplayercount = playercountresponse
                    serverplayernames = ", ".join(playernamesresponse) if playernamesresponse else "No players"
                    time.sleep(sleeptimesmall)
                    print(ssuconsole, Fore.CYAN + Style.DIM + "everything operational, second test passed.")

                if playercountresponse == 0 and serverstarting == 0: # if server is online and player count is 0
                    serverplayercount = 0
                    serverplayernames = ""
                    if close_if_empty == 'true':
                        player_ping_attempts += 1
                        time.sleep(sleeptimesmall)
                        print(ssuconsole, Fore.RED + Style.DIM + f"no players online. Player Ping Attempt: {server_ping_attempts}")

            except Exception as e:
                print(ssuconsole, Fore.RED + f"[ERROR] An error occurred during status update: {e}")

            finally:  # Final tests
                if serverstarting == 0 and server_ping_attempts >= 1: # if serverstarting is 0 but server ping attempts are 1 or more
                    time.sleep(sleeptimesmall)
                    print(ssuconsole, Fore.RED + Style.DIM + f"{server_ping_attempts} Server Ping Attempts")
                if serverstarting == 0 and player_ping_attempts >= 1: # if serverstarting is 0 but player ping attempts are 1 or more
                    time.sleep(sleeptimesmall)
                    print(ssuconsole, Fore.RED + Style.DIM + f"{player_ping_attempts} Player Ping Attempts")
                if serverwasstopped is True:
                    time.sleep(sleeptimesmall)
                    print(ssuconsole, Fore.RED + Style.DIM + f"{serverwasstopped} | Server appears to have been stopped. closing thread")
                    sleeptime = 5
                else:
                    time.sleep(sleeptimesmall)
                    print(ssuconsole, Fore.CYAN + Style.DIM + f"everything operational, final test passed. sleeping for {sleeptime} seconds...")
                time.sleep(sleeptime)

    def get_rcon_instance(self): #chatgpt
        """Dynamically create an RCON instance using the current RCON password."""
        global RCON_PASSWORD
        return MinecraftRCON(RCON_PASSWORD)

    def get_server_status(self, rcon_instance): #chatgpt
        """Fetch the consolidated server status."""
        try:
            response = rcon_instance.execute_command("list")
            if "There are" in response:
                # Parse the response for player count and list
                player_info = response.split(":")[0]
                player_count = int(player_info.split(" ")[2])
                player_list = response.split(":")[1].strip().split(", ") if ":" in response else []
                return True, player_count, player_list
            else:
                return False, 0, []
        except Exception as e:
            print(Fore.RED + f"[ERROR] Failed to fetch server status: {e}")
            return False, 0, []

class PIDLock:
    """PID-based lock to prevent multiple instances of a script."""
    def __init__(self, lock_file_path):
        self.lock_file_path = lock_file_path

    def acquire_lock(self):
        """Acquire a lock by writing the current process ID (PID) to the lock file."""
        if os.path.exists(self.lock_file_path):
            try:
                # Read the existing PID from the lock file
                with open(self.lock_file_path, "r") as lock_file:
                    existing_pid = int(lock_file.read().strip())

                # Check if the process is still running
                if psutil.pid_exists(existing_pid):
                    print(Fore.RED + Style.BRIGHT + "[STARTUP]",Fore.YELLOW + Style.BRIGHT + f"Another instance of the script is running with PID {existing_pid}. Exiting...")
                    sys.exit(1)
                else:
                    print(Fore.GREEN + Style.BRIGHT + "[STARTUP]",Fore.YELLOW + Style.BRIGHT + f"Stale lock file detected. Removing...")
                    os.remove(self.lock_file_path)
            except Exception as e:
                print(f"Error while checking lock file: {e}")
                sys.exit(1)

        # Write the current PID to the lock file
        with open(self.lock_file_path, "w") as lock_file:
            lock_file.write(str(os.getpid()))
        print(Fore.GREEN + Style.BRIGHT + "[STARTUP]",Fore.YELLOW + Style.BRIGHT + f"Lock acquired. PID {os.getpid()} written to lock file.")

    def release_lock(self):
        """Release the lock by deleting the lock file."""
        try:
            if os.path.exists(self.lock_file_path):
                os.remove(self.lock_file_path)
                print(Fore.GREEN + Style.BRIGHT + "[STARTUP]",Fore.YELLOW + Style.BRIGHT + "Lock released. Lock file removed.")
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + "[STARTUP]",Fore.YELLOW + Style.BRIGHT + f"Error while releasing lock: {e}")

def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            return toml.load(file)
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"config load error\n{e}")
        return {}

def load_index(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"index load error\n{e}")
        return {}

def save_config(file_path, config_data):
    try:
        with open(file_path, 'w') as file:
            toml.dump(config_data, file)
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"config save error\n{e}")

def startup():
    clear()
    print(Fore.GREEN + Style.BRIGHT + "[STARTUP]",Fore.YELLOW + Style.BRIGHT + "hello python console!")
    print(Fore.GREEN + Style.BRIGHT + "[STARTUP]",Fore.YELLOW + Style.BRIGHT + "server launch-pad by", Fore.MAGENTA + Style.BRIGHT + "Ayyvery~")
    print(Fore.GREEN + Style.BRIGHT + "[STARTUP]",Fore.YELLOW + Style.BRIGHT + "loading configs...")
    try:
        config_present = load_config(configpath)
        index_present = load_index(indexpath)
        if config_present:
            print(Fore.YELLOW + "    - config.toml loaded..")
        if index_present:
            print(Fore.YELLOW + "    - index.json loaded..")

    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "[ERROR]",Fore.RED + Style.DIM + f"that didn't work\n{e}")
        messagebox.error("Failure", "config load error :/\ncheck logs.")
        return

    print(Fore.GREEN + Style.BRIGHT + "[STARTUP]",Fore.GREEN + "done!")

    print(Fore.GREEN + Style.BRIGHT + "[STARTUP]",Fore.YELLOW + Style.BRIGHT + "applying config...")
    try:
        configuration()
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"that didn't work\n{e}")
        return
    print(Fore.GREEN + Style.BRIGHT + "[STARTUP]",Fore.GREEN + "done!")

    print(Fore.GREEN + Style.BRIGHT + "[STARTUP]",Fore.YELLOW + Style.BRIGHT + "starting the main program...")
    initialize_audio(background_music) # start the background music
    prologue() # start the main application

def configuration():
    config_errors = 0
    if update_ddns == 'true':
        update_ddns_records()
    elif update_ddns == 'false':
        pass
    if auto_update == 'true':
        update_ddns_records_background()
    elif auto_update == 'false':
        pass
    if minimize == 'true':
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    elif minimize == 'false':
        pass
    if do_config_check == 'true':
        conf_resp = incorrect_config_check()
        if conf_resp == 'CRITICAL':
            messagebox.showerror("CRITICAL ERROR", "One or more setting(s) break the application.\nexiting.")
            exit_script(root)
        elif conf_resp == 'CONFLICT':
            messagebox.showinfo("CONFLICT ERROR", "One or more setting(s) conflict with one another.\nYou can still use the launch-pad,\nhowever certain functions won't behave correctly.\nsee console for more info.")
        elif conf_resp == 'CORRECT':
            pass
        else:
            print("config checker responded nonesense.")
    elif do_config_check == 'false':
        pass

    if ext_debug == 'true':
        print(Fore.YELLOW + Style.BRIGHT + "[DEBUG]",Fore.YELLOW + Style.DIM + f"'update_ddns_on_launch' is set to {update_ddns}")
        print(Fore.YELLOW + Style.BRIGHT + "[DEBUG]",Fore.YELLOW + Style.DIM + f"'auto_update_ddns' is set to {auto_update}")
        print(Fore.YELLOW + Style.BRIGHT + "[DEBUG]",Fore.YELLOW + Style.DIM + f"'minimize_console_on_launch' is set to {minimize}")
        print(Fore.YELLOW + Style.BRIGHT + "[DEBUG]",Fore.YELLOW + Style.DIM + f"'main_background' is set to {background}")
        print(Fore.YELLOW + Style.BRIGHT + "[DEBUG]",Fore.YELLOW + Style.DIM + f"'launch_panel_background' is set to {background2}")
        print(Fore.YELLOW + Style.BRIGHT + "[DEBUG]",Fore.YELLOW + Style.DIM + f"'close_launchpad_on_server_boot' is set to {close_on_launch}")
        print(Fore.YELLOW + Style.BRIGHT + "[DEBUG]",Fore.YELLOW + Style.DIM + f"'ext_debug' is set to {ext_debug}")
        print(Fore.YELLOW + Style.BRIGHT + "[DEBUG]",Fore.YELLOW + Style.DIM + f"'background_music' is set to {background_music}")
    elif ext_debug == 'false':
        pass

def incorrect_config_check():
    global config_errors
    config_errors = 0

    # Define rules for conflicting settings
    conflict_rules = [
        {
            "settings": ["auto_update", "close_on_launch"],
            "message": "[Auto Update DDNS] and [Close Launchpad on Server Boot] conflict with each other",
            "reason": "[Close Launchpad on Server Boot] closes the Application when a server is started.\n                    [Auto Update DDNS] can not work without the application running."
        },
        {
            "settings": ["close_if_empty", "close_on_launch"],
            "message": "[Shutdown if Server Empty] and [Close Launchpad on Server Boot] conflict with each other",
            "reason": "[Close Launchpad on Server Boot] closes the Application when a server is started.\n                    [Shutdown if Server Empty] can not work without the application running."
        },
        {
            "settings": ["shutdown_if_empty", "close_on_launch"],
            "message": "[Shutdown PC if Server Empty] and [Close Launchpad on Server Boot] conflict with each other",
            "reason": "[Close Launchpad on Server Boot] closes the Application when a server is started.\n                    [Shutdown PC if Server Empty] can not work without the application running."
        }
    ]

    # Check for critical errors first
    debug_crash = "false"
    if debug_crash == 'true':
        print(Fore.RED + Style.BRIGHT + "[CONFIG-ERROR]", Fore.YELLOW + Style.BRIGHT +
              f"CRASHER is active.\nThis simulates a terribly invalid configuration.\nCrasher breaks the application.")
        config_errors = -100

    # Check for conflicts using rules
    for rule in conflict_rules:
        if all(eval(setting) == 'true' for setting in rule["settings"]):
            print(Fore.RED + Style.BRIGHT + "[CONFIG-WARN]", Fore.YELLOW + Style.BRIGHT + rule["message"])
            if ext_debug == 'true':
                print(Fore.RED + Style.BRIGHT + "[CONFIG-WARN-DEBUG]", Fore.YELLOW + rule["reason"])
            config_errors += 1

    # Print pretty little messages in the console
    if config_errors == 0:
        print(Fore.CYAN + Style.BRIGHT + "[CONFIG-INFO]", Fore.GREEN + Style.BRIGHT + "Configuration valid.")
        return 'CORRECT'
    elif config_errors > 0:
        print(Fore.CYAN + Style.BRIGHT + "[CONFIG-WARN]", Fore.YELLOW + Style.BRIGHT + f"Configuration invalid. {config_errors} configuration error(s).")
        return 'CONFLICT'
    elif config_errors < 0:
        print(Fore.CYAN + Style.BRIGHT + "[CONFIG-ERROR]", Fore.RED + Style.DIM + "Configuration critically invalid.")
        return 'CRITICAL'

def update_ddns_records():
    try:
        ddnsupdater.update_noip(ip=None)
    except Exception as e:
        messagebox.showerror("E", f"This didn't work: {e}")
        return None

def center_window(window):
    # center the window
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def initialize_audio(mp3_path):
    mixer.init()
    mixer.music.load(mp3_path)
    mixer.music.set_volume(0)
    mixer.music.play(-1)

def update_window_size(root, size):
    global current_windowsize
    current_windowsize = size
    root.geometry(size)

def setup_logging(log_file_path):
    """Redirect all output to a log file."""
    # Ensure the directory for the log file exists
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Open the log file in append mode
    log_file = open(log_file_path, "a")

    # Write a timestamped header
    log_file.write(f"--- Script started at {datetime.now()} ---\n")

    # Redirect stdout and stderr to the log file
    sys.stderr = log_file

    return log_file

### high priority functions ^^^^^^^^

# configuration names
configpath = './config/config.toml'
indexpath = './config/index.json'
config = load_config(configpath)
index = load_index(indexpath)
sdac = config['super-duper-awesome-config']
pc = config['path-config']
ls = config['launch-script']

# global variables
serverstarting = 0
serverstatus = "Offline"
current_windowsize = "256x256"
current_server_list = "nothing here... :("
is_dsd_open = "False"
previous_windowsize = "600x500"
server_ping_attempts = 0
player_ping_attempts = 0
current_serverselect = ""
are_modified = ""
config_errors = 0
serverplayercount = 0
serverplayernames = ""
sleeptime = 300
sleeptimesmall = 5
serverwasstopped = False

# sda config
update_ddns = sdac.get('update_ddns_on_launch').lower()
auto_update = sdac.get('auto_update_ddns').lower()
minimize = sdac.get('minimize_console_on_launch').lower()
close_on_launch = sdac.get('close_launchpad_on_server_boot').lower()
ext_debug = sdac.get('extended_debug').lower()
close_if_empty = sdac.get('auto_shutdown_on_empty_server').lower()
do_config_check = sdac.get('do_config_check_on_boot').lower()
shutdown_if_empty = sdac.get('auto_shutdown_pc_on_empty_server').lower()

# path config
background = pc.get('main_background').lower()
background2 = pc.get('launch_panel_background').lower()
background3 = pc.get('settings_panel_background').lower()
log_file_path = pc.get('log_file').lower()
background_music = pc.get('bgm').lower()

# server config - can't be put here as 'server' variable only gets defined once you select a server

# functional variables
stop_event = Event()
updater = ServerStatusUpdater(stop_event)
colorama.init()
init(autoreset=True)
clear = lambda: os.system('cls')
lock = PIDLock(pc.get('lock_file').lower())
log_file = setup_logging(log_file_path)
status_cycle = itertools.cycle(["Still Starting...", "Almost there...", "Taking longer than expected..."])

### regular priority functions vvvvvvvvvvvv

def go_back():
    if are_modified == '(modified)':
        choice = messagebox.askyesno("I", "you need to restart the application for changes to take effect.\nwould you like to restart now?")
        if choice is True:
            print("restarting...")
            python = sys.executable
            os.execv(python, ['python'] + sys.argv)
        if choice is False or None:
            pass
    update_window_size(root, previous_windowsize)
    main_menu(root)

def exit_script(root):
    log_file.write(f"--- Script ended at {datetime.now()} ---")
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    lock.release_lock()
    log_file.close()
    root.destroy()

def set_is_dsd_open_false():
    global is_dsd_open
    is_dsd_open = False

def toggle_setting(key):
    global config
    global are_modified
    are_modified = "(modified)"
    sdac = config['super-duper-awesome-config']
    current_value = sdac.get(key).lower()
    new_value = 'false' if current_value == 'true' else 'true'
    sdac[key] = new_value
    save_config(configpath, config)
    if ext_debug == 'true':
        print(Fore.YELLOW + Style.BRIGHT + "[DEBUG]",Fore.YELLOW + Style.DIM + f" {key} toggled to {new_value}")
    elif ext_debug == 'false':
        pass
    display_settings(root, sdac)  # refresh settings display

def launch_server(server, ls):
    global serverstarting
    global serverstatus
    rcon_instance = MinecraftRCON(RCON_PASSWORD)

    # make sure a server isn't already running/is currently starting
    if serverstarting == 1:
        messagebox.showerror("E", "a server is currently starting.")
        return
    elif rcon_instance.is_server_online():
        messagebox.showerror("E", "a server is already running.\nonly one server may be running at any given time.")
        return
    else:
        pass

    mcver = server.get('minecraft_version')
    mdldr = server.get('mod_loader').lower()
    location = server.get('location')
    java_path = ls.get('java21path' if mcver >= '1.21' else 'java17path')               # if minecraft version is 1.21 or above use java 21, otherwise use java 17
    ram_config = ls.get('ramconfig')                                                    # use ramconfig (8gb)
    jar_config = ls.get('jarconfig')                                                    # use jarconfig (-jar)
    mod_loader_jar = ls.get('modloader-f' if mdldr == 'fabric' else 'modloader-q')      # if modloader is fabric use fabric-server-launch otherwise use quilt-server-launch
    gui_config = ls.get('guiconfig')                                                    # use guiconfig (-nogui)
    system_ver = server.get('system').lower()                                           # which system we using (legacy or modern)

    command = [java_path,ram_config,jar_config,mod_loader_jar,gui_config]

    # print a pretty little launch message
    if ext_debug == 'true':
        print(Fore.YELLOW + Style.BRIGHT + "[DEBUG]",Fore.CYAN + "starting the Minecraft Server with the following arguments:")
        print(Fore.YELLOW + Style.BRIGHT + "[DEBUG]",Fore.YELLOW + Style.DIM + f"Java Path: {java_path}")
        print(Fore.YELLOW + Style.BRIGHT + "[DEBUG]",Fore.YELLOW + Style.DIM + f"RAM Config: {ram_config}")
        print(Fore.YELLOW + Style.BRIGHT + "[DEBUG]",Fore.YELLOW + Style.DIM + f"Jar Arg.: {jar_config}")
        print(Fore.YELLOW + Style.BRIGHT + "[DEBUG]",Fore.YELLOW + Style.DIM + f"Modloader: {mod_loader_jar}")
        print(Fore.YELLOW + Style.BRIGHT + "[DEBUG]",Fore.YELLOW + Style.DIM + f"GUI Arg.: {gui_config}")
    elif ext_debug == 'false':
        pass

    # start the server, set some variables and start the update thread
    subprocess.Popen(command, cwd=location)
    if close_on_launch == 'true':
        exit_script()
    elif close_on_launch == 'false':
        serverstarting = 1
        serverstatus = "Starting..."
        status_thread = Thread(target=updater.update_status, args=(server,))
        status_thread.start()
        print(Fore.CYAN + Style.BRIGHT + "[LAUNCHPAD]",Fore.CYAN + "starting server...")
    else:
        print(Fore.RED + Style.BRIGHT + "[ERROR]", Fore.RED + f"uh oh")
        return

def shutdown_server():
    global serverstatus, serverwasstopped
    try:
        rcon_instance = MinecraftRCON(RCON_PASSWORD)
        if not rcon_instance.is_server_online():
            messagebox.showinfo("I", "there is no server currently running.")
            return
        serverstatus = "stopping..."
        serverwasstopped = True
        response = rcon_instance.execute_command("stop")
        return "yeah"
    except Exception as e:
        messagebox.showerror("E", f"An error occurred: {e}")

def display_server_details(root, server, ls):
    global current_windowsize
    global is_dsd_open
    global current_serverselect
    previous_windowsize = current_windowsize
    current_windowsize = "800x500"
    is_dsd_open = True

    root.title(f"Server Launch Pad ({server.get('name', 'Unknown')})")
    root.geometry(current_windowsize)

    for widget in root.winfo_children():
        widget.destroy()

    # Background Image Logic
    image = Image.open(background2)
    initial_width = 800  # Width of the window
    initial_height = 500  # Height of the window
    resized_image = image.resize((initial_width, initial_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(resized_image)
    background_label = tk.Label(root, image=photo)
    background_label.image = photo
    background_label.place(relwidth=1, relheight=1)

    # Initial server info
    server_info = "nothing's here... :("

    label = tk.Label(root, text=server_info, font=('Helvetica', 13), justify='center')
    label.pack(pady=10)

    button_font = ('Helvetica', 12)
    button_padx = 10
    button_pady = 5

    btn_launch = tk.Button(root, text="Launch Server", font=button_font, padx=button_padx, pady=button_pady,command=lambda: launch_server(server, ls))
    btn_launch.pack(pady=5)

    btn_shutdown = tk.Button(root, text="Shutdown Server", font=button_font, padx=button_padx, pady=button_pady,command=shutdown_server)
    btn_shutdown.pack(pady=5)

    btn_hide = tk.Button(root, text="Hide GUI", font=button_font, padx=button_padx, pady=button_pady,command=lambda: (root.withdraw()))
    btn_hide.pack(pady=5)

    btn_back = tk.Button(root, text="Back", font=button_font, padx=button_padx, pady=button_pady,command=lambda: (set_is_dsd_open_false(),update_window_size(root, previous_windowsize), display_server_buttons(root, current_server_list, ls)))
    btn_back.pack(pady=5)

    # Start updating the status label
    def update_status_label():
        # Update the server_info text with the latest server status
        if RCON_PASSWORD == serverpanelcreds.MODERNRCONPASSWORD:
            levelnameentry = "level-name=" + get_level_dir(server.get('location') + "/server.properties", "level-name")
        else:
            levelnameentry = "world folder name entry not available in legacy systems"
        server_info = f"""
        Name: {server.get('name', 'Unknown')}
        Location: {server.get('location', 'Unknown')}
        {levelnameentry}
        Description: {server.get('description', 'No description')}
        Minecraft Version: {server.get('minecraft_version', 'Unknown')}
        Mod Loader: {server.get('mod_loader', 'None')}
        Players Online: {serverplayercount} {serverplayernames}
        Server Status: {serverstatus}
        """
        label.config(text=server_info)
        if is_dsd_open:
            root.after(1000, update_status_label)

    update_status_label()

def display_server_buttons(root, server_list, ls):
    global current_server_list
    current_server_list = server_list

    # window customization
    root.title(f"Server Select ({current_serverselect})")
    root.geometry(current_windowsize)

    for widget in root.winfo_children():
        widget.destroy()

    # Background Image Logic
    image = Image.open(background)
    initial_width = 800  # Width of the window
    initial_height = 600  # Height of the window
    resized_image = image.resize((initial_width, initial_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(resized_image)
    background_label = tk.Label(root, image=photo)
    background_label.image = photo
    background_label.place(relwidth=1, relheight=1)

    button_font = ('Helvetica', 16)
    button_padx = 12
    button_pady = 6
    pack_pady = 5

    for server in server_list:
        server_name = server.get('name', 'Unknown Server')
        btn = tk.Button(root, text=server_name, font=button_font, padx=button_padx, pady=button_pady,command=lambda s=server: display_server_details(root, s, ls))
        btn.pack(pady=pack_pady)

    btn_close = tk.Button(root, text="Back", command=lambda: (set_is_dsd_open_false(),update_window_size(root, previous_windowsize), main_menu(root)), font=button_font, padx=button_padx, pady=button_pady)
    btn_close.pack(pady=pack_pady)

def display_settings(root, settings):
    global config
    sdac = config['super-duper-awesome-config']

    root.title(f"Settings {are_modified}")
    root.geometry(current_windowsize)

    for widget in root.winfo_children():
        widget.destroy()

    # Background Image Logic
    image = Image.open(background3)
    initial_width = 1000  # Width of the window
    initial_height = 600  # Height of the window
    resized_image = image.resize((initial_width, initial_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(resized_image)
    background_label = tk.Label(root, image=photo)
    background_label.image = photo
    background_label.place(relwidth=1, relheight=1)

    button_font = ('Helvetica', 16)
    button_padx = 12
    button_pady = 6
    pack_pady = 5

    for key, value in sdac.items():
        btn = tk.Button(root, text=f"{key}: {value}", font=button_font, padx=button_padx, pady=button_pady, command=lambda k=key: toggle_setting(k))
        btn.pack(pady=pack_pady)

    btn_back = tk.Button(root, text="Back", command=go_back, font=button_font, padx=button_padx, pady=button_pady)
    btn_back.pack(pady=pack_pady)

def get_level_dir(file_path, property_name):
    try:
        with open(file_path, "r") as file:
            for line in file:
                # Skip comments and empty lines
                line = line.strip()
                if line.startswith("#") or not line:
                    continue
                # Split the key-value pair
                if "=" in line:
                    key, value = line.split("=", 1)
                    if key.strip() == property_name:
                        return value.strip()
    except FileNotFoundError:
        print(f"[ERROR] The file {file_path} does not exist.")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
    return None

def modern_server_list():
    global current_windowsize
    global RCON_PASSWORD
    global current_serverselect
    from serverpanelcreds import MODERNRCONPASSWORD as RCON_PASSWORD
    current_windowsize = "600x400"
    current_serverselect = "Modern"
    data = load_index(indexpath)
    if data:
        servers = data.get('modern-servers', [])
        display_server_buttons(root, servers, ls)

def legacy_server_list():
    global current_windowsize
    global RCON_PASSWORD
    global current_serverselect
    from serverpanelcreds import LEGACYRCONPASSWORD as RCON_PASSWORD
    current_windowsize = "800x600"
    current_serverselect = "Legacy"
    data = load_index(indexpath)
    if data:
        servers = data.get('legacy-servers', [])
        display_server_buttons(root, servers, ls)

def serverpanel_settings():
    global current_windowsize
    current_windowsize = "800x600"
    data = load_config(configpath)
    if data:
        settings = data.get('[super-duper-awesome-config]', [])
        display_settings(root, settings)

def main_menu(root):
    current_windowsize = previous_windowsize

    # window customization
    root.title("Server Launch Pad by Ayyvery")
    root.geometry(current_windowsize)

    for widget in root.winfo_children():
        widget.destroy()

    # Background Image Logic
    image = Image.open(background)
    initial_width = 800  # Width of the window
    initial_height = 600  # Height of the window
    resized_image = image.resize((initial_width, initial_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(resized_image)
    background_label = tk.Label(root, image=photo)
    background_label.image = photo
    background_label.place(relwidth=1, relheight=1)

    button_font = ('Helvetica', 20)
    button_padx = 12
    button_pady = 6
    pack_pady = 10

    center_window(root)

    btn_legacy = tk.Button(root, text="Legacy Servers", command=legacy_server_list, font=button_font, padx=button_padx, pady=button_pady)
    btn_legacy.pack(pady=pack_pady)

    btn_modern = tk.Button(root, text="Modern Servers", command=modern_server_list, font=button_font, padx=button_padx, pady=button_pady)
    btn_modern.pack(pady=pack_pady)

    btn_settings = tk.Button(root, text="Settings", command=serverpanel_settings, font=button_font, padx=button_padx, pady=button_pady)
    btn_settings.pack(pady=pack_pady)

    btn_close = tk.Button(root, text="Close", command=lambda: (exit_script(root)), font=button_font, padx=button_padx, pady=button_pady)
    btn_close.pack(pady=pack_pady)

def prologue():
    lock.acquire_lock()
    print(Fore.CYAN + Style.BRIGHT + "[LAUNCHPAD]",Fore.CYAN + "hello world!")
    global root
    root = tk.Tk()
    root.title("prologue")
    root.geometry(current_windowsize)
    root.resizable(False, False)

    # start the main menu
    main_menu(root)
    # this is neccecary apparently
    root.mainloop()

if __name__ == "__main__":
    startup()
