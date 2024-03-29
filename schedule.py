from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import getEnabledAlertUsers, getAlertUser, removeAlertUser, addAlertUser
from anilist import getCurrShowtimes, getShowtime
from response import alertEmbed
from datetime import datetime

# manager class to keep track of running jobs
class AlertManager:
    def __init__(self, bot) -> None:
        self.bot = bot
        self.jobs = {}
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(self.refreshSchedule, 'interval', hours=12)
        self.scheduler.start()

    # initializes alerts for all users who chose to enable it
    async def initAlerts(self):
        enabled_datas = getEnabledAlertUsers()
        for data in enabled_datas:
            discordId = data['discordId']
            channelId = data['channelId']
            await self.activateAlerts(discordId, channelId)

    # turns on the alert for each individual user
    async def activateAlerts(self, discordId, channelId):
        showDatas = getCurrShowtimes(discordId)
        for media in showDatas['Page']['media']:
            status = media['status']

            # skip shows that have ended or doesn't have a schedule
            if not status == "RELEASING":
                continue
            if not media['airingSchedule']['nodes']:
                continue
            
            node = media['airingSchedule']['nodes'][0]
            airingAt = datetime.fromtimestamp(int(node['airingAt']))
            alert_info = {
                'showId': media['id'],
                'discordId': discordId,
                'channelId': channelId,
                'episode': node['episode'],
                'title': media['title']['userPreferred'],
                'imageUrl': media['coverImage']['medium'],
            }

            if not discordId in self.jobs:
                self.jobs[discordId] = [self.scheduler.add_job(self.sendAlert, trigger='date', run_date=airingAt, args=[alert_info])]
                continue
            self.jobs[discordId].append(self.scheduler.add_job(self.sendAlert, trigger='date', run_date=airingAt, args=[alert_info]))
            
        pass

    # Sends a discord embed with episode information
    async def sendAlert(self, alert_info):
        print("Alerted!")
        await alertEmbed(
            self.bot,
            alert_info['title'],
            alert_info['episode'],
            alert_info['imageUrl'],
            alert_info['channelId'],
            alert_info['discordId']
        )

        await self.setNextSchedule(
            alert_info['showId'],
            alert_info['discordId'],
            alert_info['channelId']
        )

    # disables alert for user and updates database
    async def stopAlert(self, discordId, ctx):
        user_data = getAlertUser(discordId)
        # print(user_data)
        if not user_data['enabled']:
            await ctx.respond("You don't have any alerts enabled")
            return
        
        # removes user from running jobs and db
        del self.jobs[discordId]
        removeAlertUser(discordId)
        await ctx.respond("Your alerts are now disabled!")

    # enables alert for user and updates database
    async def startAlert(self, discordId, channelId, ctx):
        user_data = getAlertUser(discordId)
        # print(user_data)
        if user_data['enabled']:
            await ctx.respond("Your already have alerts enabled")
            return
        
        await ctx.respond("Your alerts are now enabled!")
        addAlertUser(discordId, channelId)
        await self.activateAlerts(discordId, channelId)

    # Called when show episode airs and need to update notification for next episode
    async def setNextSchedule(self, showId, discordId, channelId):
        anime = getShowtime(showId)
        media = anime['Page']['media']
        status = media['status']

        # skip shows that have ended or doesn't have a schedule
        if not status == "RELEASING":
            return
        if not media['airingSchedule']['nodes']:
            return
        
        node = media['airingSchedule']['nodes'][0]
        airingAt = datetime.fromtimestamp(int(node['airingAt']))
        alert_info = {
            'discordId': discordId,
            'channelId': channelId,
            'episode': node['episode'],
            'title': media['title']['userPreferred'],
            'imageUrl': media['coverImage']['medium'],
        }

        if not discordId in self.jobs:
            self.jobs[discordId] = [self.scheduler.add_job(self.sendAlert, trigger='date', run_date=airingAt, args=[alert_info])]
            return
        self.jobs[discordId].append(self.scheduler.add_job(self.sendAlert, trigger='date', run_date=airingAt, args=[alert_info]))

    async def refreshSchedule(self):
        self.jobs = {}
        await self.initAlerts()
        
