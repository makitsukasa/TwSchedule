import datetime
import traceback
from flask import Flask, request
from flaskasync import flask_async, flask_async_log
from tweet import tweet, check_key
from tweet2nd import tweet as tweet_2nd, check_key as check_key_2nd
from tweetmail import update_mail_notice
from tweetschedule import update_schedule_notice

app = Flask(__name__)

@app.route("/")
def app_route_index():
	try:
		return "Hello, World!"
	except Exception as e:
		return "Exception:" + str(traceback.format_exc()), 500

@app.route("/tweet", methods=["POST"])
def app_route_tweet():
	if not check_key_2nd():
		return "/tweet irregal access", 400
	if not tweet_2nd():
		return "/tweet server error", 500
	return "/tweet post succeeded"

@app.route("/mail", methods=["POST"])
@flask_async
def app_route_update_mail_notice():
	if not check_key():
		return "/mail irregal access", 400
	body = request.form.get("body")
	if not body:
		return "/mail irregal access", 400
	force_update = True if request.form.get("force_update") == "true" else False

	if not update_mail_notice(body, force_update):
		return "/mail server error", 500
	return "/mail post succeeded"

@app.route("/schedule", methods=["POST"])
@flask_async
def app_route_update_schedule_notice():
	if not check_key():
		return "/schedule irregal access", 400
	body = request.form.get("body")
	if not body:
		return "/schedule irregal access", 400
	force_update = True if request.form.get("force_update") == "true" else False

	if not update_schedule_notice(body, force_update):
		return "/schedule server error", 500
	return "/schedule post succeeded"

@app.route("/log", methods=["GET"])
def app_route_log():
	return flask_async_log()

@app.route("/log/<task_id>", methods=["GET"])
def app_route_log_by_id(task_id):
	return flask_async_log(task_id)

@app.route("/receivepost", methods=["POST"])
def app_route_receivepost():
	return request.get_data()

if __name__ == "__main__":
	app.run(debug = True)
