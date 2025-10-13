import asyncio
import random
import json
import time
import discord

# Message Handler
async def on_message(bot, message, dragonvars, cooldowns, cooldown_duration):
    if message.author == bot.user:
        return
    # Ignore channels and users as per dragonvars config
    if isinstance(message.channel, discord.TextChannel) and message.channel.id not in dragonvars.reaction_ignore_channels and message.author.id not in dragonvars.reaction_ignore_users:
        await message.add_reaction('🦆')
        await asyncio.sleep(1)
    if isinstance(message.channel, discord.TextChannel) and message.channel.id in dragonvars.mc_news_channel and message.author.id not in dragonvars.reaction_ignore_users:
        upvote = bot.get_emoji(1340093605410242591)
        downvote = bot.get_emoji(1340093666659668081)
        await message.add_reaction(upvote)
        await message.add_reaction(downvote)
    # Custom message responses
    if "smash" in message.content.lower():
        await message.channel.send("pass")
    elif "pass" in message.content.lower():
        await message.channel.send("smash")
    elif "keep your voice down!" in message.content.lower():
        await message.channel.send("Keep your voice down!")
    elif "reshiram" in message.content.lower():
        await message.channel.send(random.choice(dragonvars.reshiram_responses))
    elif "zekrom" in message.content.lower():
        await message.channel.send(random.choice(dragonvars.reshiram_zekrom_responses))
    elif "<@1265643551023169611>" in message.content:
        await message.channel.send(dragonvars.reshiram_ping_response)
    elif any(trigger in message.content.lower() for trigger in dragonvars.zekrom_words):
        await message.channel.send("https://media.discordapp.net/stickers/1311331297234386945.gif")
    elif "i forgor💀" in message.content.lower():
        await message.channel.send(f"nah, you forgor 💀 how to be funny. you forgor 💀 how to be original. you forgor 💀 how to be a decent human being in society.")
    elif "i rember😁" in message.content.lower():
        await message.channel.send(f"yeah, you rember 😁 the reason your parents divorced. you rember 😁 the reason why youre alone. you rember 😁 why nobody likes you. shut up lmao")
    elif any(trigger in message.content.lower() for trigger in dragonvars.weed_words):
        with open(dragonvars.WEED_JSON, "r") as file:
            data = json.load(file)
            image_urls = data.get("weed", [])
        random_url = random.choice(image_urls)
        await message.channel.send(random_url)
    elif "chair" in message.content.lower():
        current_time = time.time()
        last_used = cooldowns.get("chairpasta", 0)
        if current_time - last_used >= cooldown_duration:
            cooldowns["chairpasta"] = current_time
            await message.channel.send(dragonvars.reshiram_chairpasta)
        else:
            await message.add_reaction('⏳')

    # Process commands
    await bot.process_commands(message)