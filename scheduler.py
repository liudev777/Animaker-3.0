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

async def schedule_show(ctx, time, title, discordID):
    await asyncio.sleep(time)
    await ctx.respond('<@'+str(discordID)+'>' + f' {title} is now airing!',user_mentions = True)

async def enableAnimeAlert(ctx, discordId):
    asyncio.create_task(periodicUserShowDBRenew(discordId))
    airingShows = getAiringShows(discordId)
    if not airingShows:
        return "No airing shows in watchlist"
    shows = []
    count = 10 # delete
    for show in airingShows:
        status = show['shows']['status']
        if status == "FINISHED":
            continue

        title = show['shows']['showName']
        timeUntilAir = show['shows']['timeUntilAir']
        shows.append(asyncio.create_task(schedule_show(ctx, timeUntilAir, title, discordId)))
    await asyncio.gather(*shows)

async def periodicUserShowDBRenew(discordId):
    while True:
        print("updated db for: ", discordId)
        renewUserShowDB(discordId)
        await asyncio.sleep(43200)
    


"""
def notifyall
async def notify
need: discord id, showtimeid
update database

"""