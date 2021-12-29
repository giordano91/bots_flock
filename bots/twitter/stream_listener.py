import logging
import os
import time

import tweepy

from bots.twitter.follow_users import FollowUsers
from bots.twitter.like_tweet import LikeTweet
from bots.twitter.retweet_tweet import RetweetTweet

logger = logging.getLogger()


class TwitterStreamListener(tweepy.Stream):

    def __init__(self, api, like_tweet_enabled, retweet_tweet_enabled, interactions_per_hour, follow_tweet_author):
        # get twitter app credentials
        consumer_key = os.environ['TWITTER_CONSUMER_KEY']
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
        access_token = os.environ['TWITTER_ACCESS_TOKEN']
        access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
        super().__init__(consumer_key, consumer_secret, access_token, access_token_secret)

        self.api = api
        self.authenticated_user = api.verify_credentials()
        self.authenticated_user_followers = self.api.get_followers()

        self.like_tweet_enabled = like_tweet_enabled
        self.retweet_tweet_enabled = retweet_tweet_enabled
        self.follow_tweet_author = follow_tweet_author

        if self.like_tweet_enabled:
            self.like_tweet_manager = LikeTweet(self.api)

        if self.retweet_tweet_enabled:
            self.retweet_tweet_manager = RetweetTweet(self.api)

        if self.follow_tweet_author:
            self.follow_manager = FollowUsers(self.api)

        self.start_date = time.time()
        self.current_interactions = 0
        self.interactions_per_hour = interactions_per_hour

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")

        # discard replies or own tweets and already liked tweets
        if tweet.in_reply_to_status_id is not None or tweet.favorited or tweet.user.id == self.authenticated_user.id:
            return

        if self.interactions_per_hour:
            current_time = time.time()
            # number of interactions exceed the allowed per hour
            if self.current_interactions >= self.interactions_per_hour and (current_time - self.start_date) <= 3600:
                return
            # reset counter for the next hour
            elif (current_time - self.start_date) > 3600:
                self.current_interactions = 0
                self.start_date = time.time()
                return

        # put like if it has not been done yet
        if self.like_tweet_enabled and not tweet.favorited:
            self.like_tweet_manager.like_tweet(tweet.id)

        time.sleep(1)

        # retweet if it has not been done yet
        if self.retweet_tweet_enabled and not tweet.retweeted:
            self.retweet_tweet_manager.retweet_tweet(tweet.id)

        time.sleep(1)

        # follow the author of the tweet
        if self.follow_tweet_author and tweet.user not in self.authenticated_user_followers:
            self.follow_manager.create_friendship(tweet.user.screen_name)
            self.authenticated_user_followers.append(tweet.user)

        time.sleep(1)
        # todo: add a comment

        self.current_interactions += 1

    def on_error(self, status):
        logger.error(status)
