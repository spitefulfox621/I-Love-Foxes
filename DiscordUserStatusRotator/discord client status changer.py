import asyncio, re, json, aiohttp, colorama, itertools, traceback, random
colorama.init(autoreset=True)
status_pattern = re.compile(r'^\[(?P<status>\w+)\]\s*(?:(?P<emoji>(?:<a?:\w+:\d+>))\s*)?(?P<message>.+)$')
discord_pattern = pattern = re.compile(r'^<(?P<animated>a?):(?P<name>\w+):(?P<id>\d+)>$')

######## config section ########################################################################
try:
    config = json.load(open("dcsc_config.json", "r", encoding="utf-8"))
except:
    config = {
        "_modes": ["cycle", "random"],
        "_version": 1.1,
        "token": "YOUR_TOKEN_HERE",
        "sleep_interval": 3600,
        "api_url": "https://discord.com/api/v10/users/@me/settings",
        "mode": "cycle",
        "statuses": [
            "[dnd] example status",
            "[idle] <:wave:123456789123456789> status with a custom emoji",
            "[invisible] <a:waving:123456789123456789> status with a custom animated emoji",
            ]
        }
finally:
    json.dump(config, open("dcsc_config.json", "w", encoding="utf-8"), indent=2)
######## config section ########################################################################

######## main code section #################################################################################################################################
async def change_status(session:aiohttp.ClientSession, status_inf:dict={"status": str, "message": str}, emoji:dict={"name":str, "id":str, "animated":bool}):
    status = str(status_inf.get("status"))
    text = str(status_inf.get("message"))
    emoji_name = emoji.get("name")
    emoji_id = emoji.get("id")
    emoji_animated = emoji.get("animated")
    header = {"Authorization": config["token"]}
    jsondata = {
        "status": status,
        "custom_status": {
            "text": text,
            "emoji_name": emoji_name if emoji_name is not None else None,
            "emoji_id": emoji_id if emoji_id is not None else None,
            "emoji_animated": emoji_animated if emoji_animated is not None else False,
            }
        }
    try:
        resp = await session.patch(url=config["api_url"], headers=header, json=jsondata)
        color = (colorama.Fore.GREEN) if resp.status == 200 else (colorama.Fore.YELLOW)
        print(color + f"[{resp.status} {resp.reason}] ([{status}] {text}) next status in {config["sleep_interval"]} seconds")
        if resp.status != 200:
            data = await resp.json()
            try:
                err_msg, err_issue = data.get("message"), data.get("errors")
                print(color + f"    {err_msg} {err_issue}")
            except:
                raise
    except Exception as e:
        print(colorama.Fore.RED + f"FUCK\n{e}")

async def updater_loop():
    print(colorama.Fore.BLUE + f"status changer {colorama.Fore.GREEN}v{config["_version"]}{colorama.Fore.BLUE} by {colorama.Fore.MAGENTA}Ayyvery", "\n", "press ctr+c to exit")
    print(colorama.Fore.CYAN + f"""config:
    token: {'*' * len(config["token"])}
    cycle mode: {config["mode"]}
    cycle interval: {config["sleep_interval"]}
    """)
    session = aiohttp.ClientSession()
    if config["mode"] == "cycle":
        statuses = itertools.cycle(config["statuses"])
        statusgetter = lambda: next(statuses)
    elif config["mode"] == "random":
        statusgetter = lambda: random.choice(config["statuses"])
    while True:
        status, emoji_name, emoji_id, emoji_animated, message = process_status(statusgetter())
        if status:
            await change_status(session=session, status_inf={"status": status, "message": message}, emoji={"name": emoji_name, "id": emoji_id, "animated": emoji_animated})
            await asyncio.sleep(config["sleep_interval"])
        else:
            raise Warning("status didn't match pattern")
######## main code section #################################################################################################################################

######## helper code section #############################################
def process_status(text):
    """Processes a status line"""
    _status = _emoji_name = _emoji_id = _emoji_animated = _message = None
    match = status_pattern.match(text)
    if match:
        m = match.groupdict()
        _status = m.get("status")
        _maybe_emoji = m.get("emoji")
        _message = m.get("message")
        if _maybe_emoji:
            discord_match = discord_pattern.match(_maybe_emoji)
            if discord_match:
                d = discord_match.groupdict()
                _emoji_animated = d.get("animated")
                _emoji_name = d.get("name")
                _emoji_id = d.get("id")
    return _status, _emoji_name, _emoji_id, _emoji_animated, _message
######## helper code section #############################################

try:
    asyncio.run(updater_loop())
except KeyboardInterrupt:
    print(colorama.Fore.BLUE + "exiting...")
    exit()
except Warning as w:
    print(colorama.Fore.YELLOW + f"warning: {traceback.format_exc()}")
except Exception as e:
    print(colorama.Fore.RED + f"exception: {traceback.format_exc()}")
except BaseException as b:
    print(colorama.Fore.RED + colorama.Style.BRIGHT + f"error: {traceback.format_exc()}")
    exit()