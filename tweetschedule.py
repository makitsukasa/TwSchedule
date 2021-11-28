from tweet import tweet, delete_previous_tweet

def update_schedule_notice(body, should_update):
	HASHTAG = "#mirua_schedule #牧師録"
	USER_ID = "tsukasa_mirua"
	delete_previous_tweet(HASHTAG, USER_ID)
