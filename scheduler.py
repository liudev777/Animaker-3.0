# test phase
import asyncio
from anilist import renewUserShowDB
from database import getAiringShows, updateShows

async def p():
    while True:
        await asyncio.sleep(5)
        print("pinged")

# notifys the user when show is airing
async def notify():
    pass

async def schedule_show(bot, time, title, discordID, channelId):
    await asyncio.sleep(time)
    await bot.rest.create_message(channelId, content = '<@'+str(discordID)+'>' + f' {title} is now airing!',user_mentions = True)

async def enableAnimeAlert(bot, discordId, channelId, schedulers, renewSchedulers):
    renewSchedule = asyncio.create_task(periodicUserShowDBRenew(bot, discordId, channelId, schedulers))
    renewSchedulers[discordId] = renewSchedule
    await renewSchedulers[discordId]
    

async def updateSchedule(bot, discordId, channelId, schedulers):
    shows = []
    airingShows = getAiringShows(discordId)
    if not airingShows:
        return "No airing shows in watchlist"
    count = 0 # delete
    for show in airingShows:
        status = show['shows']['status']
        if status == "FINISHED":
            continue

        title = show['shows']['showName']
        timeUntilAir = show['shows']['timeUntilAir']

        # timeUntilAir = count
        # title = "test" + str(count)
        # count += 2
        shows.append(asyncio.create_task(schedule_show(bot, timeUntilAir, title, discordId, channelId)))

    schedule = asyncio.gather(*shows)
    schedulers[discordId] = schedule
    await schedulers[discordId]

async def periodicUserShowDBRenew(bot, discordId, channelId, schedulers):
    while True:
        renewUserShowDB(discordId)
        asyncio.create_task(updateSchedule(bot, discordId, channelId, schedulers))
        print("updated db for: ", discordId)
        await asyncio.sleep(21600)

async def reschedule():
    # afte a show has been pinged, check if it is still airing and then reschedule the next episode
    pass

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