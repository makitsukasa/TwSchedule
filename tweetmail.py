from tweet import tweet, delete_previous_tweet, search_latest_tweet

def update_mail_notice(body, should_update):
	HASHTAG = "#mirua_mail #牧師録"
	USER_ID = "tsukasa_mirua"
	latest = search_latest_tweet(HASHTAG, USER_ID)
	if not latest:
		return False

	delete_previous_tweet(HASHTAG, USER_ID)
	return True
