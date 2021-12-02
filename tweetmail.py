from tweet import update_notice

def update_mail_notice(unread_count, should_update):
	HASHTAG = "#mirua_mail #牧師録"
	USER_ID = "tsukasa_mirua"
	if unread_count == "0":
		body = "未読のメールはありません"
	else:
		body = f"@tsukasa_metam 未読のメールが{unread_count}件あります"
	return update_notice(body, HASHTAG, USER_ID, should_update)
