import datetime
import json
import random
import threading
import twitter


#loads the base configurations for access keys
config = json.loads(open("config.json").read()) #


#set up the connection with the twitter api
api = twitter.Api(
	consumer_key		=	config['consumer_key'],
	consumer_secret		=	config['consumer_secret'],
	access_token_key	=	config['access_token_key'],
	access_token_secret	=	config['access_token_secret']
)


#loads the champions data from json file
classes = json.loads(open("classes.json").read()) # load champions


#get a random champion from a random class if not specified
def get_random_pick(cls=None):
	if cls is None:
		cls = random.choice(list(classes.keys()))
	return random.choice(classes[cls])


#post a tweet with the given message
def post_tweet(message):
	if len(message) < 140:
		status = api.PostUpdate(message)
		update_status(status.text)
	else:
		update_status("message is too long", "ERROR")


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


def update_status(text, status=None):
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