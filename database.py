from supabase import create_client, Client
import inspect
import os
import dotenv

# Connects to the Supabase api

dotenv.load_dotenv()
SUPABASE_URL: str = os.environ['SUPABASE_URL']
SUPABASE_KEY: str = os.environ['SUPABASE_KEY']

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def viewData():
    data = supabase.table("tokens").select("*").execute()
    print(data.data)
    if len(data.data) <= 0:
        print("No Data Found :(", inspect.stack()[1].function)
        return
    print(data)



def insertData(discordId, anilistToken):
    table = supabase.table("tokens")
    row = table.select("*").eq("discordId", discordId).execute().data
    if (row):
        table.update({"discordId": discordId, "anilistToken": anilistToken}).eq("discordId", discordId).execute()
    else:
        table.insert({"discordId": discordId, "anilistToken": anilistToken}).execute()
    # print(data) #del

