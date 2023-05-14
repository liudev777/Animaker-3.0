from database import *
from anilist import *
import asyncio

discordId = 436687700675002388

# renewUserShowDB(discordId)

# airingShows = getAiringShows(discordId)
# if not airingShows:
#     print( "No airing shows in watchlist")

# for show in airingShows:
#     status = show['shows']['status']
#     if status == "FINISHED":
#         continue

#     title = show['shows']['showName']
#     timeUntilAir = show['shows']['timeUntilAir']

#     s = timeUntilAir
#     days = s // (24 * 3600)
#     s %= (24 * 3600)
#     hours = s // 3600
#     s %= 3600
#     minutes = s // 60

#     print(title, ("%02d:%02d:%02d" % (days, hours, minutes)))



