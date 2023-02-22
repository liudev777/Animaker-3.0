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


def viewData(discordId):
    data = supabase.table("tokens").select("*").eq("discordId", discordId).execute().data
    if len(data) > 0:
        data = decrypt(data[0]['anilistToken'])
    # pp(data)
    else:
        print("No Data Found :(", inspect.stack()[1].function)
    return data



def insertData(discordId, anilistToken):
    table = supabase.table("tokens")
    row = table.select("*").eq("discordId", discordId).execute().data
    if (row):
        table.update({"discordId": discordId, "anilistToken": anilistToken}).eq("discordId", discordId).execute()
    else:
        table.insert({"discordId": discordId, "anilistToken": anilistToken}).execute()
    # print(data) #del

