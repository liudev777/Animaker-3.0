from pprint import pp
from database import viewData
import requests
import json

query = '''
query ($search: String) {
    Viewer {
        name
    }
    Page(perPage: 10) {
        media(search: $search, type: ANIME) {
        id
        title {
            romaji
            english
            native
        }
        airingSchedule {
            nodes {
            episode
            airingAt
            }
        }
    }
  }
}
'''
url = 'https://graphql.anilist.co'


def testQuery(discordId, anime_title):
    access_token = viewData(discordId)
    if not access_token:
        return "please login using /login first!"
    variables = {
        'search': anime_title
    }
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

    print(response.status_code)
    if response.status_code == 200:
        data = json.loads(response.text)['data']
        # pp(data)
        viewer = data['Viewer']['name']
        titles = [media['title']['english'] if media['title']['english'] is not None else media['title']['romaji'] for media in data['Page']['media'] ]
        pp (titles)
        titlesStr = "\n".join(titles)
        info = f'Viewer: {viewer}\n\nTitles:\n{titlesStr}'
        return info
    return "data not found"

    
    pass