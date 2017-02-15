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
		set_status("reply event triggered", "LOG")
		parse_request(
			status.in_reply_to_screen_name,
			status.user.screen_name,
			status.text)


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


def reply_tweet(to, message):
	message = "@" + to + " " + message
	post_tweet(message)


def parse_request(to, replyto, text):
	if to == "what_pick":
		if "#assassin" in text.lower():
			recommend_pick(replyto, "ASSASSIN")
		elif "#fighter" in text.lower():
			recommend_pick(replyto, "FIGHTER")
		elif "#mage" in text.lower():
			recommend_pick(replyto, "MAGE")
		elif "#marksman" in text.lower():
			recommend_pick(replyto, "MARKSMAN")
		elif "#support" in text.lower():
			recommend_pick(replyto, "SUPPORT")
		elif "#tank" in text.lower():
			recommend_pick(replyto, "TANK")
		else:
			reply_tweet(replyto, "Try use #assassin #fighter #mage #marksman #support #tank ")


#---


def starting_tweet():
	text = "I am alive! #whatShouldIPick"
	post_tweet(text)


def recommend_pick(to=None, cls=None):
	champion = get_random_pick(cls)
	text = ""
	if to is not None:
		text += "@" + to + " "
	text += "You should try " + champion['name'] + " " + champion['title'] + "! #whatShouldIPick"
	post_tweet(text)


#---


def set_status(text, status=None):
	time = datetime.datetime.now()
	status_text = str(time)
	if status is None:
		status_text += "\t<<tweeting>>"
	elif status is "TRIGGER":
		status_text += "\t<<triggered>>"
	elif status is "ERROR":
		status_text += "\t<<error>>"
	elif status is "LOG":
		status_text += "\t<< log >>"
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


set_status("starting lol twitter bot", "LOG")

#starting_tweet() #Initial bot tweet

#Tweets a random pick each 1h
set_interval(recommend_pick, 60*60)

#Stream that reaplies to given keywords
stream.filter(track=['@what_pick'], async=True)