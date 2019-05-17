
from nba import NBAScore
import twitter
import os

if __name__ == '__main__':
	api = twitter.Api(
		consumer_key=os.environ['TW_API_KEY'],
		consumer_secret=os.environ['TW_API_SECRET'],
		access_token_key=os.environ['TW_ACCESS_KEY'],
		access_token_secret=os.environ['TW_ACCESS_SECRET'])

	api.PostUpdate(NBAScore().get_status())
