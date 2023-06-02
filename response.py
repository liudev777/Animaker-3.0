from hikari import Embed, colors

async def alertEmbed(bot, title, episode, imageUrl, channelId, discordId):
    embed = Embed(
        title = f'Now Airing:',
        description=f'{title} episode {episode}',
        color= colors.Color.of((137, 207, 240))
    )
    embed.set_thumbnail(imageUrl)

    await bot.rest.create_message(channelId, '<@'+str(discordId)+'>', embed=embed, user_mentions = True)