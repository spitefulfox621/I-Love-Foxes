"""avery?!
daz me! i'm avery!
"""
import os
import logging




environ = os.path.abspath(os.getenv("SPITEFOX_DIR", os.getcwd()))
os.makedirs(environ, exist_ok=True)
logdir = os.path.join(environ, "aVyUTils")
os.makedirs(logdir, exist_ok=True)
logfile = os.path.join(logdir, "ave.ry")

avery_logger = logging.getLogger("averyutils")
avery_logger.setLevel(logging.DEBUG)
_handler = logging.FileHandler(
    filename=logfile,
    mode="w",
    encoding="utf-8",
    delay=True)
_handler.setFormatter(fmt=logging.Formatter(fmt="%(asctime)-23s %(levelname)-8s %(filename)-12s - %(message)s"))
avery_logger.addHandler(_handler)
from .dni.branding import he_really_is
avery_logger.info(he_really_is)
