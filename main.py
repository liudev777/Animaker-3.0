# import bot
from multiprocessing import Process, freeze_support

import hikari
import lightbulb
import os
import dotenv
import auth

def startBot():
    dotenv.load_dotenv()
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    print("THIS IS THE TOKEN: " + BOT_TOKEN)

    bot = lightbulb.BotApp(token=BOT_TOKEN)

    @bot.command
    @lightbulb.command('open', 'opens auth` url')
    @lightbulb.implements(lightbulb.SlashCommand)
    async def ping(ctx):
        await ctx.respond ("ping")

    bot.run()

if __name__ == '__main__':
    p = Process(target=auth.authenticate)
    # p.start()
    startBot()

# print("hi")