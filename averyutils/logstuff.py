"""lightweight custom logger"""
from averyutils import avery_logger
_log = avery_logger
try:
    import logging as _logging
    import logging.handlers as _loghand
    import colorama as _colorama
    import re as _re
    import threading as _threading
    import traceback as _traceback
    from typing import *
    from pathlib import Path
except ImportError as e:
    print(e.name, "is not installed")
    _log.error(f"{e.name} not installed")


_pl = _threading.Lock()
def lprint(*args, **kwargs):
    """a locked print function, preventing two print calls from occouring at the same time"""
    try:
        _pl.acquire()
        print(*args, **kwargs)
    finally:
        _pl.release()

_default_logit_map = {
    "info": {"logging": _logging.INFO, "colorama": _colorama.Fore.GREEN},
    "warn": {"logging": _logging.WARNING, "colorama": _colorama.Fore.YELLOW},
    "error": {"logging": _logging.ERROR, "colorama": _colorama.Fore.RED},
    "debug": {"logging": _logging.DEBUG, "colorama": _colorama.Fore.BLUE},
    }
_reset = _colorama.Style.RESET_ALL

class LogitConfig:
    def __init__(self):
        self._llim = _default_logit_map
        self._vprntr = print
        self._prfx = ""
        self._sffx = ""
        self._lvl = False
        self._lgr = _logging.Logger(name="averyutils.logstuff", level=_logging.NOTSET)
        self._lck = _threading.Lock()
        _log.debug("initialized logit config")

    @property
    def logger(self) -> _logging.Logger:
        return self._lgr

    @property
    def printer(self) -> Callable:
        return self._vprntr
    @property
    def level_map(self) -> dict:
        return self._llim

    @property
    def prefix(self) -> str:
        return self._prfx

    @property
    def suffix(self) -> str:
        return self._sffx

    def set_message_format(self, prefix:Optional[str]="", suffix:Optional[str]="", show_level:Optional[bool]=False):
        """configure how messages should be formatted, with things like prefixes ([prefix] hello world!), suffixes (hello world! {suffix}) and more"""
        self._prfx = prefix
        self._sffx = suffix
        self._lvl = show_level
        return self

    def add_custom_logit_map(self, cmap:dict):
        """add a custom logit dictionairy
        format:
        {
            "level": {
                "logging": logging.LEVEL,
                "colorama": colorama.Fore or colorama.Style
            },
            "example_level": {
                "logging": logging.INFO,
                "colorama": colorama.Fore.CYAN
            }
        }
        """
        for k, v in cmap.items():
            if k in self._llim:
                raise KeyError(f"level [{k}] already exists in logit_level_map")
        self._llim.update(cmap)
        return self

    def add_logging_logger(self, logger:_logging.Logger):
        self._lgr = logger
        return self

    def change_logit_printer(self, printer:Callable):
        """
            change the function Logit uses to print logs
        default is builtins.print
        """
        self._vprntr = printer
        return self

config = LogitConfig()

class LogitUtils:
    def __init__(self):
        self.ansi_escape = _re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        _log.debug("initialized logit utils")

    def getloggersimple(
        self,
        name:str,
        filepath:Union[str, Path],
        level:Optional["logging.Level"]=_logging.DEBUG
        ) -> _logging.Logger:
        """
            a very simple one-liner to get a logging.Logger object
            the only things it needs is the name of the logger and the path where the logfile will be created
            """
        # normalize paths
        if not isinstance(filepath, Path):
            filepath = Path(filepath)
        # add the .log extension if it wasnt provided
        if not filepath.name.endswith(".log"):
            filepath = filepath.with_suffix(".log")
        filepath = filepath.absolute()
        logger = _logging.getLogger(name=name)
        logger.setLevel(level=level)
        handler = _loghand.RotatingFileHandler(
            filename=filepath,
            mode="w",
            encoding='utf-8',
            delay=True)
        handler.setFormatter(
            _logging.Formatter(
                fmt="%(asctime)s %(levelname)s %(message)s"
                )
            )
        logger.addHandler(handler)
        return logger

    def getsuffix(self) -> str:
        return ('[' + config.suffix + ']') if config.suffix else ''

    def getprefix(self) -> str:
        return (config.prefix + '/') if config.prefix else ''

    def getlevel(self, lvl) -> str:
        """returns the provided level only if the config allows for it"""
        return lvl if config._lvl else ""

    def getcleanmsg(self, msg:str) -> str:
        """returns a copy of the provided string devoid of any ansi escapes"""
        return self.ansi_escape.sub('', msg)

utils = LogitUtils()

def logit(level:Literal["info", "warn", "error", "debug"], message:str, **options):
    """
        wrapper for handling color, printing, logging and more
        options:
            format:str - formatting rule (default:"all" options: "all", "limited", "none")
            error:BaseException - an exception to log/trace (default:None)
    """
    _will_be_logged = _will_be_printed = True
    _add_ons = []
    with config._lck:
        # get the level info
        Linf = config.level_map[level]

        # get context from options
        err = options.get("error", None)
        fmt = options.get("format", "all") # options: all, limited, none

        # base vars for con and log
        con_msg, log_msg = message, message
        if err:
            trace = "".join(_traceback.format_exception(type(err), err, err.__traceback__))
            log_msg += "\n" + trace
            _add_ons.append(trace)


        colour = Linf["colorama"]
        branding = '[' + utils.getprefix() + utils.getlevel(level) + ']'
        if fmt == "all": # add 'all' formatting
            con_msg = colour + branding + _reset + " " + con_msg + " ".join(_add_ons) + utils.getsuffix()
        elif fmt == "limited":
            con_msg = colour + branding + _reset + " " + con_msg
        elif fmt == "none":
            pass
        else:
            raise ValueError(f"unexpected fmt value of {fmt} must be any of the following: 'all', 'limited', 'none'")

        if _will_be_printed:
            config.printer(con_msg)
        if _will_be_logged:
            config.logger.log(level=Linf["logging"], msg=utils.getcleanmsg(msg=log_msg))