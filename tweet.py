import os
from flask import request
import hashlib
import tweepy

KEYS = os.getenv("CUSTOMCONNSTR_TWITTER_KEYS")
CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = KEYS.split(";")
AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tweepy_api = tweepy.API(AUTH)

def check_key():
	if not request.form.get("key"):
		return False
	if request.form["key"] != hashlib.sha256(str(KEYS).encode('utf-8')).hexdigest():
		return False
	return True

def tweet():
	if not request.form.get("body"):
		return False
	tweepy_api.update_status(request.form["body"])
	return True

def delete_previous_tweet(hashtag, user_id):
	status = tweepy_api.search_tweets(q = hashtag + " from:" + user_id)
	if len(status) <= 0:
		print("prev tweet for " + hashtag + " is not found")
		return False
	for s in status:
		print(s.id_str)
	return True

def search_latest_tweet(hashtag, user_id):
	status = tweepy_api.search_tweets(q = hashtag + " from:" + user_id)
	if len(status) <= 0:
		print("prev tweet for " + hashtag + " is not found")
		return False
	for s in status:
		print(s.id_str)
	return True
