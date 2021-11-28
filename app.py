from time import sleep
import traceback
from flask import Flask
from tweet import tweet, delete_previous_tweet
from flaskasync import flask_async, flask_async_tasks

app = Flask(__name__)

@app.route("/")
def app_route_index():
	try:
		return "Hello, World!"

	except Exception as e:
		return "Exception:" + str(traceback.format_exc()), 500

@app.route("/tweet", methods=["POST"])
@flask_async
def app_route_tweet():
	status = tweet()
	if status:
		return "tweeted"
	else:
		return "irregal access", 400

@app.route("/update", methods=["POST"])
@flask_async
def app_route_update():
	delete_previous_tweet()

if __name__ == "__main__":
	app.run(debug = True)
