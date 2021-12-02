import urllib
import datetime
import json
from tweet import update_notice

def update_schedule_notice(body, should_update):
	HASHTAG = "#mirua_schedule #牧師録"
	USER_ID = "tsukasa_mirua"
	return update_notice(body, HASHTAG, USER_ID, should_update)

def format_day_str(date_str):
	dt = datetime.datetime.strptime(date_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
	day = str(dt.day).zfill(2)
	day_of_week = ["月", "火", "水", "木", "金", "土", "日"][dt.date().weekday()]
	return day + day_of_week;

def format(json):
	ans = ""
	for date in json:
		ans += format_day_str(date)
		if not json[date]:
			ans += " - \n"
			continue
		first_title_flag = True
		for schedule in json[date]:
			if len(schedule["visible"]) > 0:
				continue
			if first_title_flag:
				ans += " "
			else:
				ans += "     "
			ans += schedule["title"] + "\n"
			first_title_flag = False
	return ans[:-1]

def update_schedule_notice_(schedules, should_update):
	HASHTAG = "#mirua_schedule #牧師録"
	USER_ID = "tsukasa_mirua"
	body = format(json.loads(schedules))
	return update_notice(body, HASHTAG, USER_ID, should_update)

if __name__ == "__main__":
	update_schedule_notice('{"2021-11-30":[{"title":"1430+面談+liveon","visible":{}},{"title":"鳴尾","visible":{}},{"title":"年末調整が今年だけは違う","visible":{}}],"2021-12-01":[{"title":"鳴尾","visible":{}}],"2021-12-02":[{"title":"�","visible":{}},{"title":"鳴尾","visible":{}}],"2021-12-03":[],"2021-12-04":[],"2021-12-05":[{"title":"850","visible":{}}],"2021-12-06":[{"title":"休","visible":{}}],"2021-12-07":[{"title":"830","visible":{}}]}', "#mirua_schedule #牧師録")

