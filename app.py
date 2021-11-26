import os
import traceback
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
	# return "Hello, World!"
	try:
		content = ""
		access_token = os.getenv("CUSTOMCONNSTR_TWITTER_ACCESS_TOKEN")
		consumer_key, consumer_secret = access_token.split(";")
		content += "key: " + consumer_key[:5] + "***, secret: ***"
		return content

	except Exception as e:
		return "Exception:" + str(traceback.format_exc()), 500

if __name__ == "__main__":
	app.run(debug = True)
