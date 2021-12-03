import datetime
import traceback
from flask import Flask, request
from flaskasync import flask_async, flask_async_result
from tweet import tweet, check_key
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
@flask_async
def app_route_tweet():
	if not check_key():
		return "irregal access", 400
	if not tweet():
		return "server error", 500
	return "tweeted"

@app.route("/mail", methods=["POST"])
@flask_async
def app_route_update_mail_notice():
	if not check_key():
		return "irregal access", 400
	body = request.form.get("body")
	if not body:
		return "irregal access", 400
	force_update = True if request.form.get("force_update") == "true" else False

	if not update_mail_notice(body, force_update):
		return "server error", 500
	dt = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
	return dt + " /mail post succeeded", 200

@app.route("/schedule", methods=["POST"])
@flask_async
def app_route_update_schedule_notice():
	if not check_key():
		return "irregal access", 400
	body = request.form.get("body")
	if not body:
		return "irregal access", 400
	force_update = True if request.form.get("force_update") == "true" else False

	if not update_schedule_notice(body, force_update):
		return "server error", 500
	dt = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
	return dt + " /schedule post succeeded", 200

@app.route("/result", methods=["GET"])
def app_route_result():
	return flask_async_result()

@app.route("/result/<task_id>", methods=["GET"])
def app_route_result_by_id(task_id):
	return flask_async_result(task_id)

@app.route("/receivepost", methods=["POST"])
@flask_async
def app_route_receivepost():
	return request.get_data()

if __name__ == "__main__":
	app.run(debug = True)
