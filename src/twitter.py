import os
import threading
import tweepy

import src.update_data as data
from src.bot import PostBuilder


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
        data.get_updated_data(force=False)
        self.post_builder = PostBuilder()

    def _post_tweet(self, message=None):
        try:
            if message is None:
                message = self.post_builder.get_formated_message()
            status = self.api.update_status(message)
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
        print('service started')
        self._post_tweet()
        self._execute_with_interval(self._post_tweet(), 3600)
