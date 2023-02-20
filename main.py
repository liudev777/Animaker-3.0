import bot
import auth
import database
from multiprocessing import Process, freeze_support

# Starts up the Hikari Library discord bot as well as the flask webpage for authentication.

if __name__ == '__main__':
    database.viewData()
    auth_process = Process(target=auth.authenticate)
    bot_process = Process(target=bot.startBot)
    auth_process.start()
    bot_process.start()
    pass




# print("hi")
"""
TODO:
figure out how to save discord id and anilist token together
"""