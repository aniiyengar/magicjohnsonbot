
from base import BaseScore
import requests
from bs4 import BeautifulSoup
import datetime, pytz

NBA_SCORES_URL = 'https://www.usatoday.com/sports/nba/scores/'
NBA_TEAMS_URL = 'https://www.basketball-reference.com/teams/'

class NBAScore(BaseScore):

    type = 'nba'

    def __init__(self):
        super().__init__()

        self.teams = {}
        r = requests.get(NBA_TEAMS_URL)

        if r.status_code != 200:
            return None

        bs = BeautifulSoup(r.text, 'html.parser')

        for line in bs.select('#teams_active .full_table'):
            a = line.select('.left a')[0]
            abbr = a.get('href').split('/')[2]
            name = a.text.strip().rsplit(' ', 1)
            self.teams[abbr] = name

        # Hack
        self.teams['POR'] = ['Portland', 'Trail Blazers']

    def get_game(self):
        r = requests.get(NBA_SCORES_URL)

        if r.status_code != 200:
            return None

        root_bs = BeautifulSoup(r.text, 'html.parser')
        link = root_bs.select('.game.post-event li.contextlinks ' + \
            'a[data-ht="sportsnbascoresboxscore"]')[0].get('href')

        r = requests.get('https://www.usatoday.com' + link)

        if r.status_code != 200:
            return None

        bs = BeautifulSoup(r.text, 'html.parser')
        info = {}

        day = bs.select('.headline-wrapper .details p:first-child')[0]
        tz = pytz.timezone('America/Los_Angeles')
        new_d = pytz.utc.localize(datetime.datetime.today())
        new_d = new_d.astimezone(tz)
        day_str = new_d.strftime("%A, %B %d")

        if day.text.strip() != day_str:
            return None

        details = bs.select('.teams-wrapper .details')[0]
        for loc in ['home', 'away']:
            score = int(details.select('.team.' + loc + ' .odds')[0].text)
            team = details.select('.team.' + loc + ' h2')[0].text.strip()
            abbr = [key for key in self.teams.keys() \
                    if self.teams[key][1] == team][0]
            
            info[loc] = {
                'team': {
                    'abbr': abbr,
                    'city': self.teams[abbr][0],
                    'name': self.teams[abbr][1]
                },
                'score': score
            }

        charts = bs.select('.chart.player-stats')
        for chart in charts:
            players = []
            header = chart.select('tr')[0]
            team = header.select('td')[0].text.strip().split()[-1]
            
            # Hack again
            if team == 'Blazers':
                team = 'Trail Blazers'

            abbr = [key for key in self.teams.keys() \
                    if self.teams[key][1] == team][0]
            
            rows = chart.select('tr[class]:not(.highlight)')
            for row in rows:
                player = row.select('td:first-child')[0].text.strip()
                player = player.split('(')[0].strip()
                pts = int(row.select('td:last-child')[0].text.strip())

                players.append({ "name": player, "pts": pts })

            players.sort(key=lambda x: -x['pts'])

            for loc in ['home', 'away']:
                if info[loc]['team']['abbr'] == abbr:
                    info[loc]['players'] = players

        if info['home']['score'] > info['away']['score']:
            return info['home'], info['away']
        else:
            return info['away'], info['home']
