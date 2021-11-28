import os
from flask import request
import hashlib
import tweepy
from pprint import pprint

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

def tweet(body = None):
	if not body:
		if not request.form.get("body"):
			return False
		body = request.form.get("body")
	tweepy_api.update_status(body)
	return True

def delete_all_tweets(hashtag, user_id):
	status = tweepy_api.search_tweets(
		q = hashtag + " from:" + user_id,
		result_type = "recent",
		tweet_mode = "extended")
	if len(status) <= 0:
		return False
	for s in status:
		tweepy_api.destroy_status(s.id)
	return True

def get_latest_tweet_text(hashtag, user_id):
	status = tweepy_api.search_tweets(q = hashtag + " from:" + user_id)
	if len(status) <= 0:
		print("No tweet with hashtag " + hashtag + " were found")
		return False
	return sorted(status, key = lambda i: i.created_at, reverse = True)[0].text
