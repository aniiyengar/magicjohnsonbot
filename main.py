#!venv/bin/python3

from nba import NBAScore
from twitter import *
import sys
import json

if __name__ == '__main__':

    if len(sys.argv) <= 1:
        sys.exit()

    # with open(sys.argv[1]) as f:
    #     keys = json.loads(f.read())

    # api = Twitter(
    #     auth=(
    #         keys['access_key'],
    #         keys['access_secret'],
    #         keys['consumer_key'],
    #         keys['consumer_secret']
    #     )
    # )
    # api.statuses.update(status=NBAScore().get_status())
    print(NBAScore().get_status())
