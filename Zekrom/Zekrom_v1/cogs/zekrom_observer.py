import os
from discord.ext import commands

from components.Zekrom_Furfag import furfag

class Zekrom_Observer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await furfag.firLoggers( "DISCORD", "I", f"{os.path.splitext(os.path.basename(__file__))[0].lower()} is ready")

    async def cog_load(self):
        await furfag.firLoggers( "DISCORD", "I", f"{os.path.splitext(os.path.basename(__file__))[0].lower()} loaded")

    @commands.Cog.listener()
    async def on_connect(self):
        await furfag.firLoggers("DISCORD", "I", "connected to discord")

    @commands.Cog.listener()
    async def on_disconnect(self):
        await furfag.firLoggers("DISCORD", "E", "disconnected from discord")

    @commands.Cog.listener()
    async def on_resumed(self):
        await furfag.firLoggers("DISCORD", "W", "resumed session")

async def setup(bot):
    await bot.add_cog(Zekrom_Observer(bot))