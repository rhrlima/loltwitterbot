import os
import threading
import tweepy

import src.update_data as data
from src.post_builder import PostBuilder


class TwitterBot:

    def __init__(self):
        self._connect()
        self._initialize()

    def _connect(self):
        api_key = os.environ['lolbot_api']
        api_key_secret = os.environ['lolbot_api_secret']
        access_key = os.environ['lolbot_access']
        access_key_secret = os.environ['lolbot_access_secret']

        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_key, access_key_secret)
        self.api = tweepy.API(auth)

    def _initialize(self):
        data.get_updated_data()
        self.post_builder = PostBuilder()

    def post_data_update(self):
        self._initialize()
        curr_version = self.post_builder.champions_data['version']
        message = f'Champion data updated to version {curr_version}'
        self.post_tweet(message)

    def post_tweet(self, message=None):
        try:
            if message is None:
                message = self.post_builder.get_formated_message()
            # post and log
            print(self.api.update_status(message))
        except tweepy.TweepError as e:
            raise e

    def reply_tweet(self, id, reply_to, message):
        pass

    def _parse_request(self):
        pass

    def _execute_with_interval(self, func, seconds=60):
        def func_wrapper():
            self._execute_with_interval(func, seconds)
            func()
        threading.Timer(seconds, func_wrapper).start()

    def start(self):
        print('Bot Started')

        # first post
        self.post_data_update()
        self.post_tweet()

        # creates an infinite queue with posts every 1h
        self._execute_with_interval(self.post_tweet, 60 * 60)

        # creates an infinite queue for updating the data and posting every week
        self._execute_with_interval(
            self.post_data_update(), 
            60      # 1 minute
            * 60    # 1 hour
            * 24    # 1 day
            * 7     # 1 week
        )
