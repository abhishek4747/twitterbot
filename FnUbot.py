from twitterbot import *


if __name__=="__main__":
	
	user_list = get_credentials(CREDENTIALS_FILE)
	b = Bot(user_list[0])
	b.printLog = lambda x: [print(x),logToFile("logs/%s.log"%(__file__.split('.')[0]), x)]

	b.printLog ("\n\n#################### %s ########################" % __file__)  
	b.printLog ("Loop Bot Template (%s) starting at %s" % (b.user_cred.BOT_NAME, str(datetime.now())))
	login_count = 0
	login_failed= 0
	while True:
		try:
			while b.login():
				login_count += 1
				b.printLog ("Login successful count: %d " % login_count)
				try:
					# Read toFollow
					b.toFollow = b.readFromCache(TOFOLLOW_FILE)
					
					# Follow one from toFollow
					if len(b.toFollow)>0:
						try:
							b.follow(user=b.toFollow.pop())
						except Exception as e:
							b.printLog ("Error in follow: %s" % str(e))
					else:
						b.printLog ("No one to follow")

					b.cacheIt(TOFOLLOW_FILE, b.toFollow," to follow")
					
					# Read toUnfollow
					b.toUnfollow = b.readFromCache(TOUNFOLLOW_FILE)

					# Unfollow one from toUnfollow
					if len(b.toUnfollow)>0:
						b.unfollow(user=b.toUnfollow.pop())
					else:
						b.printLog ("No one to unfollow")

					b.cacheIt(TOUNFOLLOW_FILE, b.toUnfollow," to unfollow")
				except Exception as e:
					b.printLog ("Error in while loop: %s" % str(e))
					#raise e

				b.printLog ("While loop sleeping for 60 secs\n")
				time.sleep(60)
		except Exception as e:
			login_failed += 1
			b.printLog ("Login Failed count: %d " % login_failed)
			#raise e
		
		b.printLog ("Outer loop sleeping for 60 secs\n")
		time.sleep(60)

