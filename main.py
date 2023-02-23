import hikari
import lightbulb
import os
import dotenv
from anilist import testQuery, getCurrAnimeList, getCurrShowtimes
from encryp import encrypt

dotenv.load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = lightbulb.BotApp(token=BOT_TOKEN)

dotenv.load_dotenv()
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]

# REDIRECT_URI= f'http://localhost:3000/'

# Lets users connect their anilist account to discord
@bot.command
@lightbulb.command('login', 'opens auth url', ephemeral=[True])
@lightbulb.implements(lightbulb.SlashCommand)
async def login(ctx):
    discordId = (ctx.author.id)
    discordId = encrypt(str(discordId))
    authUrl = f'https://anilist.co/api/v2/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&state={discordId}&response_type=code'
    await ctx.respond(hikari.Embed(title= "Link Discord with Anilist", url=authUrl))

# Displays search result of input
@bot.command
@lightbulb.option('anime_title', 'name of anime')
@lightbulb.command('info', 'get anime info')
@lightbulb.implements(lightbulb.SlashCommand)
async def info(ctx):
    discordId = (ctx.author.id)
    anime_title = str(ctx.options.anime_title)
    r = testQuery(discordId, anime_title)
    await ctx.respond(r)

# Gets current watchlist animes
@bot.command
@lightbulb.command('list', 'get anime watchlist info')
@lightbulb.implements(lightbulb.SlashCommand)
async def list(ctx):
    discordId = (ctx.author.id)
    r = getCurrAnimeList(discordId)
    await ctx.respond(r)

# Gets current watchlist anime airtimes
@bot.command
@lightbulb.command('showtime', 'get currently watching anime showtime info')
@lightbulb.implements(lightbulb.SlashCommand)
async def showtime(ctx):
    discordId = (ctx.author.id)
    r = getCurrShowtimes(discordId)
    await ctx.respond(r)




bot.run()


"""
TODO:
calendar
calendar reminder
view library
add to library
remove from library


optional:
give rating

"""

