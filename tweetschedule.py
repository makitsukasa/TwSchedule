import urllib
import datetime
import json
from tweet import update_notice

def format_day_str(date_str):
	dt = datetime.datetime.strptime(date_str + " 00:00:00", "%Y-%m-%d %H:%M:%S")
	day = str(dt.day).zfill(2)
	day_of_week = ["月", "火", "水", "木", "金", "土", "日"][dt.date().weekday()]
	return day + day_of_week

def format(json):
	ans = ""
	for date in json:
		ans += format_day_str(date)
		if not json[date]:
			ans += " - \n"
			continue
		first_title_flag = True
		for schedule in json[date]:
			if first_title_flag:
				ans += " "
			else:
				ans += "         "
			ans += schedule["title"] + "\n"
			first_title_flag = False
		if first_title_flag:
			ans += " - \n"
	return ans[:-1]

def update_schedule_notice(schedules, should_update):
	HASHTAG = "#mirua_schedule #牧師録"
	USER_ID = "tsukasa_mirua"
	body = format(json.loads(schedules))
	return update_notice(body, HASHTAG, USER_ID, should_update)
