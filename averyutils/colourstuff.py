from averyutils import avery_logger
_log = avery_logger

try:
    import sys, re
    # from colorama import Fore, Style
    coloramaPresent = False
except ImportError as e:
    print(e.name, "is not installed")
    _log.error(f"{e.name} not installed")
    coloramaPresent = False

class COLORCONFIG:
    ColorTagPattern = re.compile(r"\[(/?)([a-zA-Z]+)\]")
    if coloramaPresent:
        ColorTags: dict = {
            "black": Fore.BLACK,
            "red": Fore.RED,
            "green": Fore.GREEN,
            "yellow": Fore.YELLOW,
            "blue": Fore.BLUE,
            "magenta": Fore.MAGENTA,
            "cyan": Fore.CYAN,
            "white": Fore.WHITE,
            "reset": Fore.RESET,
            "bright": Style.BRIGHT,
            "normal": Style.NORMAL,
            "dim": Style.DIM,
            "reset_all": Style.RESET_ALL
        }
    else:
        ColorTags: dict = {
            "black": "\033[30m",
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
            "white": "\033[37m",
            "reset": "\033[0m",
        }
    _log.debug("initialized color config")

config = COLORCONFIG()

class COLORUTILS:
    _log.debug("initialized color utils")
    @staticmethod
    def parse_color_tags(s: str) -> str:
        """
        Replace tags like [red] and [/red] (or [reset]) with ANSI codes.
        """
        def repl(match):
            slash, name = match.group(1), match.group(2).lower()
            if slash:  # e.g. [/red]
                return config.ColorTags.get("reset", "")
            else:
                return config.ColorTags.get(name, "")
        return config.ColorTagPattern.sub(repl, s) + config.ColorTags.get("reset", "")

utils = COLORUTILS()

def fmt_color(s: str) -> "ANSI String":
    """formats a string to be coloured, tags like [red] or [bright](colorama only) get replaced with ansi codes"""
    def repl(match):
        slash, name = match.group(1), match.group(2).lower()
        if slash:
            return config.ColorTags.get("reset", "")
        else:
            return config.ColorTags.get(name, "")
    return config.ColorTagPattern.sub(repl, s) + config.ColorTags.get("reset", "")

def cprint(*objects: object):
    """coloured printing with simple tags like [red] [green] [blue]"""
    s = ""
    for o in objects:
        s += fmt_color(str(o))
        s += " "
    sys.stdout.write(s)
    sys.stdout.write("\n")