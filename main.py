#!venv/bin/python3

from nba import NBAScore
from twitter import *
import sys
import json

if __name__ == '__main__':

    if len(sys.argv) <= 1:
        sys.exit()

    with open(sys.argv[1]) as f:
        keys = json.loads(f.read())

    api = Twitter(
        auth=OAuth(
            keys['access_key'],
            keys['access_secret'],
            keys['consumer_key'],
            keys['consumer_secret']
        )
    )

    if len(sys.argv) >= 3:
        commit_type = sys.argv[2]
        if commit_type == 'print':
            commit_fn = print
        else:
            commit_fn = lambda x: api.statuses.update(status=x)

    commit_fn(NBAScore().get_status())
