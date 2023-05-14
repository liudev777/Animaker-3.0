# test phase
import asyncio
from pprint import pp
from anilist import getCurrShowtimes
from hikari import Embed
from hikari import colors

count = 0

async def p():
    while True:
        await asyncio.sleep(5)
        print("pinged")

# notifys the user when show is airing
async def notify():
    pass

# sends a ping message when a scheduled show is airing
async def schedule_show(bot, time, title, episode, imageUrl, discordId, channelId, schedulers):
    await asyncio.sleep(time)
    embed = Embed(
        title = f'Now Airing:',
        description=f'{title} episode {episode}',
        color= colors.Color.of((137, 207, 240))
    )
    embed.set_thumbnail(imageUrl)

    await bot.rest.create_message(channelId, '<@'+str(discordId)+'>', embed=embed, user_mentions = True)
    # await reschedule(bot, discordId, channelId, schedulers)

# enables ping alerts for user
async def enableAnimeAlert(bot, discordId, channelId, schedulers, renewSchedulers):
    renewSchedule = asyncio.create_task(periodicUserShowRenew(bot, discordId, channelId, schedulers))
    renewSchedulers[discordId] = renewSchedule
    await renewSchedulers[discordId]
    

# makes a call to anilist api and fetches up to date anime and airtime from watch list
async def updateSchedule(bot, discordId, channelId, schedulers):
    shows = []
    currShows = getCurrShowtimes(discordId)
    # pp(currShows)
    for media in currShows['Page']['media']: # repopulate userShows entries with updated shows
        # pp(media)
        status = media['status']
        if not status == "RELEASING":
            continue
        if not media['airingSchedule']['nodes']:
            continue
        node = media['airingSchedule']['nodes'][0]
        timeUntilAir = node['timeUntilAiring']
        episode = node['episode']
        title = media['title']['userPreferred']
        imageUrl = media['coverImage']['medium']

        # global count 
        # timeUntilAir = count
        # title = "test" + str(count)
        # count += 3
        shows.append(asyncio.create_task(schedule_show(bot, timeUntilAir, title, episode, imageUrl, discordId, channelId, schedulers)))

    # updates the scheduler
    if discordId in schedulers:
        schedulers[discordId].cancel()
    schedule = asyncio.gather(*shows)
    schedulers[discordId] = schedule
    await schedulers[discordId]

# update the scheduler periodically to fetch any new anime or changes in showtime
async def periodicUserShowRenew(bot, discordId, channelId, schedulers):
    while True:
        await reschedule(bot, discordId, channelId, schedulers)
        await asyncio.sleep(21600)

async def reschedule(bot, discordId, channelId, schedulers):
    # afte a show has been pinged, check if it is still airing and then reschedule the next episode
    asyncio.create_task(updateSchedule(bot, discordId, channelId, schedulers))
    print("updated db for: ", discordId)
    pass

# disables schedule alerts
async def disableAnimeAlert(ctx, discordId, schedulers, renewSchedulers):
    if discordId not in schedulers:
        await ctx.respond("You don't have any alerts enabled")
        return

    schedulers[discordId].cancel()
    del schedulers[discordId]
    renewSchedulers[discordId].cancel()
    del renewSchedulers[discordId]
    await ctx.respond("Your alerts are now disabled!")
    


"""
def notifyall
async def notify
need: discord id, showtimeid
update database

"""