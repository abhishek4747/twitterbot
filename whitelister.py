from twitterbot import *


if __name__=="__main__":
	
	user_list = get_credentials(CREDENTIALS_FILE)
	b = Bot(user_list[0])
	b.printLog = lambda x: [print(x),logToFile("logs/%s.log" % (__file__.split('.')[0]), x)]

	b.printLog ("\n\n################# %s ########################" % __file__)  
	b.printLog ("Linear Bot (%s) starting at %s" % (b.user_cred.BOT_NAME, str(datetime.now())))
	try:
		if b.login():
			# Do something
			# b.printLog("Do something!!")
			open(("cache/%s" % WHITELIST_FILE), "w")
			b.printLog ("Whiltelist cleared")
			b.getFollowers(handle="abhishek4747",cacheFile="+"+WHITELIST_FILE)
			b.printLog ("Followers added")
			b.getFollowing(handle="abhishek4747",cacheFile="+"+WHITELIST_FILE)
			b.printLog ("Following added")
			b.whitelist = self.readFromCache(WHITELIST_FILE)	
			b.cacheIt(WHITELIST_FILE,b.whitelist, "whitelist") 
			b.printLog ("Whitelist refreshed")
	except Exception as e:
		b.printLog("Execption:")
		b.printLog(str(e))
		b.printLog("At %s" % ( str(datetime.now())))
		raise e
	b.printLog("Linear Bot (%s) Exited at %s" % (b.user_cred.BOT_NAME, str(datetime.now())))
