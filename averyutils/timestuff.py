"""timing based utilities"""
from averyutils import avery_logger
_log = avery_logger
try:
    import time
except ImportError as e:
    print(e.name, "is not installed")
    print("how the fuck do you manage to not have time installed? what is wrong with you?! IT'S A DEFAULT LIBRARY. IT'S BUILTIN. DUDE. WHAT.")
    _log.error(f"{e.name} not installed")

class TimerConfig:
    timers: dict = {}
    def __init__(self):
        _log.info("initialized logit config")

config = TimerConfig()

class Timer:
    def start(self, name:str):
        self.timers[name] = time.time()

    def stop(self, name:str):
        if name in self.timers:
            _t = self.timers.pop(name)
            _e = time.time() - _t
            return _e
        else:
            return None

timeit = Timer()