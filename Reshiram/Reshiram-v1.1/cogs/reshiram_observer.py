"""
event listener for Reshiram\n
very cool
"""

import os, random, time, asyncio
from discord.ext import commands

from components.Reshiram_Furfag import furfag

class Reshiram_Observer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await furfag.firLoggers("DISCORD", "I", f"{os.path.splitext(os.path.basename(__file__))[0].lower()} is ready")

    async def cog_load(self):
        await furfag.firLoggers("DISCORD", "I", f"{os.path.splitext(os.path.basename(__file__))[0].lower()} loaded")

    @commands.Cog.listener()
    async def on_connect(self):
        await furfag.firLoggers("DISCORD", "I", "connected to discord")

    @commands.Cog.listener()
    async def on_disconnect(self):
        await furfag.firLoggers("DISCORD", "E", "disconnected from discord")

    @commands.Cog.listener()
    async def on_resumed(self):
        await furfag.firLoggers("DISCORD", "W", "resumed session")
        await self.bot.reshiram_channel.send("blacked out for a sec.. what happened?!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await furfag.firLoggers("DISCORD", "W", f"{member} joined")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await furfag.firLoggers("DISCORD", "W", f"{member} left")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        await furfag.firLoggers("DISCORD", "W", f"{user} just got banned from {guild}")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        await furfag.firLoggers("DISCORD", "W", f"{user} just got un-banned from {guild}")

    @commands.Cog.listener()
    async def on_guild_available(self, guild):
        await furfag.firLoggers("DISCORD", "I", f"{guild} is available! :3")

    @commands.Cog.listener()
    async def on_guild_unavailable(self, guild):
        await furfag.firLoggers("DISCORD", "E", f"{guild} is not available! :c")

    @commands.Cog.listener()
    async def is_ws_ratelimited(self):
        await furfag.firLoggers("DISCORD", "W", f"we are being cockblocked (rate limited)")

    async def on_error(self, event, *args, **kwargs):
        await furfag.firLoggers("DISCORD", "E", f"AN ERROR HAPPENED. SOMEWHERE.\n{event} - {args} - {kwargs}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("the fuck did you just say to me?")
            await furfag.firLoggers("DISCORD", "E", f"idk what the fuck this means: {error}")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("what")
            await furfag.firLoggers("DISCORD", "E", f"give me more data dawg: {error}")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("hey! you can't do that! >:c")
            await furfag.firLoggers("DISCORD", "E", f"YOU CAN'T DO THAT MAN: {error}")
        elif isinstance(error, commands.CommandOnCooldown):
            cooldown_end = int(time.time() + error.retry_after)
            msg = await ctx.send(f"s-slown down {ctx.author}-kun.. hngghh... try again <t:{cooldown_end}:R>...")
            await furfag.firLoggers("DISCORD", "E", f"rape limited LOL:{error}")
            await asyncio.sleep(error.retry_after)
            await msg.delete()
        else:
            await ctx.send("erm, what the sigma...")
            await furfag.firLoggers("DISCORD", "E", f"Error in command {ctx.command}: {error}")

class Reshiram_Message_Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        ctx = await self.bot.get_context(before)
        if before.author == self.bot.user or before.author.bot or before.content == "" or ctx.valid or "https://" in before.content:
            return
        woah_i_logged_that = f"{before.author.nick} — <t:{int(before.created_at.timestamp())}:t>\n{before.content}"
        await before.channel.send(content=woah_i_logged_that)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        ctx = await self.bot.get_context(message)
        if message.author.bot or message.content == "" or ctx.valid or "https://" in message.content:
            return
        await message.channel.send(content=f"alright then, keep your secrets {message.author.mention}")

    @commands.Cog.listener()
    async def on_message(self, message): # message handler courtesy of Risumies <3
        if message.channel.id == furfag.config["channel-ids"]["minecraft_news_channel"]:
            await message.add_reaction(self.bot.get_emoji(1340093605410242591))
            await message.add_reaction(self.bot.get_emoji(1340093666659668081))
            return

        ctx = await self.bot.get_context(message)
        if message.author == self.bot.user or message.author.bot or message.content == "" or ctx.valid or "https://" in message.content:
            return

        # helpers
        def word(*triggers):
            return lambda: any(trigger in message.content.lower() for trigger in triggers)

        def cond(predicate):
            return predicate

        def chance(amount):
            return lambda: random.random() < amount

        def or_merge(*predicates):
            return lambda: any(predicate() for predicate in predicates)

        def and_merge(*predicates):
            return lambda: all(predicate() for predicate in predicates)

        def resp(*args):
            async def inner():
                response = random.choice(args)
                await message.channel.send(response)
            return inner

        keyword_map = {
            ### custom response creation
            chance(0.01):                                                                                                           lambda: self.bot.REF.custom_response(message, 'random'),
            word("chair"):                                                                                                          lambda: self.bot.REF.custom_response(message, 'chair'),
            word(*furfag.config["trigger-words"]["weed_words"]):                                                                    lambda: self.bot.REF.custom_response(message, 'weed_cat'),
            word(*furfag.config["trigger-words"]["cat_words"]):                                                                     lambda: self.bot.REF.custom_response(message, 'reddit_cat'),
            and_merge(cond(lambda: True if furfag.config["settings"]["reshiram_ai_enabled"] is True else False), chance(0.05)):     lambda: self.bot.REF.custom_response(message, 'ai_reshi'),
            cond(lambda: len(message.content) > 300):                                                                               resp("I ain't reading allat bro 💀", "holy yap", "ts pmo icl"),

            ### single trigger, single response
            word("i forgor💀"):                                                                                                     resp("nah, you forgor 💀 how to be funny. you forgor 💀 how to be original. you forgor 💀 how to be a decent human being in society."),
            word("i rember😁"):                                                                                                     resp("yeah, you rember 😁 the reason your parents divorced. you rember 😁 the reason why youre alone. you rember 😁 why nobody likes you. shut up lmao"),
            word("avery"):                                                                                                          resp("avery? fuck that guy"),
            word("smash"):                                                                                                          resp("pass"),
            word("pass"):                                                                                                           resp("smash"),
            word("femboy"):                                                                                                         resp("FEMBOY? AWOOGA!!!!!!!!!!!!!!"),
            word("poggies"):                                                                                                        resp("``'PLAP ' * 400``" if random.random() < 0.1 else "PLAP " * 400),
            word("keep your voice down!"):                                                                                          resp("Keep your voice down!"),
            word("i love you"):                                                                                                     resp("gross, get a room"),
            word("reshiram"):                                                                                                       resp(*furfag.config["response-messages"]["reshiram_mentioned_messages"]),
            word("zekrom"):                                                                                                         resp(*furfag.config["response-messages"]["zekrom_mentioned_messages"]),


            ### examples ###
            ## many triggers, many responses
            # word("reshiram", "", "thank you", "..."): resp("ok?", "sure ig...", "..."),
            ## merged conditions:
            # should prob at the bottom, cuz this can execute randomly if the dice roll is lucky
            # or_merge(word("reshiram", "zekrom"), chance(0.1)): resp("reshiram or zekrom"),
            ## another example
            # condition(lambda: self.Reshi.user in message.mentions): resp("who pigged me")
        }

        for condition, handler in keyword_map.items():
            if condition():
                response = await handler()
                if response:
                    await message.channel.send(content=response)
                else:
                    break

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji == '🤓':
            if reaction.message.author == self.bot.user:
                await reaction.message.channel.send("don't you dare 🤓 me")

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        if random.random() < 0.01:
            await self.bot.get_channel(channel.id).send(f"don't even bother typing, {user}. you just be yapping bruh")

async def setup(bot):
    await bot.add_cog(Reshiram_Observer(bot))
    await bot.add_cog(Reshiram_Message_Handler(bot))