import os
import traceback
from azure.appconfiguration import AzureAppConfigurationClient, ConfigurationSetting
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
	# return "Hello, World!"
	try:
		content = ""
		connection_string = os.getenv("CUSTOMCONNSTR_AZURE_APP_CONFIG_CONNECTION_STRING")
		app_config_client = AzureAppConfigurationClient.from_connection_string(connection_string)
		retrieved_config_setting = app_config_client.get_configuration_setting(key='test')
		content += "Retrieved configuration setting:<br>"
		content += "Key: " + retrieved_config_setting.key + ", Value: " + retrieved_config_setting.value
		return content

	except Exception as e:
		return "Exception:" + str(traceback.format_exc()), 500

if __name__ == "__main__":
	app.run(debug = True)
