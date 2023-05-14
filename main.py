import asyncio
import hikari
import lightbulb
import os
import dotenv
from scheduler import p, schedule_show, enableAnimeAlert, disableAnimeAlert
from anilist import testQuery, getCurrAnimeList, getCurrShowtimes
from encryp import encrypt
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
    data = getCurrAnimeList(discordId)
    if data == -1:
        await ctx.respond("There was an Error")
        return
    name = data['User']['name']
    entries = data['MediaListCollection']['lists'][0]['entries']
    titles = [entrie['media']['title']['userPreferred'] for entrie in entries]
    titles = "\n".join(titles)
    shows = f'Viewer: {name}\n\nCurrently Watching:\n{titles}'
    if not shows:
        shows = "No Shows In Watchlist"
    await ctx.respond(hikari.Embed(title=shows))

# Gets current watchlist anime airtimes
@bot.command
@lightbulb.command('showtime', 'get currently watching anime showtime info')
@lightbulb.implements(lightbulb.SlashCommand)
async def showtime(ctx):
    discordId = (ctx.author.id)
    data = getCurrShowtimes(discordId)
    if data == -1:
        await ctx.respond("No Shows Airing in Watchlist")
        return
    medias = data['Page']['media']
    showInfosList = [(showInfos['title']['userPreferred'], showInfos['airingSchedule']['nodes']) for showInfos in medias if showInfos['airingSchedule']['nodes']]

    print(showInfosList)
    output = ""
    for showInfos in showInfosList:
        title = showInfos[0]
        formatedNode = ''
        for node in showInfos[1]:
            formatedNode += "\t" + repr(node) + '\n'
        output += (f'{title}:\n{formatedNode}\n')
    print(output)
    
    if not output:
        output = "No Shows Airing in Watchlist"
    await ctx.respond(output)

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

@bot.command
@lightbulb.command('alert', 'Enable Anime reminders')
@lightbulb.implements(lightbulb.SlashCommand)
async def alert(ctx):
    discordId = ctx.author.id
    channelId = ctx.channel_id
    await ctx.respond("Your alerts are now enabled!")
    await enableAnimeAlert(bot, discordId, channelId, schedulers, renewSchedulers)

@bot.command
@lightbulb.command('stop', 'Disable Anime reminders')
@lightbulb.implements(lightbulb.SlashCommand)
async def stop(ctx):
    discordId = ctx.author.id
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

