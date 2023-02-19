from oauthlib.oauth2 import BackendApplicationClient
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

redirect_uri = 'http://localhost:8000/callback'
authUrl = f'https://anilist.co/api/v2/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={redirect_uri}&response_type=code'

def getURL():
    return authUrl
    # webbrowser.open_new(authUrl)



def authenticate():

    app = Flask(__name__)


    @app.route('/callback')
    def callback():
        code = request.args.get('code') #anilist auth will auto append this after user auths and open up this

        oauth = OAuth2Session(CLIENT_ID, redirect_uri=redirect_uri)
        authorization_url, state = oauth.authorization_url(authUrl)
        tokenUrl = 'https://anilist.co/api/v2/oauth/token'
        token = oauth.fetch_token(tokenUrl, code=code, client_secret=CLIENT_SECRET)
        with open('tokens.json', 'w') as f:
            json.dump({'TOKEN': token['access_token']}, f)
        
        return "You can close this page and go back to Discord!"

    app.run(port=8000)