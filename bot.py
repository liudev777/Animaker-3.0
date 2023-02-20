import hikari
import lightbulb
import os
import dotenv
import auth

def startBot():
    dotenv.load_dotenv()
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    bot = lightbulb.BotApp(token=BOT_TOKEN)

    @bot.command
    @lightbulb.command('open', 'opens auth` url')
    @lightbulb.implements(lightbulb.SlashCommand)
    async def ping(ctx):
        print(auth.getURL())
        await ctx.respond (auth.getURL())

    bot.run()

