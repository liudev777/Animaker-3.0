import hikari
import lightbulb
import os
import dotenv
import auth
from auth import authenticate
from queue import Queue
import threading

queue = Queue()
auth_thread = threading.Thread(target=authenticate, args=(queue,))
auth_thread.start()

# if (__name__ == '__main__'):
dotenv.load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = lightbulb.BotApp(token=BOT_TOKEN)

@bot.command
@lightbulb.command('login', 'opens auth url')
@lightbulb.implements(lightbulb.SlashCommand)
async def login(ctx):
    queue.put(ctx.author.id)
    await ctx.respond(auth.getURL())

def startBot():
    bot.run()




