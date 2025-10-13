"""
experimental commands for Reshiram\n
some of them are broken or unfinished.
"""
import os, io, aiohttp

import discord
from discord.ext import commands
from discord import app_commands

from components.Reshiram_Furfag import furfag
from enum import Enum

class InDev_Init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await furfag.firLoggers("DISCORD", "I", f"{os.path.splitext(os.path.basename(__file__))[0].lower()} is ready")

    async def cog_load(self):
        await furfag.firLoggers("DISCORD", "I", f"{os.path.splitext(os.path.basename(__file__))[0].lower()} loaded")

class InDev_Modern(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reshi_channel = furfag.config["channel-ids"]["reshiram_channel"]

    class ReturnType(Enum):
        Raw = 0
        Post = 1

    class FilterType(Enum):
        Random = 0
        Top = 1
        Bottom = 2

    class E6E9(Enum):
        e926_request = 'e926'
        e621_request = 'e621'

    # @dataclass
    # class Payload(Enum):
    #     action: Optional[int]
    #     mcss_filter: 0
    #     mcss_id: '08d786b8-f81b-4483-b71e-cb51027b7490'

    # class WebRequest(Enum):
    #     get_api_version = RWR.mcss_requests.get_api_version()
    #     get_server_list = RWR.mcss_requests.get_server_list(mcss_filter)
    #     get_server_count = RWR.mcss_requests.get_server_count(mcss_filter)
    #     get_server_details = RWR.mcss_requests.get_server_details(mcss_id, mcss_filter)
    #     get_server_stats = RWR.mcss_requests.get_server_stats(mcss_id)
    #     post_server_action = RWR.mcss_requests.post_server_action(action, mcss_id)


    @app_commands.command(name="e6e9-request", description="just for testing")
    @app_commands.describe(
        service="which service to make a API-Request to",
        tags="tags to search by | ex. zorua, oder:score, rating:e, -futa",
        return_type="what type of response we want | post returns the page link, raw returns the media link",
        filter_type="how should the response be chosen",
    )
    async def esix_enine(self, interaction: discord.Interaction, service: E6E9, tags: str, return_type: ReturnType, filter_type: FilterType):
        await interaction.response.defer()
        try:
            response = await self.bot.RWR.e6e9_api_request(
                                                                service=service.value,
                                                                tags=tags,
                                                                return_type=return_type.value,
                                                                filter_type=filter_type.value)
            print(response)

            if 'https://' in response:
                await furfag.firLoggers("SYSTEM", "I", f"LINK DETECTED {response}")
                if response.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.mp4', '.webm')):
                    async with aiohttp.ClientSession() as session:
                        async with session.get(response) as new_response:
                            data = await new_response.read()
                            buffer = io.BytesIO(data)
                            buffer.seek(0)
                    if response.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                        print("is image :3")
                        file = discord.File(buffer, filename=f"{tags}.png", spoiler=True)
                    elif response.endswith(('.gif')):
                        print("is gif :3")
                        file = discord.File(buffer, filename=f"{tags}.gif", spoiler=True)
                    elif response.endswith(('.mp4', '.webm')):
                        print("is video :3")
                        file = discord.File(buffer, filename=f"{tags}.mp4", spoiler=True)
                    await interaction.followup.send(content=f"[RESHI-DEBUG] TRIGGERED WEB REQUEST {service.name}", file=file)
                else:
                    await interaction.edit_original_response(content=f"[RESHI-DEBUG] TRIGGERED WEB REQUEST {service.name}\n||{response}||")

        except Exception as e:
            await interaction.edit_original_response(content=f"[RESHI-DEBUG] COULDN'T TRIGGER WEB REQUEST: {e}")

class InDev_Legacy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def emojitest(self, ctx):
    #     serverid = '08d786b8-f81b-4483-b71e-cb51027b7490'
    #     url = 'https://localfoxgames.sytes.net:25600/api/v2'
    #     test_path = 'C:\\Users\\Avery\\AppData\\Roaming\\.spitefox\\reshiram\\cache\\test.png'
    #     print("guh")
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(url + f"/servers/{serverid}/icon", headers={"apiKey": os.getenv("mcss_api_key"),"Accept": "application/json"}, ssl=False, timeout=aiohttp.ClientTimeout(total=5)) as response:
    #             data, s, r = await response.read(), response.status, response.reason
    #             async with aiofiles.open(test_path, "wb") as file: # write the server icon file to the cache
    #                 await file.write(data)
    #             async with aiofiles.open(test_path, "rb") as file: # read from the cache for the emoji creation
    #                 imagereadfromfile = await file.read()
    #                 await self.bot.create_application_emoji(name='test', image=imagereadfromfile)

async def setup(bot):
    await bot.add_cog(InDev_Init(bot))
    await bot.add_cog(InDev_Modern(bot))
    await bot.add_cog(InDev_Legacy(bot))