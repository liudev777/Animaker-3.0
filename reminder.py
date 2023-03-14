# test phase
import asyncio

async def p():
    while True:
        await asyncio.sleep(5)
        print("pinged")

# notifys the user when show is airing
async def notify():
    pass


"""
def notifyall
async def notify
need: discord id, showtimeid
update database

"""