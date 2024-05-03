'''
	This script is going to access the recent tweets on home timeline
	and then favourite them, retweet them and put a random reply on them.
	It will perform this act every 30 minutes
'''

import tweepy, json, time
from threading import Thread
import random
from tweepy import *

def create_tweeter_api():

	with open('credentials.json','r') as f:
		data = json.load(f)

	consumer_key = data['consumer_key']
	consumer_secret = data['consumer_secret']

	access_secret = data['access_secret']
	access_token = data['access_token']

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)

	#tweet_api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify=True)
	tweet_api = tweepy.API(auth, wait_on_rate_limit = True)
	return tweet_api

tweet_api = create_tweeter_api()

def like_and_retweet(t):

	try:
		tweet_api.create_favorite(t.id)
		print("Liked the tweet with id:", t.id, " sent by ", t.user.name)
	except tweepy.error.TweepError:
		print("This tweet has already been liked.")

	try:
		tweet_api.retweet(t.id)
		print("Retweeted the tweet with id:", t.id," sent by ", t.user.name)
	except tweepy.error.TweepError:
		print("already retweed.")


def get_msg_to_reply():

	data = []
	with open("shakespeare.txt",'r') as f:
		data =f.readlines()

	s=''
	s = s.join(d for d in data)
	st_pos = random.randint(0,len(s))
	try:
		m = s[st_pos: st_pos + 280]
	except:
		m = s[st_pos: len(s)]
	print(m)	
	return m

#m = get_msg_to_reply()

def send_reply(to_tweet, m):

	if to_tweet.user.name != "dhiraj maheswari":
		try:
			media = tweet_api.media_upload("four-charges0.png")
			#tweet_api.update_status(status="this is puzzle", media_ids = [media.media_id_string])
			tweet_reply = tweet_api.update_status(status = m, in_reply_to_status_id = to_tweet.id, 
				auto_populate_reply_metadata = True, media_ids=[media.media_id_string])
			print("Replying to --", to_tweet.user.name)
			like_and_retweet(to_tweet)
#			time.sleep(10)
		
		except tweepy.error.TweepError as e:
			print("---Error tweeting---", e)



def main():

	q = 0
	while True:
		m = get_msg_to_reply()
		print("Run number: ",q)
		tweets = tweet_api.home_timeline(include_rts=True, include_entities=True)
		th = [Thread(target=send_reply, args=(tweet,m,)) for tweet in tweets]
		for t in th:
			t.start()
		q = q + 1
		time.sleep(1800) # sleep 30 minutes

if __name__ == "__main__":
	main()
