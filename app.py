import os
import traceback
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
	# return "Hello, World!"
	try:
		content = ""
		connection_string = os.getenv("CUSTOMCONNSTR_TWITTER_ACCESS_TOKEN")
		content += "key: " + retrieved_config_setting.key + ", secret: ***"
		return content

	except Exception as e:
		return "Exception:" + str(traceback.format_exc()), 500

if __name__ == "__main__":
	app.run(debug = True)
