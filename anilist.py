from pprint import pp
from database import viewData, getAllUsers, updateUserShows, updateShows, clearAllUserShows, clearAllShows, clearUserShows
import requests
import json
import hikari
from query import query1, query2, query3, query4

url = 'https://graphql.anilist.co'


# updates the database for all user and the shows they are watching
def renewAllUserShowDB(): 
    allUsers = getAllUsers()
    # print(allUsers) #del
    # clearAllUserShows() #delete the userShows entries 
    # clearAllShows() # delete the shows entries
    for user in allUsers:
        renewUserShowDB(user['discordId'])

def renewUserShowDB(discordId):
    clearUserShows(discordId)
    currShows = getCurrShowtimes(discordId)
    # pp(currShows)
    for media in currShows['Page']['media']: # repopulate userShows entries with updated shows
        # pp(media)
        # pp("\n")
        showId = media['id']
        title = media['title']['userPreferred']
        status = media['status']
        timeUntilAiring = None
        if not status == "FINISHED":
            status = True
            if media['airingSchedule']['nodes']:
                timeUntilAiring = media['airingSchedule']['nodes'][0]['timeUntilAiring']
                print("TIME UNTIL AIRING: ", timeUntilAiring) #del
        else: 
            status = False
        print("FIELDS: \n", showId, title, status, timeUntilAiring)
        updateShows(showId, title, status, timeUntilAiring)
        # print(showId)
        updateUserShows(discordId, showId)

def getUserShowtime():
    renewAllUserShowDB()

# Query that requires user token
def __getAuthQuery(discordId, variables, query):
    access_token = viewData(discordId)
    if not access_token:
        return -1

    headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    }
    data = {
        'query': query,
        'variables': variables
    }

    response = requests.post(url, headers=headers, json=data)
    return response

# Public query for general information
def __getQuery(variables, query):

    data = {
        'query': query,
        'variables': variables
    }

    response = requests.post(url, json=data)
    return response

# Lists search results of inputted anime title
def testQuery(discordId, anime_title):

    variables = {
        'search': anime_title
    }
    response = __getAuthQuery(discordId, variables, query1)

    if response == -1:
        return "please login using /login first!"
    
    if not response:
        return "No Shows Found"

    print(response.status_code)
    if response.status_code == 200:
        data = json.loads(response.text)['data']
        # pp(data)
        viewer = data['Viewer']['name']
        titles = [media['title']['userPreferred'] for media in data['Page']['media'] ]
        pp (titles)
        titlesStr = "\n".join(titles)
        info = f'Viewer: {viewer}\n\nTitles:\n{titlesStr}'
        return info
    return "data not found"

# returns the discord output of current anime watchlist
def getCurrAnimeList(discordId):
    data = __getCurrShows(discordId)
    # pp(data) #del
    if not data:
        return -1
    return data

# returns discord output of current anime watchlist airtimes
def getCurrShowtimes(discordId):
    data = __getCurrShows(discordId)
    # print("DATA: ", data)
    if not data:
        return "No Current Shows"
    name = data['User']['name']
    entries = data['MediaListCollection']['lists'][0]['entries']
    showIds = [entrie['media']['id'] for entrie in entries]

    variables = {
        "mediaIds": showIds
    }
    response = __getQuery(variables, query4)
    if response.status_code == 200:
        data = json.loads(response.text)['data']
        return data
        
    return -1
    

# gets some information about current watchlist
def __getCurrShows(discordId):
    viewer_id = __getUserId(discordId)
    if viewer_id == -1:
        return "Please login using /login first!"
    if not viewer_id:
        return "User Not Found"
    print("viewer id: ", viewer_id)
    variables = {
        'userId': viewer_id
    }
    response = __getQuery(variables, query3)
    print(response.status_code)
    if response.status_code == 200:
        data = json.loads(response.text)['data']
        return data
    return "Something went wrong"

# returns the user id of the current user
def __getUserId(discordId):
    variables = {}
    response = __getAuthQuery(discordId, variables, query2)

    if response == -1 or response == False:
        return response

    if response.status_code == 200:
        data = json.loads(response.text)['data']
        print("getUserId(): ", data)
        viewer_id = data['Viewer']['id']
        # watch_list = data['']
        return viewer_id
    return False

    pass