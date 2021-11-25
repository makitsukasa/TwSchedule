import os
from azure.appconfiguration import AzureAppConfigurationClient, ConfigurationSetting
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
	# return "Hello, World!"
	try:
		content = ""
		retrieved_config_setting = app_config_client.get_configuration_setting(key='test')
		content += "Retrieved configuration setting:<br>"
		content += "Key: " + retrieved_config_setting.key + ", Value: " + retrieved_config_setting.value
		return content
	except Exception as e:
		return "Exception:" + e
