import discord
import socket
import asyncio
import random
import json
import time
import subprocess
import sys
import os
import aiohttp
from mcstatus import JavaServer
from discord.ext import commands
from discord import Webhook
import dragonvars
import commands as bot_commands

def setup(bot, dragonvars):

### Minecraft Commands
    @bot.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def minecraft(ctx, port: str = "25565"):
        if ctx.channel.id not in dragonvars.mc_channel:
            await ctx.message.add_reaction("❌")
            await asyncio.sleep(5)
            await ctx.message.delete()
            return False

        server_adress = f"{dragonvars.hostname}:{port}"
        server = JavaServer.lookup(server_adress)
        status = server.status()
        latency = server.ping()

        embed = discord.Embed(title="Minecraft Server Info", color=discord.Color.green())
        embed.set_author(name="Ayyvery", url="https://awooga.free.nf/contact", icon_url="https://iili.io/2RwXf87.webp")
        embed.add_field(name="Hostname", value=f"{dragonvars.hostname}", inline=False)
        embed.add_field(name="Ping", value=f"{latency:.2f}ms", inline=False)
        embed.add_field(name="Latency", value=f"{status.latency:.2f}", inline=False)
        embed.add_field(name="Players", value=f"{status.players.online}", inline=False)
        embed.set_footer(text="this message will self destruct in 2 minutes.", icon_url="https://iili.io/2RwVaUP.webp")
        bot_embed = await ctx.send(embed=embed)
        await asyncio.sleep(120)
        await ctx.message.delete()
        await bot_embed.delete()

### Utility Commands
    @bot.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def ping(ctx):
        latency = bot.latency * 1000
        await ctx.send(f"Pong! {latency:.2f}ms")

    @bot.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def boykisser(ctx):
        await ctx.send("awakening the creature...")
        try:
            subprocess.Popen(
            ["cmd", "/c", os.path.abspath("../../MusicBot/run.bat")],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True
            )
        except Exception as e:
            await reshiram.send_error_webhook()

    @bot.command()
    async def addvote(interaction: discord.Interaction, message_id: int):
        try:
            await interaction.message.delete()
            message = await interaction.channel.fetch_message(message_id)
            upvote = bot.get_emoji(1340093605410242591)
            downvote = bot.get_emoji(1340093666659668081)
            await message.add_reaction(upvote)
            await message.add_reaction(downvote)
        except Exception as e:
            await reshiram.send_error_webhook()

### Fun Commands
    @bot.command()
    async def ask(ctx, *, question: str):
        answer = random.choice(dragonvars.answers)
        emotion = random.choice(dragonvars.emotions)
        response = f"**Question**: {question}\n**Answer**: {answer} {emotion}"
        await ctx.send(response)

    @bot.command()
    @commands.cooldown(10, 120, commands.BucketType.user)
    async def reshirammed(ctx):
        with open(dragonvars.RESHIRAMMED_JSON_FILE, "r") as file:
            data = json.load(file)
            image_urls = data.get("images", [])
            await ctx.send(random.choice(image_urls))

    @bot.command()
    async def sprigatito(ctx):
        params = {"tags": "sprigatito solo pokemon(species)","limit": 500}
        async with aiohttp.ClientSession(headers=dragonvars.headers) as session:
            async with session.get(dragonvars.e926_api_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    posts = data.get("posts", [])
                    if not posts:
                        await ctx.send(f"No results found! {params}")
                        return
                    post = random.choice(posts)
                    image_url = post.get("file", {}).get("url")
                    if image_url:
                        await ctx.send(image_url)
                    else:
                        await reshiram.send_error_webhook()

### Admid Commands
    @bot.command()
    @commands.has_permissions(administrator=True)
    async def deactivate(ctx):
        print("shutting down...")
        await ctx.send("Reshiram: Deactivated")
        await bot.close()
        sys.exit()