import discord
from discord.ext import commands


### main bot class
class Zekrom(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="z!", intents=intents)
        self.remove_command('help')

    async def on_ready(self):
        print(f"logged in as {self.user}")

    async def setup_hook(self):
        await self.add_cog(Reshiram_Message_Handler(self))



### message handler
class Reshiram_Message_Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        keywords_map = {
          "avery": self.responder(["avery? fuck that guy"]),
          "zekrom": self.responder(["my love", "dragons mmmm", ... ]),
          # in general, this maps trigger words to functions that return a response
        }
        for k, v in keywords_map.items():
            if k in message.content:
                response = v()
                message.channel.send(response)

    def responder(self, responses):
        message.channel.send(response)

class ReshiramConfig():
    default_config = """[super-duper-awesome-config]\nsignature = "I love men"\n[settings]\nstartup_message = true\nclear_logs_on_startup = true\n[trigger-words]\nprefixes = ["r!", "reshi"]\nweed_words = ["weed", "bunt", "drugs", "cocaine", "meth", "breaking bad", "blunt", "crack", "tabacco", "cannabis", "heroin", "lsd"]\ncat_words = ["cat", "car", "kitty", "kimty", "gato", "cato", "chipflake"]\nthankful_words = ["thanks", "thank you", "thanks", "ty"]\n[channel-ids]\nreaction_ignore_channels = [1234567891011121314, 1234567891011121314]\nstartup_channel = 1234567891011121314 # startup channel\nmc_channel = 1234567891011121314\nmc_news_channel = 1234567891011121314\n[user-ids]\nzekrom_user = 1234567891011121314 # user id of zekrom\n[response-messages]\nanswers = ["yes", "no", "maybe","probably","probably not","oh for sure","oh hell nah","never ask me a god damn thing again", "I don't wanna answer that", "fuck off why don'tcha", "yeah", "nah", "yup", "nope", "what are you yapping about", "sometimes", "always", "never", "hey OP, what the fuck does this mean"]\nemotions = [":)", ":(", ":]", ":[", ":}", ":{", ":3", "3:", ":c", "c:", "^-^", "^w^", "OwO", "owo", "UwU", "uwu", ">w<", ">.<", ">~<", ">///<", ":D", "D:", ":v)", ":v(", "-w-", "-.-", "._.", "O_o", "o_O", "(=^ ◡ ^=)", "(ಥ﹏ಥ)"]\nspecial_emotions = ["😭", "😢", "😔", "😕", "😖", "😞", "😟", "😠", "😡", "😢", "😣", "😤", "😥", "😦", "😧", "😨", "😩", "😪", "😫", "😬", "😭", "😮", "😯", "😰", "😱", "😲", "😳", "😴", "😵", "😶", "😷", "😸", "😹", "😺", "😻", "😼", "😽", "😾", "😿", "🙀", "🙁", "🙂", "🙃", "🙄", "🙅", "🙆", "🙇", "🙈", "🙉", "🙊", "🙋", "🙌", "🙍", "🙎", "🙏"]\nchair_message = "A Chair is a piece of furniture with a raised surface supported by legs, commonly used to seat a single person. Chairs are supported most often by four legs and have a back; however, a Chair can have three legs or can have a different shape. Chairs are made of a wide variety of materials, ranging from wood to metal to synthetic material (e.g. plastic), and they may be padded or upholstered in various colors and fabrics, either just on the seat (as with some dining room Chairs) or on the entire Chair. Chairs are used in a number of rooms in homes (e.g. in living rooms, dining rooms, and dens), in schools and offices (with desks), and in various other workplaces, such as the Black Mesa facility. A Chair without a back or arm rests is a stool, or when raised up, a bar stool. A Chair with arms is an armChair; one with upholstery, reclining action, and a fold-out footrest is a recliner.A permanently fixed Chair in a train or theater is a seat or, in an airplane, airline seat; when riding, it is a saddle or bicycle saddle; and for an automobile, a car seat or infant car seat. With wheels it is a wheelChair; or when hung from above, a swing. An upholstered, padded Chair for two people is a 'loveseat', while if it is for more than two person it is a couch, sofa, or settee; or if is not upholstered, a bench. A separate footrest for a Chair, usually upholstered, is known as an ottoman, hassock, or pouffe.https://media.discordapp.net/stickers/1311291974304927754.webp\\n-# source: Wikipedia"\nthankful_messages = ["you're welcome ig?", "what for?", "np?", "sure ig..", "uhh yeah!"]\n[status-config]\nstatus_types = ["online", "invisible", "idle", "dnd"]\nactivity_types = ["playing", "streaming", "listening", "watching"]\nplaying_statuses = ["Minecraft", "Garry's Mod", "Team Fortress 2", "Among Us", "Minceraft", "Half Life 2", "Pokémon Black", "Pokémon White", "Pokémon Black 2", "Pokémon White 2"] # i love miners\nstreaming_statuses = ["my ass", "my pussy", "my dick", "my asshole", "my pussyhole", "my dickhole", "my assholehole", "my pussyholehole", "my dickholehole"] # assholehole is a thing\nlistening_statuses = ["Spotify", "Apple Music", "YouTube Music", "Tidal ??? ? ?? ??? ?? ?? ", "Amazon Music", "Deez (nuts)er", "SoundCloud", "Bandcamp"] # i dont know what this is\nwatching_statuses = ["femboy porn", "hentai", "pokemon porn", "NOT porn..?", "youtube", "netflix", "disney+", "hulu", "crunchyroll", "pokemon (not porn)", "pokemon porn (not hentai)"] # i love pokemon porn (true)\n[urls]\nstartup_gif = "https://media.discordapp.net/stickers/1311331170109100124.gif"\nreshiram_sticker = "https://media.discordapp.net/stickers/1311331170109100124.gif"\nzekrom_sticker = "https://media.discordapp.net/stickers/1311331297234386945.gif"\ne926_api_url = "https://e926.net/posts.json"\npokemon_images_json = "super-duper-pawsome-pokemon-images.json"\nhostname = ""\nmcss_api_url = ""\npokeapi_url = "https://pokeapi.co/api/v2/"\n[api-kys]\ne921_headers = '{"User-Agent": "YOUR_E6_USER_AGENT"}'\ne926_params = '{"tags": "sprigatito solo pokemon(species)","limit": 500}'\nreddit = '{"client_id": "YOUR_CLIENT_ID", "client_secret": "YOUR_CLIENT_SECRET", "user_agent": "YOUR_REDDIT_USER_AGENT"}' # please please PLEASE user enviroment variables\nmcss_api_key = "YOUR_MCSS_API_KEYS"\nreshiram_token = "YOUR_BOT_TOKEN"\n[meta]\nbackup = true"""

### entrypoint
if __name__ == "__main__":
    import os
    bot = Zekrom()
    bot.run('')