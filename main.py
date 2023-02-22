import hikari
import lightbulb
import os
import dotenv
from encryp import encrypt

dotenv.load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = lightbulb.BotApp(token=BOT_TOKEN)

dotenv.load_dotenv()
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]

# REDIRECT_URI= f'http://localhost:3000/'


@bot.command
@lightbulb.command('login', 'opens auth url')
@lightbulb.implements(lightbulb.SlashCommand)
async def login(ctx):
    discordId = (ctx.author.id)
    discordId = encrypt(str(discordId))
    authUrl = f'https://anilist.co/api/v2/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&state={discordId}&response_type=code'
    await ctx.respond(authUrl)

bot.run()




