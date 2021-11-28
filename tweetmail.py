from tweet import tweet, delete_all_tweets, get_latest_tweet_text

def update_mail_notice(body, should_update):
	HASHTAG = "#mirua_mail #牧師録"
	USER_ID = "tsukasa_mirua"

	if not should_update:
		latest_text = get_latest_tweet_text(HASHTAG, USER_ID)
		if not latest_text:
			# 前にツイートがないならツイートだけ
			print("No tweet with hashtag " + HASHTAG + " were found")
			tweet(body + "\n" + HASHTAG)
			return True

		if latest_text == body + "\n" + HASHTAG:
			# 直近のツイートと変わらないならなにもせずreturn
			print("The status is not changed")
			return True

		# どちらでもない(前のツイートと内容が変わっている)なら下に合流

	# これまでのツイートを消して新しくツイート
	delete_all_tweets(HASHTAG, USER_ID)
	tweet(body + "\n" +HASHTAG)

	return True
