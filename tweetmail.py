from tweet import update_notice

def update_mail_notice(body, should_update):
	HASHTAG = "#mirua_mail #牧師録"
	USER_ID = "tsukasa_mirua"
	update_notice(body, HASHTAG, USER_ID, should_update)
