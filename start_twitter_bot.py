import argparse

from bots.twitter.auth import create_twitter_api
from bots.twitter.stream_listener import TwitterStreamListener

parser = argparse.ArgumentParser(description="Anomaly detection project")

parser.add_argument("-lt", "--like_tweet", action="store_true",
                    help="If this parameter is present, a like is left on tweets that match keywords")

args = parser.parse_args()

like_tweet_enabled = args.like_tweet

# todo: add checks on input parameters

if like_tweet_enabled:
    api = create_twitter_api()

    tweets_listener = TwitterStreamListener(api, like_tweet_enabled)
    tweets_listener.filter(track=["#python"], languages=["en"])
