
from nba import NBAScore
import twitter
import os
import json

if __name__ == '__main__':

	with open('api_keys.json') as f:
		keys = json.loads(f.read())

	api = twitter.Api(
		consumer_key=keys['consumer_key'],
		consumer_secret=keys['consumer_secret'],
		access_token_key=keys['access_key'],
		access_token_secret=keys['access_secret'])

	api.PostUpdate(NBAScore().get_status())
