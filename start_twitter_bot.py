import argparse
import logging

from bots.twitter.auth import create_twitter_api
from bots.twitter.stream_listener import TwitterStreamListener

# set up logging to file
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S',
                    filename='twitter_bot.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)


parser = argparse.ArgumentParser(description="Bots Flock")
parser.add_argument("-l", "--like_tweet", action="store_true",
                    help="If this parameter is present, a like is left on tweets that match keywords")
parser.add_argument("-r", "--retweet_tweet", action="store_true",
                    help="If this parameter is present, a retweet is done on tweets that match keywords")
parser.add_argument("-kt", "--keywords_to_track", nargs="+", type=str, help="Specify list of keywords to track")
parser.add_argument("-lt", "--languages_to_track", nargs="+", type=str, help="Specify list of languages to track")
parser.add_argument("-iph", "--interactions_per_hour", type=int, help="Number of tweets considered per hour. This is "
                                                                      "useful to do not overload the API and the daily"
                                                                      " interactions")

args = parser.parse_args()
like_tweet_enabled = args.like_tweet
retweet_tweet_enabled = args.retweet_tweet
keywords_to_track = args.keywords_to_track
languages_to_track = args.languages_to_track
interactions_per_hour = args.interactions_per_hour

# todo: add checks on input parameters

# create api
api = create_twitter_api()

if like_tweet_enabled or retweet_tweet_enabled:
    tweets_listener = TwitterStreamListener(api, like_tweet_enabled, retweet_tweet_enabled, interactions_per_hour)
    tweets_listener.filter(track=keywords_to_track, languages=languages_to_track, threaded=True)
