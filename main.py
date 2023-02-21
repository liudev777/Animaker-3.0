from auth import authenticate
from bot import startBot
import database
# Starts up the Hikari Library discord bot as well as the flask webpage for authentication.

# async def main():
#     queue = asyncio.Queue()
#     await asyncio.gather(authenticate(), bot.bot.run())
#     # await asyncio.gather(startBot(queue), authenticate(queue)
if __name__ == '__main__':
    startBot()

    # database.viewData() #del
    # asyncio.run(main())

    # queue = Manager().Queue()
    # auth_process = Process(target=auth.authenticate, args=(queue,))
    # bot_process = Process(target=bot.startBot, args=(queue,))
    # auth_process.start()
    # bot_process.start()
    pass




# print("hi")
"""
TODO:
figure out how to save discord id and anilist token together
"""