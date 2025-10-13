"""
even more extra functions for Reshiram\n
these don't require the bot session, which is why they are seperate
"""

import os, random, aiohttp, aiofiles, asyncpraw, asyncio, json, uuid

from components.Reshiram_Furfag import furfag

from mistralai import Mistral
from mistralai.models import SDKError

from datetime import datetime
from discord import Embed
from functools import wraps

### Extra Functions(2)
class Reshiram_Extra_Functions_2:
    async def Webhook_Maker(author, body, fields, images, footer):
        author_name, author_url, author_icon_url = author
        body_title, body_title_url, body_description, body_colour = body
        image_url, image_thumbnail_url = images
        footer_text, footer_icon_url = footer
        try:
            embed = Embed(title=body_title,
                          url=body_title_url,
                          description=body_description,
                          colour=body_colour,
                          timestamp=datetime.now())

            embed.set_author(name=author_name,
                             url=author_url,
                             icon_url=author_icon_url)

            for field in fields:
                field_name, field_value, field_inline = field

                embed.add_field(name=field_name,
                                value=field_value,
                                inline=field_inline)

            embed.set_image(url=image_url
                            )

            embed.set_thumbnail(url=image_thumbnail_url
                                )

            embed.set_footer(text=footer_text,
                             icon_url=footer_icon_url)
        except Exception as e:
            await furfag.firLoggers("SYSTEM", "E", f"WebhookMaker encountered an issue: {e}")
            return None
        finally:
            return embed

### Web Requests
class Reshiram_Web_Requests:
    def __init__(self, rwr_session):
        self.RWR_Session = rwr_session
        self.Mistral = Mistral
        self.SDKError = SDKError
        self.MistralKey = os.getenv("mistral_api_key")
        self.posts = []
        self.reddit_creds = eval(os.getenv("reddit_creds"))
        self.elevenlabs_url = "https://api.elevenlabs.io/v1/text-to-speech/"
        self.elevenlabs_api_key = os.getenv("xi_api_key")
        self.elevenlabs_api_key_two = os.getenv("xi_api_key_two")
        self.pokeapi_url = "https://pokeapi.co/api/v2/pokemon/"
        self.lazypyro_url = "https://lazypy.ro/tts/request_tts.php"

    async def e6e9_api_request(self, service: str, tags: str, return_type: int = 0, filter_type: int = 0): # returns a result
        await furfag.firLoggers("SYSTEM", "I", f"{service} request started")
        try:
            e6e9_headers = {"User-Agent": "Reshiram/2.0 (by LucarioKisser on e621)"}
            e6e9_params = {"tags": f"{tags}", "limit": 621}
            if service == 'e621':
                e6e9_url = 'https://e621.net/posts.json'
            elif service == 'e926':
                e6e9_url = 'https://e926.net/posts.json'
        except Exception as e:
            await furfag.firLoggers("SYSTEM", "E", f"couldn't define e6e9 variables: {e}")
        # get posts.json from e6 or e9
        try:
            async with self.RWR_Session.get(url=e6e9_url, headers=e6e9_headers, params=e6e9_params, ssl=True, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    posts_json = await response.json()
                    posts = posts_json.get("posts", [])
        except Exception as e:
            await furfag.firLoggers("SYSTEM", "E", f"couldn't get posts from {service}: {e}")
        # filter posts based on the filter provided
        try:
            ############################################################################
            if filter_type == 0: # random
                filtered_post = random.choice(posts)
            elif filter_type == 1: # top
                filtered_post = max(posts, key=lambda p: p.get("score", {}).get("total", 0))
            elif filter == 2: # bottom
                filtered_post = max(posts, key=lambda p: p.get("score", {}).get("down", 0))
            ############################################################################
        except Exception as e:
            await furfag.firLoggers("SYSTEM", "E", f"couldn't filter posts: {e}")

        # return either the raw file link or the post's page
        try:
            ############################################################################
            if return_type == 0: # raw link
                return_to_sender = filtered_post.get("file", {}).get("url")
            elif return_type == 1: # post page
                return_to_sender = f"https://e621.net/posts/{filtered_post.get('id')}"
            ############################################################################
        except Exception as e:
            await furfag.firLoggers("SYSTEM", "E", f"couldn't retrieve post: {e}")
        finally:
            await furfag.firLoggers("SYSTEM", "I", f"{service} request finished")
            return return_to_sender

    async def reddit_api_request(self): # returns a result
        await furfag.firLoggers("SYSTEM", "I", f"reddit request started")
        try:
            reddit = asyncpraw.Reddit(**self.reddit_creds)
            subreddit = await reddit.subreddit("cats")
            hot_posts = subreddit.hot(limit=100)
            async for post in hot_posts:
                if post.url.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    self.posts.append(post)
            await reddit.close()
            if self.posts:
                cat_to_send = random.choice(self.posts).url
        except Exception as e:
            await furfag.firLoggers("SYSTEM", "E", f"encountered an issue while fetching your kitties: {e}")
        finally:
            await furfag.firLoggers( "SYSTEM", "I", f"reddit request finished")
            return cat_to_send

    async def reshiram_ai_response(self, message, agent_id_override: str = None): # returns a result
        await furfag.firLoggers("AI", "I", f"{message.author.name} says: {message.content}")
        async with message.channel.typing():
            client = self.Mistral(api_key=self.MistralKey)
            agent_ids = [
                'ag:ae79bb3c:20250409:reshi-ai-helpful:480aad5f',
                'ag:ae79bb3c:20250409:reshi-ai-rude:384fa8fa'
            ]
            opposite = "rewrite the following message to change it's meaning to the opposite. respond with only the rewritten message and nothing else."
            caveman = "rewrite the following message as though you are a caveman, keep your response to less than 2 sentences. respond with only the rewritten message and nothing else."
            vowels_only = "rewrite the following message to only include vowels. respond with only the rewritten message and nothing else."
            reshiram = "rewrite the following message as though you are reshiram, a snarky and sassy dragon. respond with only the rewritten message and nothing else."
            rewriter_options = [
                opposite,
                caveman,
                vowels_only,
                reshiram
            ]
            try:
                if random.random() < 0.5:
                    chat_response = client.agents.complete(
                        agent_id = agent_id_override or random.choice(agent_ids),
                        messages= [
                            {
                                "role": "system",
                                "content": random.choice(rewriter_options)
                            },
                            {
                            "role": "user",
                            "content": f"{message.content}"
                        }
                    ]
                )
                else:
                    chat_response = client.agents.complete(
                        agent_id = agent_id_override or random.choice(agent_ids),
                        messages= [
                            {
                            "role": "user",
                            "content": f"{message.author.name} says: {message.content}",
                        }
                    ]
                )
                reshi_response = chat_response.choices[0].message.content
                await furfag.firLoggers("AI", "I", f"AI Reshiram says: {reshi_response}")
            except self.SDKError as e:
                if e.status_code == 429:
                    await furfag.firLoggers("AI", "W", f"rate limited {e.status_code}")
                    return "-# we're getting cock blocked (rate limited)"
            except Exception as e:
                await furfag.firLoggers("AI", "E", f"AI Response failed: {e}")
            finally:
                return reshi_response + "\n-# AI-Generated"

    async def lazypyro_request(self, service: str = "VoiceForge", voice: str = "French-fry", message: str = None): # returns a result
        data = {
            "service": service,
            "voice": voice,
            "text": message
            }
        try:
            await furfag.firLoggers("SYSTEM", "I", f"{service}/{voice}/{message}")
            async with self.RWR_Session.post(self.lazypyro_url, data=data) as response:
                result = await response.text()
                response_json = json.loads(result)
                audio_url = response_json["audio_url"]
                async with self.RWR_Session.get(audio_url) as audio_response:
                    return_data = await audio_response.read()
        except Exception as e:
            await furfag.firLoggers("SYSTEM", "E", f"couldn't get lazypyro-tts: {e}")
            return None
        finally:
            return return_data

    async def elevenlabs_request(self, voice_id: str = 'nPczCjzI2devNBz1zQrb', message = None):
        if message is not None:
            api_key = self.elevenlabs_api_key
            headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
            jsondata = {"text": message, "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}
            try:
                async with aiohttp.ClientSession() as session: # very W.I.P, don't judge the messy code
                    async with session.post(url=self.elevenlabs_url + voice_id, headers=headers, json=jsondata, ssl=False, timeout=aiohttp.ClientTimeout(total=5)) as response:
                        data = await response.read()
                        if response.status == 200:
                            await furfag.firLoggers("SYSTEM", "I", f"primary api key worked! ({response.status}/{response.reason})")
                            final_data = data

                        elif response.status == 401:
                            await furfag.firLoggers("SYSTEM", "W", f"primary api key failed! ({response.status}/{response.reason})")

                            api_key = self.elevenlabs_api_key_two
                            headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
                            jsondata = {"text": message, "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}
                            await furfag.firLoggers( "SYSTEM", "W", f"retrying with backup api key..")
                            async with aiohttp.ClientSession() as session: # very W.I.P, don't judge the messy code
                                async with session.post(url=self.elevenlabs_url + voice_id, headers=headers, json=jsondata, ssl=False, timeout=aiohttp.ClientTimeout(total=5)) as response:
                                    new_data = await response.read()
                                    if response.status == 200:
                                        await furfag.firLoggers("SYSTEM", "I", f"backup api key worked! ({response.status}/{response.reason})")
                                        final_data = new_data
                                    elif response.status == 401:
                                        await furfag.firLoggers("SYSTEM", "E", f"backup api key failed! ({response.status}/{response.reason})")
                                        final_data = None
            except Exception as e:
                await furfag.firLoggers( "SYSTEM", "E", f"couldn't do the funny ai voice: {e}")

            finally:
                return final_data

    async def cache_pokemon_sprites(self, cache_path):
        pokemon_sprites_path = os.path.join(cache_path, "pokemon_sprites.json")
        async def pokeapi_helper(session, url):
            while True:
                try:
                    async with session.get(url) as response:
                        if response.status == 429:
                            retry_after = int(response.headers.get("Retry-After", 5))
                            await furfag.firLoggers( "SYSTEM", "E", f"Rate limited! Waiting {retry_after} seconds...")
                            await asyncio.sleep(retry_after)
                            continue
                        data = await response.json()
                        return data["name"], data["sprites"]["front_default"]
                except Exception as e:
                    await furfag.firLoggers("SYSTEM", "E", f"Exception in helper for {url}: {e}")
                    return None, None

        async def load_pokesmonprites():
            try:
                async with aiofiles.open(pokemon_sprites_path, "r", encoding='utf-8') as f:
                    file = await f.read()
                    pokemon_sprites_json = json.loads(file)
            except (json.JSONDecodeError, FileNotFoundError):
                pokemon_sprites_json = {}
            finally:
                return pokemon_sprites_json

        async def save_pokesmonprites(pokemon_sprites_json):
            async with aiofiles.open(pokemon_sprites_path, "w", encoding='utf-8') as f:
                data = json.dumps(pokemon_sprites_json, indent=None)
                await f.write(data)

        furfag.firTimers.start('pokemon-sprites-creation')
        pokemon_sprites = await load_pokesmonprites()
        try:
            error_raised = False
            async with self.RWR_Session.get(self.pokeapi_url + "?limit=2000") as response:
                data = await response.json()
                tasks = [pokeapi_helper(self.RWR_Session, pokemon["url"]) for pokemon in data["results"]]
                results = await asyncio.gather(*tasks)

                for name, image_url in results:
                    if image_url:
                        pokemon_sprites[name] = image_url

        except Exception as e:
            await furfag.firLoggers("SYSTEM", "E", f"couldn't cache pokémon sprites: {e}")
            error_raised = True
        finally:
            if error_raised is True:
                return 400
            else:
                elapsed = furfag.firTimers.stop('pokemon-sprites-creation')
                await furfag.firLoggers("TIMER", "I", f"caching pokémon sprites took {elapsed:.2f} seconds")
                await furfag.firLoggers("SYSTEM", "I", f"pokemon sprites saved to {os.path.relpath(os.path.join(cache_path, "pokemon_sprites.json"), os.path.dirname(os.path.dirname(cache_path)))}")
                await save_pokesmonprites(pokemon_sprites)
                return 200

### MCSS Requests
class Reshiram_Mcss_Requests:
    def __init__(self, rmr_session):
        self.RMR_Session = rmr_session
        self.url = 'https://localfoxgames.sytes.net:25600/api/v2'
        self.headers = {"apiKey": os.getenv("mcss_api_key"),"Accept": "application/json"}


    def catch_timeout(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except (asyncio.TimeoutError, aiohttp.ClientError):
                return 'None', 408, 'Request Timeout'
        return wrapper

# api
    @catch_timeout
    async def get_api_version(self):
        async with self.RMR_Session.get(self.url, headers=self.headers, ssl=False, timeout=aiohttp.ClientTimeout(total=5)) as response:
            return await response.json(), response.status, response.reason

# servers
    @catch_timeout
    async def get_server_list(self, serverfilter):
        async with self.RMR_Session.get(self.url + "/servers", headers=self.headers, params={"filter": serverfilter}, ssl=False, timeout=aiohttp.ClientTimeout(total=5)) as response:
            return await response.json(), response.status, response.reason

    @catch_timeout
    async def get_server_count(self, serverfilter):
        async with self.RMR_Session.get(self.url + "/servers/count", headers=self.headers, params={"filter": serverfilter}, ssl=False, timeout=aiohttp.ClientTimeout(total=5)) as response:
            return await response.json(), response.status, response.reason

# server
    @catch_timeout
    async def get_server_details(self, serverid, serverfilter):
        async with self.RMR_Session.get(self.url + f"/servers/{serverid}", headers=self.headers, params={"filter": serverfilter}, ssl=False, timeout=aiohttp.ClientTimeout(total=5)) as response:
            return await response.json(), response.status, response.reason

    @catch_timeout
    async def get_server_stats(self, serverid):
        async with self.RMR_Session.get(self.url + f"/servers/{serverid}/stats", headers=self.headers, ssl=False, timeout=aiohttp.ClientTimeout(total=5)) as response:
            return await response.json(), response.status, response.reason

    @catch_timeout
    async def get_server_icon(self, serverid):
        async with self.RMR_Session.get(self.url + f"/servers/{serverid}/icon", headers=self.headers, ssl=False, timeout=aiohttp.ClientTimeout(total=5)) as response:
            return await response.read(), response.status, response.reason

# server(post)
    @catch_timeout
    async def post_server_action(self, serverid, serveraction):
        async with self.RMR_Session.post(self.url + f"/servers/{serverid}/execute/action", headers=self.headers, json={"action": serveraction}, ssl=False, timeout=aiohttp.ClientTimeout(total=5)) as response:
            return await response.read(), response.status, response.reason