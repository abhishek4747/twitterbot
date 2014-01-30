###############################################################################
# Twitter Bot: By Abhishek Kumar
# User name : The Legend
# Bot : Twitter Bot Class
###############################################################################

'''
myFollowers.txt  -> my followers [who follow me]	-> Automatic
myFollowees.txt  -> my followees [whom I follow]	-> Automatic
whitelist.tsv 	 -> people not to be unfollowed 		-> Manual for now
toFollow.txt 	 -> people to be followed 			-> Automatic
followed.txt 	 -> people who i followed and when 	-> Automatic
toUnfollow.txt 	 -> to unfollow 						-> Manual
blocked.txt 	 -> don't follow these people			-> Manual
credentials.txt	 -> save credentials of different bot 	-> Manual
logs 			 -> logs of bot 					-> Automatic
tweets.txt 		 -> tweets with separator $^$^$ 	-> Automatic
hottweets.txt    -> hot tweets with separator $^$^$ -> Automatic

'''

'''
This File will have only class. Implementation on other file.
Enable Logging. Save in file as well as in memory.

'''


''' AIM
Bot to have at least 1 lac followers.
	Strategy:   
		Followback If eligible.
		Follow 40 people per hour. Try following only Indians.
			Follow a person every 90 second.
		Unfollow other people if
			They don't follow back even after 1 week.
			They speak other language than english or hindi.
		Unfollow people if they don't follow back even after 1 week.
		Unfollow unfollowers
		Do not unfollow whitelisted people.
Post tweets from a file on regular interval. [Automatic]
Add a hot topic tweet file. [Adding Manual, Tweeting Automatic]
Retweet abhishek4747's tweet to get favs and RTs [Manual]
Generate Notifications for me to check. [Automatic]
'''

''' Commit

1. [Done] Read globals from file: credentials.txt as array of users
2. Create the white list
3. Autofollow back
4. Create ToFollow.txt
5. Create NotFollowingback.txt with follow date
6. 

'''

''' Execution
Refresh():
	Error logging 
	Update whitelist.tsv [Manual or write another bot]
	Follow one random person from ToFollow.txt but not in Unfollowed.txt 
	Unfollow people if they don't follow back even after 1 week.
	Unfollow unfollowers if they are not in whitelist.tsv.
	Update and clear entries from Unfollowed.txt which are 1 month old. [Later]
	AutoFollowBack new Followers [Manual]
	Read TL and Update ToFollow.txt not in Unfollowed.txt [Later]
	Tweet() [Later]
	TweetCurrent() [Later]
	RetweetAbhishek4747() [Manual]
	Sleep(90 secs)

'''
''' Limitations
15 requests per 15 minute per type
60 sec -> Ek follow 
1000 min -> 1000 follow 
440 min -> 440 requests
	5 requests -> get followers 
	1 request -> follow back check
	x10

	5 requests -> last_followed
	1 request -> follow back check
	x1

New plan per hour 60 requests:
	5 requests -> getFollowers
	1 requests -> follow back check
	next n follows
	5 requests -> last_followed
	1 request -> follow back check
	unfollow people

'''


########################### INCLUDED LIBS #####################################

import time, sys
from twitter import Twitter, OAuth, TwitterHTTPError

########################## GLOBAL CONSTANTS ###################################

CREDENTIALS_FILE = "credentials.txt"
FOLLOWER_FILE = "myFollowers.txt"
FOLLOWEE_FILE = "myFollowees.txt"
TOUNFOLLOW_FILE = "toUnfollow.txt"

WHITELIST_FILE = "whitelist.tsv"

FOLLOWER_BANK = ["mojokajojo","KrishnaAthal"]

################################ CLASSES ######################################
class Credential:
	"""docstring for Credential"""
	def __init__(self, OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET, TWITTER_HANDLE, TWITTER_PASSWORD):
		self.OAUTH_TOKEN     = OAUTH_TOKEN     
		self.OAUTH_SECRET    = OAUTH_SECRET    
		self.CONSUMER_KEY    = CONSUMER_KEY    
		self.CONSUMER_SECRET = CONSUMER_SECRET 
		self.TWITTER_HANDLE  = TWITTER_HANDLE  
		self.TWITTER_PASSWORD= TWITTER_PASSWORD
		
		
	def __repr__(self):
		return "\n[%s, %s, %s, %s, %s, %s]"%(self.OAUTH_TOKEN, self.OAUTH_SECRET, self.CONSUMER_KEY, self.CONSUMER_SECRET, self.TWITTER_HANDLE, self.TWITTER_PASSWORD)

class Bot:
	"""docstring for Bot"""
	def __init__(self, user_cred):
		self.user_cred = user_cred
		self.api = None
		self.t = self.api
		self.whitelist = None
		self.toUnfollow = None
		self.followers = None
		self.followees = None
		self.followersCached = True
		self.followeesCached = True

	def login(self):
		try:
			self.api = Twitter(auth=OAuth(self.user_cred.OAUTH_TOKEN, self.user_cred.OAUTH_SECRET, self.user_cred.CONSUMER_KEY, self.user_cred.CONSUMER_SECRET))
			self.t = self.api
			return self.api
		except Exception as e:
			print (e)
			return None

	def getFollowers(self,handle=None):
		if self.followersCached and self.followers!=None:
			# print(self.followers)
			return self.followers
		else:
			if handle==None:
				handle = self.user_cred.TWITTER_HANDLE
			self.followers = []
			next = None
			while True:
				if not next:
					followers_list = self.api.followers.list(screen_name=handle)
				else:
					followers_list = self.api.followers.list(screen_name=handle, cursor=next)
				new_followers = [(user['id_str'], user['screen_name'], cleanStr(user['name'])) for user in followers_list["users"]]
				self.followers += new_followers
				print ("fetched followers count: %d" % len(new_followers))
				if followers_list['next_cursor']==0:
					break
				next = followers_list['next_cursor']
				self.cacheFollowers()
				time.sleep(60)
			return self.followers

	def getFollowing(self,handle=None):
		if self.followeesCached and self.followees!=None:
			# print(self.followees)
			return self.followees
		else:
			if handle==None:
				handle = self.user_cred.TWITTER_HANDLE
			self.followees = []
			next = None
			while True:
				if not next:
					following_list = self.api.friends.list(screen_name=handle)
				else:
					following_list = self.api.friends.list(screen_name=handle, cursor=next)
				new_friends = [(user['id_str'], user['screen_name'], cleanStr(user['name'])) for user in following_list["users"]]
				self.followees += new_friends
				print ("fetched friends count: %d" % len(new_friends))
				if following_list['next_cursor']==0:
					break
				next = following_list['next_cursor']
				self.cacheFollowees()
				time.sleep(60)
			return self.followees


	def cacheToUnfollow(self):
		followers = set(list(map(lambda x: x[0],self.getFollowers())))
		following = set(list(map(lambda x: x[0],self.getFollowing())))
		self.toUnfollow = list(following - followers)
		b.cacheIt(TOUNFOLLOW_FILE, self.toUnfollow, "toUnfollow")

	def cacheFollowers(self):
		f = open(FOLLOWER_FILE,"w")
		for follower in self.followers:
			f.write("%s\t%s\t%s\n"%(follower[0],follower[1],follower[2]))
		f.close()
		print("%d followers cached" % len(self.followers))

	def cacheFollowees(self):
		f = open(FOLLOWEE_FILE,"w")
		for followee in self.followees:
			f.write("%s\t%s\t%s\n"%(followee[0],followee[1],followee[2]))
		f.close()
		print("%d followees cached" % len(self.followees))

	def cacheIt(self, filename, variable, name):
		f = open(filename,"w")
		for var in variable:
			if type(var) is list:
				f.write('\t'.join(var)+"\n")
			else:
				f.write(str(var)+"\n")
		f.close()
		print("%d %s cached" % (len(variable), str(name) ))

	def readFromCache(self, filename):
		l = open(str(filename)).readlines()
		c = []
		for line in l:
			c.append(line.split('\t'))
		print("%d read from %s cached" % (len(l), str(filename) ))
		return c


	def unfollow(self,handle=None, userid=None):
		if handle==None and userid==None:
			return
		if userid!=None:
			self.api.friendships.destroy(user_id=userid)
			print("Unfollowed: %s"%str(userid))
		else:
			self.api.friendships.destroy(screen_name=handle)
			print("Unfollowed: %s"%str(handle))

	def unfollowAll(self):
		print("Now Unfollowing: %d people"%len(self.toUnfollow))
		for user in self.toUnfollow:
			if type(user) is list:
				self.unfollow(userid=user[0])
			else:
				self.unfollow(userid=user)
			time.sleep(60)

	def updateWhitelist(self):
		# self.whitelist = [line for line in readFile(WHITELIST_FILE) if line!=""] # This is manual, too easy
		self.whitelist = self.getFollowers(self.user_cred.TWITTER_HANDLE)
		f = open(WHITELIST_FILE,"w")
		for user in self.whitelist:
			f.write("%s\t%s\t%s\n"%(user[0],user[1],user[2]))
		f.close()
		print(len(self.whitelist))
		print("whitelist.tsv updated.")
		return self.whitelist

	def followRandom(self):
		pass

	def unfollowPeople(self):
		pass

	def updateUnfollowed(self):
		pass

	def autoFollowBack(self):
		pass

	def updateToFollow(self):
		pass

	def tweetScheduled(self):
		pass

	def tweetCurrent(self):
		pass

	def retweetAbhishek4747(self):
		pass

	def refresh(self):
		""" Execution Refresh():
			Update whitelist.tsv
			Follow one random person from ToFollow.txt but not in Unfollowed.txt
			Unfollow people if they don't follow back even after 1 week.
			Unfollow unfollowers if they are not in whitelist.tsv.
			Update and clear entries from Unfollowed.txt which are 1 month old.
			AutoFollowBack new Followers
			Read TL and Update ToFollow.txt not in Unfollowed.txt
			Tweet()
			TweetCurrent()
			RetweetAbhishek4747()
			Sleep(90 secs)

		"""
		self.updateWhitelist()
		self.followRandom()
		self.unfollowPeople()
		self.updateUnfollowed()
		self.autoFollowBack()
		self.updateToFollow()
		self.tweetScheduled()
		self.tweetCurrent()
		self.retweetAbhishek4747()
		pass

	def stats(self):
		pass

	def logToFile(self,s):
		open('logs','a',encoding='utf-8').write(s)


############################# FUNCTIONS #######################################
def cleanStr(string):
	return str(string.encode('ascii', 'ignore')) #ignore, replace, xmlcharrefreplace

def readFile(filename):
	return [s for s in map(lambda x:x.strip(),open(filename).readlines())]

def get_credentials(filename):
	lines = readFile(filename)
	users = []
	for i in range(int((len(lines)+1)/7)):
		users.append(Credential(lines[i*7+0],lines[i*7+1],lines[i*7+2],lines[i*7+3],lines[i*7+4],lines[i*7+5]))
	return users

#	# TODO: 
	# def auto_follow(q, count=100, result_type="recent"):
	# 	result = search_tweets(q, count, result_type)
	# 	following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
		
	# 	for tweet in result['statuses']:
	# 		try:
	# 			if tweet['user']['screen_name'] != TWITTER_HANDLE and tweet['user']['id'] not in following:
	# 				t.friendships.create(user_id=tweet['user']['id'], follow=True)
	# 				following.update(set([tweet['user']['id']]))
					
	# 				print ("followed " + tweet['user']['screen_name'])
					
	# 		except TwitterHTTPError as e:
	# 			print ("error: ", e)


	# tweets = t.statuses.home_timeline()

	# def search_tweets(q, count=100, result_type="recent"):
	# 	return t.search.tweets(q=q, result_type=result_type, count=count)

	# for i,tweet in enumerate(tweets):
	# 	print(i,str(tweet['text'].encode('ascii', 'xmlcharrefreplace'))) #ignore, replace, xmlcharrefreplace

	# def fav_tweet(tweet):
	# 	try:
	# 		result = t.favorites.create(_id=tweet['id'])
	# 		print ("Favorited: %s" % (result['text']))
	# 		return result
	# 	# when you have already favourited a tweet
	# 	# this error is thrown
	# 	except TwitterHTTPError as e:
	# 		print ("Error: ", e)
	# 		return None

	# def auto_fav(q, count=100, result_type="recent"):
	# 	result = search_tweets(q, count, result_type)
		
	# 	for tweet in result['statuses']:
	# 		try:
	# 			# don't favorite your own tweets
	# 			if tweet['user']['screen_name'] == TWITTER_HANDLE:
	# 				continue
				
	# 			result = t.favorites.create(_id=tweet['id'])
	# 			print ("favorited: %s" % (result['text']))
				
	# 		# when you have already favorited a tweet this error is thrown
	# 		except TwitterHTTPError as e:
	# 			print ("error: ", e)

	# def getFollowersOf(thisuser, thispage):
	# 	followerlist = api.GetFollowers(user=thisuser, page=str(thispage))

	# 	for x in followerlist:
	# 		print(x.screen_name)

	# 	time.sleep(30)


	# def auto_unfollow_nonfollowers():
	# 	following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
	# 	followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])
		
	# 	# put user IDs here that you want to keep following even if they don't follow you back
	# 	users_keep_following = set([])
		
	# 	not_following_back = following - followers
		
	# 	for userid in not_following_back:
	# 		if userid not in users_keep_following:
	# 			t.friendships.destroy(user_id=userid)

	# getFollowersOf(TWITTER_HANDLE,1)


if __name__ == "__main__":
	users_list = get_credentials(CREDENTIALS_FILE)
	
	b = Bot(users_list[0]) #Bot no. 0 for F4F

	# if b.login():
	# 	print ("Logged In")
	# 	b.cacheToUnfollow()
	# 	b.unfollowAll()

	if b.login():
		b.followers = b.readFromCache(FOLLOWER_FILE)
		b.followees = b.readFromCache(FOLLOWEE_FILE)
		b.cacheToUnfollow()
		b.unfollowAll()


	# login_count = 0
	# while b.login():
	# 	print("Login count: %d" % login_count)
	# 	login_count += 1
	# 	b.cacheToUnfollow()
	# 	while True:
	# 		b.unfollow()
	# 		#b.refresh()
	# 		print("Refreshing in 90 secs..")
	# 		time.sleep(90)
	# print("Couldn't Login!! Aborting")
















''' credentials.txt : looks like this; can have multiple users; 
OAUTH_TOKEN     
OAUTH_SECRET    
CONSUMER_KEY    
CONSUMER_SECRET 
TWITTER_HANDLE  
TWITTER_PASSWORD

OAUTH_TOKEN     
OAUTH_SECRET    
CONSUMER_KEY    
CONSUMER_SECRET 
TWITTER_HANDLE  
TWITTER_PASSWORD
'''
