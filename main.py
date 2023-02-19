import hikari
import lightbulb
import os
import dotenv

dotenv.load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]

bot = hikari.GatewayBot(token=BOT_TOKEN)

@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent):
    print("message detected")

bot.run()