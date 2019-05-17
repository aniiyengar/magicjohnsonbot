
from nba import NBAScore
import twitter
import sys
import json

if __name__ == '__main__':

	if len(sys.argv) <= 1:
		sys.exit()

	with open(sys.argv[1]) as f:
		keys = json.loads(f.read())

	api = twitter.Api(
		consumer_key=keys['consumer_key'],
		consumer_secret=keys['consumer_secret'],
		access_token_key=keys['access_key'],
		access_token_secret=keys['access_secret'])

	api.PostUpdate(NBAScore().get_status())
