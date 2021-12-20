import tweepy
import os
import logging

from bots.twitter.like_tweet import LikeTweet

logger = logging.getLogger()


class TwitterStreamListener(tweepy.Stream):

    def __init__(self, api, like_tweet_enabled):
        # get twitter app credentials
        consumer_key = os.environ['TWITTER_CONSUMER_KEY']
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
        access_token = os.environ['TWITTER_ACCESS_TOKEN']
        access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
        super().__init__(consumer_key, consumer_secret, access_token, access_token_secret)

        self.api = api
        self.authenticated_user = api.verify_credentials()

        if like_tweet_enabled:
            self.like_tweet_manager = LikeTweet(self.api)

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")

        # discard replies or own tweets
        if tweet.in_reply_to_status_id is not None or tweet.user.id == self.authenticated_user.id:
            return

        # put like if it has not been done yet
        if not tweet.favorited:
            self.like_tweet_manager.like_tweet(tweet.id)

        # retweet if it has not been done yet
        if not tweet.retweeted:
            pass

        # todo: add a comment

    def on_error(self, status):
        logger.error(status)
