from tweet import tweet, delete_all_tweets

def update_schedule_notice(body, should_update):
	HASHTAG = "#mirua_schedule #牧師録"
	USER_ID = "tsukasa_mirua"
	delete_all_tweets(HASHTAG, USER_ID)
