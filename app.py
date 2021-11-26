import os
import hashlib
import traceback
from flask import Flask, request
import tweepy

flask_app = Flask(__name__)

KEYS = os.getenv("CUSTOMCONNSTR_TWITTER_KEYS")
CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = KEYS.split(";")
AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tweepy_api = tweepy.API(AUTH)

@flask_app.route("/")
def hello():
	try:
		return "Hello, World!"

	except Exception as e:
		return "Exception:" + str(traceback.format_exc()), 500

@flask_app.route("/tweet", methods=["POST"])
def tweet():
	print(request.form)
	if not request.form.get("key") or not request.form.get("body"):
		return "irregal access", 400
	if request.form["key"] != hashlib.sha256(str(KEYS).encode('utf-8')).hexdigest():
		return "irregal access", 400
	tweepy_api.update_status(request.form["body"])
	return "tweeted"

if __name__ == "__main__":
	flask_app.run(debug = True)
