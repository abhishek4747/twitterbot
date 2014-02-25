from twitterbot import *


if __name__=="__main__":
	
	user_list = get_credentials(CREDENTIALS_FILE)
	b = Bot(user_list[0])
	b.printLog = lambda x: [print(x),logToFile("logs/%s.log" % (__file__.split('.')[0]), x)]

	b.printLog ("\n\n################# %s ########################" % __file__)  
	b.printLog ("Linear Bot (%s) starting at %s" % (b.user_cred.BOT_NAME, str(datetime.now())))
	try:
		if b.login():
			b.printLog("Login successful. ")
			b.getFollowers()
	except Exception as e:
		b.printLog("Execption:")
		b.printLog(str(e))
	b.printLog("Linear Bot (%s) Exited at %s" % (b.user_cred.BOT_NAME, str(datetime.now())))

