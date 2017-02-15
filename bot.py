import datetime
import json
import random
import sys
import threading
import tweepy

#loads the base configurations for access keys
config = json.loads(open("config.json").read()) #


#set up the connection with the twitter api
auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
auth.set_access_token(config['access_token_key'], config['access_token_secret'])
#authorizing the connection
api = tweepy.API(auth)


#loads the champions data from json file
classes = json.loads(open("classes.json").read()) # load champions


class BotStreamListener(tweepy.StreamListener):

	def on_status(self, status):
		print(status.text)

	def on_error(self, status_code):
		if status_code == 420:
			return False


listener = BotStreamListener()
stream = tweepy.Stream(auth = api.auth, listener = listener)


#get a random champion from a random class if not specified
def get_random_pick(cls=None):
	if cls is None:
		cls = random.choice(list(classes.keys()))
	return random.choice(classes[cls])


#post a tweet with the given message
def post_tweet(message):
	try:
		status = api.update_status(message)
		set_status(status.text)
	except tweepy.TweepError as e:
		data = json.loads(e.reason.replace("[", "").replace("]", "").replace("'", "\""))
		set_status(data['message'], "ERROR")


def reply_tweet(message):
	pass


#---


def starting_tweet():
	text = "I am alive! #whatShouldIPick"
	post_tweet(text)


def recommend_pick():
	champion = get_random_pick()
	text = "You should try " + champion['name'] + " " + champion['title'] + "! #whatShouldIPick"
	post_tweet(text)


#---


def set_status(text, status=None):
	time = datetime.datetime.now()
	status_text = str(time)
	if status is None:
		status_text += "\t<<tweeting>>"
	elif status == "ERROR":
		status_text += "\t<<error>>"
	else:
		status_text += "\t<<unkown>>"
	status_text += "\t" + text
	print(status_text)


#executes the given function after each X seconds
def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


#starting_tweet() #Initial bot tweet
#set_interval(recommend_pick, 60*60) #Tweets a pick each 1h

print("Listener bot")
stream.filter(track=['@what_pick'], async=True)

def hello():
	print("Hello")

set_interval(hello, 5)