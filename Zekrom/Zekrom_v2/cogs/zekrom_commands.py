"""
slash commands for Zekrom\n
"""
from components.Zekrom_Furfag import furfag
import os
import time
import uuid
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View

class Zekrom_Slash_Command_Handler(commands.Cog, name='Zekrom Commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await furfag.firLoggers("DISCORD", "D", f"{self.qualified_name} is ready")

    async def cog_load(self):
        await furfag.firLoggers("DISCORD", "D", f"{self.qualified_name} loaded")

    async def cog_unload(self):
        await furfag.firLoggers("DISCORD", "D", f"{self.qualified_name} unloaded")

    @commands.command()
    async def kys(self, ctx):
        await ctx.reply('alright, geez...')
        await self.bot.change_presence(status=discord.Status.dnd,activity=discord.CustomActivity(name="💤 shutting down..."))
        await self.bot.close()
        exit()

async def setup(bot):
    await bot.add_cog(Zekrom_Slash_Command_Handler(bot))