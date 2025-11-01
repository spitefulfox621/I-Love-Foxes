"""sound stuff that sounds like stuff that has to do with sound"""
############################################
from averyutils import avery_logger
_log = avery_logger
try:
    import os, time, random, pygame
except ImportError as e:
    print(e.name, "is not installed")
    _log.error(f"{e.name} not installed")
############################################

# initialization
pygame.mixer.init()

# config
class SoundConfig:
    channels: dict = {
        0: pygame.mixer.Channel(0),
        1: pygame.mixer.Channel(1),
        }
    soundcache: dict = {}
    def __init__(self):
        _log.debug("initialized sound config")

    def add_channel(self):
        existing = len(self.channels) - 1 # starting from 0
        new = existing + 1
        self.channels[new] = pygame.mixer.Channel(new)
        _log.debug(f"adding new channel, channel count is now {len(self.channels)}")

# config instance
config = SoundConfig()

class SoundUtils:
    def __init__(self):
        _log.debug("initialized sound utils")

    def get_all_channels(self) -> list:
        return [c for i, c in config.channels.items()]

    def get_channel_by_id(self, channelId: int) -> pygame.mixer.Channel:
        return config.channels.get(channelId)

    def get_channel_count(self) -> int:
        return len(config.channels)

utils = SoundUtils()



def play(filepath: str, volume: float=0.5, channel: int=0):
    """play an audio file"""
    p = os.path.abspath(filepath)
    s = config.soundcache.get(p)
    if not s:
        s = pygame.mixer.Sound(p)
        config.soundcache[p] = s
    c = utils.get_channel_by_id(channel)
    c.set_volume(volume)
    c.play(s)
    _log.debug(f"playing sound {p}")
    return c

def wait(channel: int=0):
    """blocking call that waits for a channel to finish playback"""
    c = utils.get_channel_by_id(channel)
    while c.get_busy():
        time.sleep(0.1)
def wait_all():
    """blocking call that waits for all channels to finish playback"""
    for c in utils.get_all_channels():
        while c.get_busy():
            time.sleep(0.1)