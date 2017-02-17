import datetime
import json
import random
import re
import sys
import threading
import tweepy


#loads the base configurations for access keys
config = json.loads(open("config.json").read()) #

#set up the connection with the twitter api
auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
auth.set_access_token(config['access_token_key'], config['access_token_secret'])
api = tweepy.API(auth)

classes = json.loads(open("classes.json").read()) # load champions

phrases = json.loads(open("phrases.json").read()) # load phrases


class BotStreamListener(tweepy.StreamListener):

	def on_status(self, status):
		set_status("Reply event triggered.", "LOG")
		parse_request(
			status.id,
			status.in_reply_to_screen_name,
			status.user.screen_name,
			status.text)


	def on_error(self, status_code):
		if status_code == 420:
			return False


#get a random champion from a random class if not specified
def get_random_pick(cls=None):
	if cls is None:
		cls = random.choice(list(classes.keys()))
	return random.choice(classes[cls])


#generates a recommendation
def recommend_pick(to=None, cls=None):
	champion = get_random_pick(cls)
	if to is not None:
		return random.choice(phrases['replies']).format(to, champion['name'], champion['title'])
	else:
		return random.choice(phrases['posts']).format(champion['name'], champion['title'])


index = 0
def get_rotate_pick():
	global index
	sequence = ["ASSASSIN", "FIGHTER", "MAGE", "MARKSMAN", "SUPPORT", "TANK"]
	post_tweet(recommend_pick(cls = sequence[index]))
	index = (index + 1 if index < len(sequence)-1 else 0)


#post a tweet with the given message
def post_tweet(message):
	attempts = 0
	while attempts < 5:
		try:
			status = api.update_status(message)
			set_status("Tweeting: " + status.text, "LOG")
			break
		except tweepy.TweepError as e:
			attempts += 1
			if attempts < 5:
				set_status("Erro ocorrido ao postar tweet, tentando novamente.", "ERROR")
			else:
				set_status(parse_error(e.reason), "ERROR")


#post a reply to a given tweet
def reply_tweet(id, to, message):
	try:
		status = api.update_status(message, id)
		set_status("Replying: " + status.text, "LOG")
	except tweepy.TweepError as e:
		set_status(parse_error(e.reason), "ERROR")


#parse keyword
def parse_request(id, to, replyto, text):
	if to == "what_pick":
		if "#assassin" in text.lower():
			text = recommend_pick(replyto, "ASSASSIN")
		elif "#fighter" in text.lower():
			text = recommend_pick(replyto, "FIGHTER")
		elif "#mage" in text.lower():
			text = recommend_pick(replyto, "MAGE")
		elif "#marksman" in text.lower():
			text = recommend_pick(replyto, "MARKSMAN")
		elif "#support" in text.lower():
			text = recommend_pick(replyto, "SUPPORT")
		elif "#tank" in text.lower():
			text = recommend_pick(replyto, "TANK")
		else:
			text = phrases['errors']["keyword_error"].format(replyto)
		reply_tweet(id, replyto, text)


def parse_error(error):
	data = json.loads(re.sub("[\[\]]", "", error).replace("'", "\""))
	error_code = str(data['code'])
	error_message = data['message']
	return error_code + " " + error_message


def start_stream():
	listener = BotStreamListener()
	stream = tweepy.Stream(auth = api.auth, listener = listener)
	try:
		stream.filter(track=['@what_pick'], async=True)
		set_status("Reply sytem started.", "LOG")
	except tweepy.TweepError as e:
		set_status(parse_error(e.reason), "ERROR")

#print given message to the log with different status
def set_status(text, status=None):
	if status is "LOG":
		status = "<< log >>"
	elif status is "ERROR":
		status = "<<error>>"		
	else:
		status = "<<unkown>>"
	time = datetime.datetime.now()
	print("{0}\t{1}\t{2}".format(str(time), status, text))


#executes the given function after each X seconds
def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def start_bot():
	try:
		api.verify_credentials()							#Authenticate keys
		set_status("Starting bot.", "LOG")

		get_rotate_pick()									#Start with first tweet
		set_status("Initial tweet.", "LOG")

		set_interval(get_rotate_pick, 60*10)				#Tweets a pick each 10h following a sequence
		set_status("Recommendation started.", "LOG")

		start_stream()										#Stream that reaplies to given keywords

	except tweepy.TweepError as e:
		set_status(parse_error(e.reason), "ERROR")


start_bot()