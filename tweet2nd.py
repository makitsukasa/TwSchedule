import os
from flask import request
import hashlib
import tweepy

KEYS = os.getenv("CUSTOMCONNSTR_TWITTER_KEYS_2ND")
CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = KEYS.split(";")
AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tweepy_api_2nd = tweepy.API(AUTH)

def check_key():
	if not request.form.get("key"):
		return False
	if request.form["key"] != hashlib.sha256(str(KEYS).encode("utf-8")).hexdigest():
		return False
	return True

def tweet(body = None):
	if not body:
		if not request.form.get("body"):
			return False
		body = request.form.get("body")
	tweepy_api_2nd.update_status(body)
	return True
