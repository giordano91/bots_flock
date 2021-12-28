import argparse
import logging
import time

import schedule

from bots.twitter.auth import create_twitter_api
from bots.twitter.follow_followers import FollowFollowers
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
parser.add_argument("-ff", "--follow_followers", action="store_true", help="If this parameter is present, you will "
                                                                           "automatically follow every person who "
                                                                           "follows you. This check is done every four"
                                                                           "hours")
parser.add_argument("-fta", "--follow_tweet_author", action="store_true",
                    help="If this parameter is present, the author of the tweet you interacted with will be followed")


args = parser.parse_args()
like_tweet_enabled = args.like_tweet
retweet_tweet_enabled = args.retweet_tweet
keywords_to_track = args.keywords_to_track
languages_to_track = args.languages_to_track
interactions_per_hour = args.interactions_per_hour
follow_followers = args.follow_followers
follow_tweet_author = args.follow_tweet_author

# todo: add checks on input parameters

# create api
api = create_twitter_api()

# a new thread starts to monitor new tweets based on selected keywords and languages
if like_tweet_enabled or retweet_tweet_enabled:
    tweets_listener = TwitterStreamListener(api, like_tweet_enabled, retweet_tweet_enabled, interactions_per_hour,
                                            follow_tweet_author)
    tweets_listener.filter(track=keywords_to_track, languages=languages_to_track, threaded=True)

# schedule every hour a check to follow new followers
if follow_followers:
    follow_followers_manager = FollowFollowers(api)
    follow_followers_manager.follow_followers()
    schedule.every(4).hours.do(follow_followers_manager.follow_followers)

# apply all the pending schedules
while True:
    schedule.run_pending()
    time.sleep(1)
