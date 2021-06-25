import requests
import json
from src import util
from src import conf
import time
import pathlib


def get_anime(id, request='', parameter=''):
    r = requests.get(util.JIKAN_API_Path + f'/anime/{id}/{request}/{parameter}')
    res = r.json()

    mask = util.ANIME_MASK 
    anime = {key:res[key] for key in mask}
    anime['studios'] = [studio['name'] for studio in anime['studios']]
    anime['genres'] = [genre['name'] for genre in anime['genres']]

    return anime
def get_season(year='',season=''):
    r = requests.get(util.JIKAN_API_Path + f'/season/{year}/{season}')
    season = r.json()

    mal_ids = [anime['mal_id'] for anime in season['anime'] if anime['type'] in ['TV', 'Movie']]
    season['anime'] = []

    time.sleep(3)

    for id in mal_ids:
        anime = get_anime(id)
        season['anime'].append( anime )
        #time.sleep(0 if anime['request_cached'] else 3) # not working
        time.sleep(3)
        #with open('./season_temp.json', 'w') as f:
        #  json.dump(season, f, indent=4)

    return season
def get_user(username, request='animelist', argument='all'):
    print(f"fetching list for {username}...")
    path = pathlib.Path(__file__).parent.parent / f'cache/{username}.json'
    if path.exists():
        print('results cached, fetching from file...')
        with path.open('r') as f:
            user = f.read()
        print('done.')
        try:
            return json.loads(user)
        except Exception:
            return None 
    else:
        path.touch()
        r = requests.get(util.JIKAN_API_Path + f'/user/{username}/{request}/{argument}')
        user = r.json()

        mal_ids = [anime['mal_id'] for anime in user['anime'] if anime['type'] in ['TV', 'Movie']]
        user_score = [anime['score'] for anime in user['anime'] if anime['type'] in ['TV', 'Movie']]
        user['anime'] = []

        time.sleep(3)
        print(f'fetching {len(mal_ids)} individual animes (this might take a while)...')
        i = 0
        for id in mal_ids:
            anime = get_anime(id)
            if conf.Config.get().DEBUG: util.printProgressBar(i+1, len(mal_ids), decimals=2)
            i = i+1
            user['anime'].append( anime )
            #time.sleep(0 if anime['request_cached'] else 3) # not working
            time.sleep(3)
            #with open('./user_temp.json', 'w') as f:
            #  json.dump(user, f, indent=4)
        for i in range(len(user_score)):
            user['anime'][i]['user_score'] = user_score[i]

        print(f'creating cache for {username}')
        with path.open('w') as f:
            json.dump(user, f)
        print('done.')
        return user

def get_season_raw(year='',season=''):
    r = requests.get(util.JIKAN_API_Path + f'/season/{year}/{season}')
    season = r.json()

    mask = [#"request_hash", #"request_cached", #"request_cache_expiry",
      "season_name", "season_year", "anime"]
    season = {key:season[key] for key in mask}

    animes = [anime for anime in season['anime'] if anime['type'] in ['TV', 'Movie']]
    season['anime'] = []

    mask = util.SEASON_ANIME_MASK 
    for anime in animes:
        anime = {key:anime[key] for key in mask}

        anime['studios'] = [studio['name'] for studio in anime.pop('producers')]
        anime['genres'] = [genre['name'] for genre in anime['genres']]

        season['anime'].append( anime )


    return season
def get_user_raw(username=None, request='animelist', argument='all'):
    r = requests.get(util.JIKAN_API_Path + f'/user/{username}/{request}/{argument}')
    user = r.json()

    mask = [#"request_hash", #"request_cached", #"request_cache_expiry",
      "anime"]
    user = {key:user[key] for key in mask}
    
    animes = [anime for anime in user['anime'] if anime['type'] in ['TV', 'Movie']]
    user['anime'] = []

    mask = util.USER_ANIME_MASK 
    for anime in animes:
        anime = {key:anime[key] for key in mask}

        anime['studios'] = [studio['name'] for studio in anime['studios']]

        user['anime'].append( anime )

    return user
