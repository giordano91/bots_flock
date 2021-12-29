import logging

logger = logging.getLogger()


class FollowFollowers(object):

    def __init__(self, api):
        self.api = api

    def follow_followers(self):
        logger.info("Looking for follow back followers")

        for follower in self.api.get_followers():
            if not follower.following:
                try:
                    follower.follow()
                    logger.info(f"\tFollow {follower.screen_name} ({follower.name})")
                except Exception as e:
                    logger.error(f"An error occurred following follower {follower.screen_name} ({follower.name}",
                                 exc_info=True)

    def create_friendship(self, screen_name):
        try:
            self.api.create_friendship(screen_name=screen_name)
            logger.info(f"\tFollow {screen_name}")
        except Exception as e:
            logger.error(f"An error occurred following {screen_name}", exc_info=True)
