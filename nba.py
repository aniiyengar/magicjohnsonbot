
from base import BaseScore
import requests
from bs4 import BeautifulSoup
import datetime, pytz
import json
import random

NBA_SCORES_URL = 'https://www.espn.com/nba/scoreboard/'
NBA_TEAMS_URL = 'https://www.basketball-reference.com/teams/'

class NBAScore(BaseScore):

    type = 'nba'

    def get_game(self):
        r = requests.get('https://data.nba.com/data/5s/v2015/json/mobile_teams/nba/2019/scores/00_todays_scores.json')

        if r.status_code != 200:
            return None

        games = [g for g in json.loads(r.text)['gs']['g'] if g['stt'] == 'Final']
        game_id = random.choice(games)['gid']

        r = requests.get('https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2019/scores/gamedetail/' + game_id + '_gamedetail.json')

        if r.status_code != 200:
            return None

        info = {}

        stats = json.loads(r.text)['g']
        stats['home'], stats['away'] = stats['hls'], stats['vls']

        for loc in ['home', 'away']:
            score = stats[loc]['s']
            abbr = stats[loc]['ta']

            info[loc] = {
                'team': {
                    'abbr': abbr,
                    'city': stats[loc]['tc'],
                    'name': stats[loc]['tn']
                },
                'score': score
            }

            players = stats[loc]['pstsg']
            for player in players:
                player['name'] = player['fn'] + ' ' + player['ln']

            players.sort(key=lambda x: -x['pts'])
            info[loc]['players'] = players

        if info['home']['score'] > info['away']['score']:
            return info['home'], info['away']
        else:
            return info['away'], info['home']
