from pprint import pp
from supabase import create_client, Client
from encryp import decrypt
import inspect
import os
import dotenv

# Connects to the Supabase api

dotenv.load_dotenv()
SUPABASE_URL: str = os.environ['SUPABASE_URL']
SUPABASE_KEY: str = os.environ['SUPABASE_KEY']

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# gets the anilist token from discord 
def viewData(discordId):
    data = supabase.table("tokens").select("*").eq("discordId", discordId).execute().data
    if len(data) > 0:
        data = decrypt(data[0]['anilistToken'])
    # pp(data)
    else:
        print("No Data Found :(", inspect.stack()[1].function)
    return data


# insert 
def updateToken(discordId, anilistToken):
    try:
        table = supabase.table("tokens")
        row = table.select("*").eq("discordId", discordId).execute().data
        if (row):
            table.update({"discordId": discordId, "anilistToken": anilistToken}).eq("discordId", discordId).execute()
        else:
            table.insert({"discordId": discordId, "anilistToken": anilistToken}).execute()
    except Exception as e: 
        print ("updateToken: ", e)



def updateUserShows(discordId, showId):
    try:
        table = supabase.table("userShows")
        table.insert({"discordId": discordId, "showId": showId}).execute().data
        # print("done") #del
        return 1
    except Exception as e:
        print ("updateUserShows: ", e)

def clearAllUserShows():
    try:
        table = supabase.table("userShows")
        table.delete().neq("discordId", 0).execute()
        print("deleted ALL userShows db") #del
    except Exception as e:
        print ("clearAllUserShow: ", e)

def clearUserShows(discordId):
    try:
        table = supabase.table("userShows")
        table.delete().eq("discordId", discordId).execute()
        print("deleted userShows db") #del
    except Exception as e:
        print ("clearUserShow: ", e)    
        
def updateShows(showId, showName, status, timeUntilAir):
    try:
        table = supabase.table("shows")
        row = table.select("showId").eq("showId", showId).execute().data
        # pp("\n")
        # pp(row)
        if (row):
            table.update({"showId": showId, "showName": showName, "status": status, "timeUntilAir": timeUntilAir}).eq("showId", showId).execute()
            # print("show updated!: ", showId, showName, status, timeUntilAir)
        else:
            table.insert({"showId": showId, "showName": showName, "status": status, "timeUntilAir": timeUntilAir}).execute()
            # print("show not in db, adding it now: ", showName)
    except Exception as e:
        print("updateShows: ", e)

def clearAllShows():
    try:
        table = supabase.table("shows")
        table.delete().neq("showId", 0).execute()
        print("deleted ALL Shows db") #del
    except Exception as e:
        print ("clearAllUserShow: ", e)
    

def getAllUsers():
    data = supabase.table("tokens").select("discordId").execute().data
    if (data):
        pp(data) #del
        return data
    else:
        print("getAllShowtime: No data found :(")
    pass

def getAiringShows(discordId):
    try:
        data = supabase.table("userShows").select("*, shows(status, timeUntilAir, showName)").eq("discordId", discordId).execute().data
        return data
    except Exception as e:
        print("getAiringShows: ", e)

    return None
