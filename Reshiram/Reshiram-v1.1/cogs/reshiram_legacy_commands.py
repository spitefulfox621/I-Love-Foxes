"""
prefix(r!) commands for Reshiram
"""
from spiteƒox import spitefox
import os, json, random, asyncio, aiofiles, io, uuid

import discord
from discord import File
from discord.ext import commands
from discord.ui import Button, View
#from discord import app_commands

from components.Reshiram_Furfag import furfag
view = View()

class Reshiram_Legacy_Init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await furfag.firLoggers("DISCORD", "I", f"{os.path.splitext(os.path.basename(__file__))[0].lower()} is ready")

    async def cog_load(self):
        await furfag.firLoggers("DISCORD", "I", f"{os.path.splitext(os.path.basename(__file__))[0].lower()} loaded")

class Reshiram_Command_Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ask(self, ctx, *, question):
        await ctx.send(f"**Question:** {question}\n**Answer:** {random.choice(furfag.config["response-messages"]["answers"])} {random.choice(furfag.config["response-messages"]["emotions"])}")

    @commands.command(aliases=["rammed"])
    @commands.cooldown(10, 120, commands.BucketType.user)
    async def reshirammed(self,ctx):
        try:
            if not os.path.exists(os.path.join(self.bot.cache_path, "pokemon_sprites.json")):
                await self.bot.RWR.cache_pokemon_sprites(self.bot.cache_path)
        except Exception as e:
            await furfag.firLoggers("DISCORD", "E", f"an error occoured bruh {e}")
        finally:
            async with aiofiles.open(os.path.join(self.bot.cache_path, "pokemon_sprites.json"), "r") as file:
                pokemon_sprites = await file.read()
                pokemon_sprites_jsonified = json.loads(pokemon_sprites)
                await ctx.send(random.choice(list(pokemon_sprites_jsonified.values())))

    @commands.command()
    async def rape(self, ctx, victim: discord.Member): # github will love this one
        await ctx.send(f"**{ctx.author}** is raping **{victim}**")

    @commands.command()
    async def halfrape(self, ctx, quote_unquote_victim: discord.Member):
        await ctx.send(f"**{ctx.author}** is having wild(but loving) sex with **{quote_unquote_victim}**")

    @commands.command()
    async def notrape(self, ctx, enjoyer: discord.Member):
        await ctx.send(f"**{ctx.author}** is having gentle and loving sex with **{enjoyer}**")

    @commands.command(aliases=["nf"])
    async def new_features(self, ctx): # TODO: rewrite
        new_features_file_path = os.path.join(spitefox.locations.spitefox_dir_p, furfag.client, "new features.json")
        try:
            async with aiofiles.open(new_features_file_path, "r", encoding='utf8') as nf:
                newfeatures = await nf.read()
                data = json.loads(newfeatures)
                user_list = (list(set([(f"{item['user']}") for item in data])))
                grouped = {}
                for item in data:
                    user = item['user']
                    suggestion = item['suggestion']
                    status = item['status']
                    if user not in grouped:
                        grouped[user] = []
                    grouped[user].append((suggestion, status))

                suggestion_list = []
                for user, suggestions in grouped.items():
                    entry = "\n".join(f"- {suggestion}\n • (status: ``{status}``)" for suggestion, status in suggestions)
                    suggestion_list.append((user, entry, False))

                if user_list:
                    if len(user_list) == 1:
                        suggesters = user_list[0]
                    elif len(user_list) == 2:
                        suggesters = " and ".join(user_list)
                    else:
                        suggesters = f"{', '.join(user_list[:-1])} and {user_list[-1]}"

                nf_author=(f"New Features", "https://awooga.free.nf/localfoxgames.net", "https://iili.io/3cuA172.png")
                nf_body=(f"{self.bot.reshiram_badge}", "", f"you got suggestions from ``{suggesters}``!", 0x00bfe6)
                nf_fields=suggestion_list
                nf_images=("", "https://iili.io/3cJwzU7.png")
                nf_footer=(f"✅", "")

        except Exception as e:
            await furfag.firLoggers("DISCORD", "E", f"no new features for you bud: {e}")
            nf_author = (f"New Features", "https://awooga.free.nf", "https://iili.io/3cuA172.png")
            nf_body = (f"{self.bot.reshiram_badge}", "", "", 0x781313)
            nf_fields = [("an error occoured", f"error message: {e}", False)]
            nf_images = ("", "https://iili.io/3cmNr3x.png")
            nf_footer = (f"❌", "")

        finally:
            embed = await self.bot.REF2.Webhook_Maker(
                author=nf_author,
                body=nf_body,
                fields=nf_fields,
                images=nf_images,
                footer=nf_footer,
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def reshi_tits(self, ctx, service = None, voice = None, *, speakify: str):
        """service - sex"""
        data = await self.bot.RWR.lazypyro_request(service=service, voice=voice, message=speakify)
        if data:
            filename = f"{uuid.uuid4()}.mp3"
            file = File(io.BytesIO(data), filename=filename)
        await ctx.channel.send_voice_message(file)

class Reshiram_Legacy_Minecraft_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['gsc'])
    async def get_server_count(self, ctx):
        data, status_code, reason = await self.bot.RMR.get_server_count(0)
        await ctx.send(f"``{data['count']}`` servers registered on ``{furfag.config["urls"]["hostname"]}``\n-# {status_code} {reason}")

    @commands.command(aliases=['gav'])
    @commands.has_permissions(administrator=True)
    async def get_api_ver(self, ctx): # TODO: rewrite
        reshimessage = await ctx.send("Reshiram is thinking...")
        try:
            api_version, status_code, reason = await self.bot.RMR.get_api_version()
            if status_code == 200:
                await reshimessage.edit(content=f"server responded, constructing server list...\n-# {status_code} {reason}")
                field_list = []
                api_version.update({"theFogIsComing":True})
                for k, v in api_version.items(): # (k, v, True) for k, v in api_version.items()
                    if k == 'isDevBuild':
                        k_emoji = '🖥️'
                    elif k == 'mcssVersion':
                        k_emoji = '🔰'
                    elif k == 'mcssApiVersion':
                        k_emoji = '✒️'
                    elif k == 'uniqueIdentifier':
                        k_emoji = '❗'
                    elif k == 'youAreAwesome':
                        k_emoji = '😻'
                    elif k == 'theFogIsComing':
                        k_emoji = self.bot.thefogiscoming
                    else:
                        k_emoji = '💭'

                    if v is True:
                        v_emoji = '✅'
                    elif v is False:
                        v_emoji = '❌'
                    elif any(char.isdigit() for char in v) and k != 'uniqueIdentifier':
                        v_emoji = '🌡️'
                    else:
                        v_emoji = '💭'

                    if k == 'theFogIsComing':
                        suffix = '-# (entry not by MCSS)'
                    else:
                        suffix = ''

                    field1 = f"{k_emoji} {k}"
                    field2 = f"-# {v_emoji} ``{v}``\n{suffix}"
                    field3 = False
                    field_list.append((field1, field2, field3))
                e_author=(f"Local Foxgames", "https://awooga.free.nf/localfoxgames.net", "https://iili.io/3cuA172.png")
                e_body=(f"{self.bot.reshiram_badge}", "", "", 0x13781a)
                e_fields=field_list
                e_images=("", "https://iili.io/3cJwzU7.png")
                e_footer=(f"{status_code} {reason}", "https://iili.io/3AE69YG.png")

            elif status_code == 408:
                async def fuckyou(interaction):
                    view.remove_item(fuckyoubutton)
                    await reshimessage.edit(content=f"-# couldn't contact server {status_code} {reason}\n:(", view=view, delete_after=1)
                fuckyoubutton = Button(label="Fuck You", style=discord.ButtonStyle.primary)
                fuckyoubutton.callback = fuckyou
                view.add_item(fuckyoubutton)
                await reshimessage.edit(content=f"couldn't contact server\n-# {status_code} {reason}", view=view)
                await asyncio.sleep(5)
                raise ValueError(f"{status_code} {reason}")

        except Exception as e:
            e_author=(f"Local Foxgames", "https://awooga.free.nf/localfoxgames.net", "https://iili.io/3cuA172.png")
            e_body=(f"{self.bot.reshiram_badge}", "", "", 0x781313)
            e_fields=[("an error occoured", f"error message: {e}", True)]
            e_images=("", "https://iili.io/3cmNr3x.png")
            e_footer=(f"❌", "https://iili.io/3AE69YG.png")

        finally:
            await reshimessage.edit(content="building embed...")
            embed = await self.bot.REF2.Webhook_Maker(author=e_author,body=e_body,fields=e_fields,images=e_images,footer=e_footer)
            await reshimessage.edit(content=None,embed=embed,view=None)

class Reshiram_Legacy_System_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, victim: discord.Member, *, reason = None):
        """strike someone with the ban hammer"""
        await victim.ban(reason=reason)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def unban(self, ctx, *, id: int):
        """act like nothing ever happened and unban someone"""
        await ctx.guild.unban(await self.bot.fetch_user(id))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reconnect(self, ctx):
        """triggers a reconnect"""
        await self.bot.ws.close(code=4000)

async def setup(bot):
    await bot.add_cog(Reshiram_Legacy_Init(bot))
    await bot.add_cog(Reshiram_Legacy_Minecraft_Commands(bot))
    await bot.add_cog(Reshiram_Legacy_System_Commands(bot))
    await bot.add_cog(Reshiram_Command_Handler(bot))