import urllib
import json
from tweet import update_notice

def get_day_str(datetime):
	pass

def get_weekly_schedule_str(src_json):
	src = json.loads(src_json)
	ans = ""
	for date in src:
		for schedule in src[date]:
			print(date, schedule["title"])

def update_schedule_notice(body, should_update):
	HASHTAG = "#mirua_schedule #牧師録"
	USER_ID = "tsukasa_mirua"
	# body = urllib.parse.unquote(body, "utf-8")
	# print(body)
	# get_weekly_schedule_str(body)
	# return body, 200
	return update_notice(body, HASHTAG, USER_ID, should_update)
