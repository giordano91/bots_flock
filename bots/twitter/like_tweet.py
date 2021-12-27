import logging

logger = logging.getLogger()


class LikeTweet(object):

    def __init__(self, api):
        self.api = api

    def like_tweet(self, tweet_id):
        try:
            self.api.create_favorite(tweet_id)
            logger.info(f"\tTweet '{tweet_id}' liked")
        except Exception as e:
            logger.error(f"An error occurred in like_tweet on tweet id {tweet_id}", exc_info=True)
