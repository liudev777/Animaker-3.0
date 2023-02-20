from supabase import create_client, Client
import inspect
import os
import dotenv

# Connects to the Supabase api

dotenv.load_dotenv()
SUPABASE_URL: str = os.environ.get('SUPABASE_URL')
SUPABASE_KEY: str = os.environ.get('SUPABASE_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print('called!')

def viewData():
    data = supabase.table("tokens").select("*").execute()
    if len(data.data) <= 0:
        print("No Data Found :(", inspect.stack()[1].function)
        return
    print(data)
