import logging

logger = logging.getLogger()


class FollowUsers(object):

    def __init__(self, api, welcome_message=None):
        self.api = api
        self.welcome_message = welcome_message

    def follow_followers(self):
        logger.info("Looking for follow back followers")

        for follower in self.api.get_followers():
            if not follower.following:
                try:
                    follower.follow()
                    logger.info(f"\tFollow {follower.screen_name} ({follower.name})")
                    if self.welcome_message:
                        self.api.send_direct_message(follower.id, self.welcome_message)
                        logger.info(f"\tDirect message sent to {follower.screen_name} ({follower.name})")
                except Exception as e:
                    logger.error(f"An error occurred following follower {follower.screen_name} ({follower.name})",
                                 exc_info=True)

    def create_friendship(self, screen_name):
        try:
            self.api.create_friendship(screen_name=screen_name)
            logger.info(f"\tFollow {screen_name}")
        except Exception as e:
            logger.error(f"An error occurred following {screen_name}", exc_info=True)
