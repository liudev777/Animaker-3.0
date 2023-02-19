from requests_oauthlib import OAuth2Session
from pprint import pp
from requests_oauthlib import OAuth2Session
from flask import Flask, request
import os
import dotenv
import json
from multiprocessing import Process

dotenv.load_dotenv()
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

# 'http://localhost:8000/callback'
redirect_uri = "https://animaker3.herokuapp.com/"
authUrl = f'https://anilist.co/api/v2/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={redirect_uri}&response_type=code'

def getURL():
    return authUrl
    # webbrowser.open_new(authUrl)



def authenticate():

    app = Flask(__name__)


    @app.route('/')
    def index():
        code = request.args.get('code') #anilist auth will auto append this after user auths and open up this
        if not code:
            return "Code not provided"
        oauth = OAuth2Session(CLIENT_ID, redirect_uri=redirect_uri)
        authorization_url, state = oauth.authorization_url(authUrl)
        tokenUrl = 'https://anilist.co/api/v2/oauth/token'
        token = oauth.fetch_token(tokenUrl, code=code, client_secret=CLIENT_SECRET)
        print("token fetched!")
        # with open('tokens.json', 'w') as f:
        #     json.dump({'TOKEN': token['access_token']}, f)
        
        return f"You can close this page and go back to Discord!{token[0:20]}"

    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)

