from tweet import update_notice

def update_schedule_notice(body, should_update):
	HASHTAG = "#mirua_schedule #牧師録"
	USER_ID = "tsukasa_mirua"
	return update_notice(body, HASHTAG, USER_ID, should_update)
