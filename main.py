import auth
import bot
from multiprocessing import Process, freeze_support

if __name__ == '__main__':
    auth_process = Process(target=auth.authenticate)
    bot_process = Process(target=bot.startBot)

    auth_process.start()
    bot_process.start()

    auth_process.join()
    bot_process.join()

print("hi")