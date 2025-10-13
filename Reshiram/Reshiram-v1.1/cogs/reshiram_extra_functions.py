"""
extra functions for Reshiram
"""

import os, asyncio, time, random, uuid, aiohttp, aiofiles, io

from discord import File
from discord.ext import commands
from pathlib import Path

from components.Reshiram_Furfag import furfag


class Reshiram_Extra_Functions_Init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await furfag.firLoggers("DISCORD", "I", f"{os.path.splitext(os.path.basename(__file__))[0].lower()} is ready")

    async def cog_load(self):
        await furfag.firLoggers("DISCORD", "I", f"{os.path.splitext(os.path.basename(__file__))[0].lower()} loaded")

class Reshiram_Extra_Functions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}
        self.cooldown_duration = 60
        self.vw = self.voice_wrapper(self)

    async def cache_server_icons(self, servers):
        furfag.firTimers.start('cache builder')

        async def process_server(server_id):
            server_id_truncated = server_id[:8]
            furfag.firTimers.start(f"{server_id_truncated}")

            server_icon, server_code, server_reason = await self.bot.RMR.get_server_icon(server_id)

            if server_code == 200:
                await self.bot.syffycache.create_custom_emoji(name=server_id_truncated, image=server_icon)
                async with aiofiles.open(os.path.join(self.bot.cache_path, f"{server_id}.png"), "wb") as file:
                    await file.write(server_icon)

                elapsed_server = furfag.firTimers.stop(f"{server_id[:8]}")
                await furfag.firLoggers("SYSTEM", "I", f"successfully cached {server_id_truncated} ({server_code}/{server_reason} • took {elapsed_server:.2f} seconds)")

            else:
                elapsed_server = furfag.firTimers.stop(f"{server_id[:8]}")
                await furfag.firLoggers("SYSTEM", "W", f"failed to cache {server_id_truncated} ({server_code}/{server_reason} • took {elapsed_server:.2f} seconds)")

        try:
            self.error_raised = False
            await furfag.firLoggers("SYSTEM", "I", f"caching server icons...")
            tasks = [process_server(server_id) for server_id in servers]
            await asyncio.gather(*tasks)
        except Exception as e:
            self.error_raised = True
            await furfag.firLoggers("SYSTEM", "E", f"we encountered an issue caching your stuff: {e}")
        finally:
            elapsed = furfag.firTimers.stop('cache builder')
            if self.error_raised is True:
                await furfag.firLoggers("TIMER", "E", f"failed.")
            else:
                await furfag.firLoggers("TIMER", "I", f"done! cache rebuild took {elapsed:.2f} seconds")

    async def is_valid_chair_message(self, message): # the code for this is so unneccecarily complicated
        current_time = time.time()
        last_used = self.cooldowns.get("chairpasta", 0)
        if current_time - last_used >= self.cooldown_duration:
            self.cooldowns["chairpasta"] = current_time
            chair_url = 'https://iili.io/3aKcocN.jpg'
            return chair_url
        else:
            await message.add_reaction("⏳")
            await asyncio.sleep(self.cooldown_duration)
            await message.remove_reaction("⏳", self.bot.user)

    async def custom_response(self, message, trigger):
        try:
            reshiram_filename = 'reshiram' + uuid.uuid4().hex

            if trigger == 'ai_reshi':
                response_source = await self.bot.RWR.reshiram_ai_response(message)
                response_file = None
                response_content = response_source

            if trigger == 'chair':
                response_source = await self.is_valid_chair_message(message) # url
                response_file = await self.file_from_link(response_source)
                response_content = furfag.config["response-messages"]["chair_message"]

            if trigger == 'weed_cat':
                response_source = await self.bot.RWR.e6e9_api_request(service='e926', tags='sprigatito solo pokemon(species)', return_type=0, filter_type=0)
                response_file = await self.file_from_link(response_source)
                response_content = None

            if trigger == 'reddit_cat':
                response_source = await self.bot.RWR.reddit_api_request()
                response_file = await self.file_from_link(response_source)
                response_content = "-# did someone say car?"

            if trigger == 'random':
                response_source = None
                response_file = None
                response_content = None
                helper_map = [
                lambda: self.vw.reshi_ctts(message),
                lambda: self.vw.reshi_rtts(message),
                lambda: self.vw.reshi_aitts(message),
                lambda: self.vw.reversify(message),
                ]
                await random.choice(helper_map)()
        finally:
            if response_file:
                if response_source.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    file = File(response_file, filename=f"{reshiram_filename}.png")
                elif response_source.endswith(('.gif')):
                    file = File(response_file, filename=f"{reshiram_filename}.gif")
                elif response_source.endswith(('.mp4', '.webm')):
                    file = File(response_file, filename=f"{reshiram_filename}.mp4")
                await message.channel.send(content=response_content, file=file)
            elif response_content:
                await message.channel.send(content=response_content)
            else:
                pass

    async def file_from_link(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as new_response:
                data = await new_response.read()
                file = io.BytesIO(data)
                file.seek(0)
                return file

    class voice_wrapper:
        def __init__(self, parent):
            self.parent = parent

        async def send_voicemessage(self, packed_data):
            data, filename, message = packed_data
            file = File(io.BytesIO(data), filename=filename)
            await message.channel.send_voice_message(file)

        async def reshi_ctts(self, message):
            await furfag.firLoggers("SYSTEM", "I", f"started!")
            data = await self.parent.bot.RWR.lazypyro_request(service="VoiceForge", voice="French-fry", message=message.content)
            if data:
                filename = f"RESHI_TTS(CANON)-{str(uuid.uuid4())[:8]}.mp3"
                await self.send_voicemessage(packed_data=(data, filename, message))
            else:
                await furfag.firLoggers("SYSTEM", "E", f"didn't recieve any data")

        async def reshi_rtts(self, message): # same as ctts but picks a random voice
            await furfag.firLoggers("SYSTEM", "I", f"started!")
            service = random.choice(["TikTok", "VoiceForge"])

            if service == 'TikTok':
                voice = random.choice(["en_male_narration", "en_uk_001", "en_male_funny"])
            elif service == 'VoiceForge':
                voice = random.choice(["Conrad", "Diesel", "Frank", "Gregory", "Kevin", "RansomNote", "Vlad", "Wiseguy", "Designer", "Evilgenius", "French-fry", "JerkFace", "Kidaroo", "TopHat", "Warren", "Zach"])

            data = await self.parent.bot.RWR.lazypyro_request(service=service, voice=voice, message=message.content)
            if data:
                filename = f"RESHI_TTS({service.upper()},{voice.upper()})-{str(uuid.uuid4())[:8]}.mp3"
                await self.send_voicemessage(packed_data=(data, filename, message))
            else:
                await furfag.firLoggers("SYSTEM", "E", f"didn't recieve any data")

        async def reshi_aitts(self, message):
            await furfag.firLoggers("SYSTEM", "I", f"started!")
            data = await self.parent.bot.RWR.elevenlabs_request(voice_id='nPczCjzI2devNBz1zQrb', message=message.content)
            if data:
                filename = f"RESHI_TTS(XILABS)-{str(uuid.uuid4())[:8]}.mp3"
                await self.send_voicemessage(packed_data=(data, filename, message))
            else:
                await furfag.firLoggers("SYSTEM", "E", f"didn't recieve any data")

        async def reversify(self, message):
            await furfag.firLoggers("SYSTEM", "I", f"started!")
            reversed = message.content[::-1]
            await message.channel.send(content=reversed)

async def setup(bot):
    await bot.add_cog(Reshiram_Extra_Functions_Init(bot))
    await bot.add_cog(Reshiram_Extra_Functions(bot))