import os
from flask import request
import hashlib
import tweepy

KEYS = os.getenv("CUSTOMCONNSTR_TWITTER_KEYS")
CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = KEYS.split(";")
AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tweepy_api = tweepy.API(AUTH)

def tweet():
	if not request.form.get("key") or not request.form.get("body"):
		return False
	if request.form["key"] != hashlib.sha256(str(KEYS).encode('utf-8')).hexdigest():
		return False
	tweepy_api.update_status(request.form["body"])
	return True
