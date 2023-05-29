import asyncio
import hikari
import lightbulb
import os
import dotenv
from scheduler import p, schedule_show, enableAnimeAlert, disableAnimeAlert
from anilist import testQuery, getCurrAnimeList, getCurrShowtimes, checkIsLoggedIn
from encryp import encrypt
from hikari import Embed
# from database import getAllShowtime

dotenv.load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = lightbulb.BotApp(token=BOT_TOKEN)

dotenv.load_dotenv()
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]

# REDIRECT_URI= f'http://localhost:3000/'

schedulers = {}
renewSchedulers = {}


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
    if not checkIsLoggedIn(discordId):
        await ctx.respond("Please Login first using /login")
        return

    data = getCurrAnimeList(discordId)
    if not data:
        await ctx.respond("Please Log in")
        return
    name = data['User']['name']
    entries = data['MediaListCollection']['lists'][0]['entries']
    titles = [entrie['media']['title']['userPreferred'] for entrie in entries]
    titles = "\n".join(titles)

    if not titles:
        titles = "No Shows In Watchlist"
    embed = Embed(
        title=f"{name}'s Shows:",
        description=titles,
        color=hikari.colors.Color.of((137, 207, 240))
    )
    await ctx.respond(embed=embed)

# test command
@bot.command
@lightbulb.command('ping', 'test', ephemeral=[True])
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    discordID = ctx.author.id
    await ctx.respond("started!")
    schedule = [(1, "one piece"), (2, "dragon ball"), (3, "fairy tail")]
    tasks = []
    for time, title in schedule:
        task = asyncio.create_task(schedule_show(ctx, time, title, discordID))
        tasks.append(task)
    await asyncio.gather(*tasks)

# enables anime reminders for airing shows
@bot.command
@lightbulb.command('alert', 'Enable Anime reminders')
@lightbulb.implements(lightbulb.SlashCommand)
async def alert(ctx):
    discordId = ctx.author.id
    if not checkIsLoggedIn(discordId):
        await ctx.respond("Please Login first using /login")
        return

    channelId = ctx.channel_id
    if discordId in renewSchedulers:
        await ctx.respond("Your alerts are already enabled")
    else:
        await ctx.respond("Your alerts are now enabled!")
        await enableAnimeAlert(bot, discordId, channelId, schedulers, renewSchedulers)

# disables any ping notification
@bot.command
@lightbulb.command('stop', 'Disable Anime reminders')
@lightbulb.implements(lightbulb.SlashCommand)
async def stop(ctx):
    discordId = ctx.author.id
    if not checkIsLoggedIn(ctx, discordId):
        await ctx.respond("Please Login first using /login")
        return
        
    await disableAnimeAlert(ctx, discordId, schedulers, renewSchedulers)

@bot.command
@lightbulb.command('helpu', 'Displays helpful')
@lightbulb.implements(lightbulb.SlashCommand)
async def stop(ctx):
    discordId = ctx.author.id
    if not checkIsLoggedIn(ctx, discordId):
        await ctx.respond("Please Login first using /login")
        return
        
    await disableAnimeAlert(ctx, discordId, schedulers, renewSchedulers)

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

