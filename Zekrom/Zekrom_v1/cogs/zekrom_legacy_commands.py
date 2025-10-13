import os, random

from discord.ext import commands

from components.Zekrom_Furfag import furfag

class Zekrom_Command_Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await furfag.firLoggers( "DISCORD", "I", f"{os.path.splitext(os.path.basename(__file__))[0].lower()} is ready")

    async def cog_load(self):
        await furfag.firLoggers( "DISCORD", "I", f"{os.path.splitext(os.path.basename(__file__))[0].lower()} loaded")

    @commands.command()
    async def ask(self, ctx, *, question):
        await ctx.send(random.choice(["yeah like ima tell you LMFAO", "uh idk", "wouldn't you like to know, weather boy"]))

    @commands.command()
    async def showmeyourcache(self, ctx):
        await ctx.send(f"no, fuck off.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reconnect(self, ctx):
        await self.bot.ws.close(code=4000)

async def setup(bot):
    await bot.add_cog(Zekrom_Command_Handler(bot))