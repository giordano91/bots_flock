import logging

logger = logging.getLogger()


class RetweetTweet(object):

    def __init__(self, api):
        self.api = api

    def retweet_tweet(self, tweet_id):
        try:
            self.api.retweet(tweet_id)
            logger.info(f"\tTweet '{tweet_id}' retweeted")
        except Exception as e:
            logger.error(f"An error occurred in retweet_tweet on tweet id {tweet_id}", exc_info=True)
