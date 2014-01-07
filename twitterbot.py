###############################################################################
# Twitter Bot: By Abhishek Kumar
# Bot name : The Legend
###############################################################################

''' AIM

Bot to have at least 1 lac followers.
	Whitelist.txt: People who abhishek4747 follow 
		& abhishek4747's followers follow
	ToFollow.txt: 
		People on my TL 
		& Followers of Whitelist.txt
	Unfollowed.txt:
		Recently unfollowed people and date.
	Blocked.txt:
		Don't follow these people [Manual]
	Strategy:   
		Followback Immediately. If it passes the eligiblity criteria.
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
	Update Whitelist.txt
	Follow one random person from ToFollow.txt but not in Unfollowed.txt
	Unfollow people if they don't follow back even after 1 week.
	Unfollow unfollowers if they are not in Whitelist.txt.
	Update and clear entries from Unfollowed.txt which are 1 month old.
	AutoFollowBack new Followers
	Read TL and Update ToFollow.txt not in Unfollowed.txt
	Tweet()
	TweetCurrent()
	RetweetAbhishek4747()
	Sleep(90 secs)

'''


########################### INCLUDED LIBS #####################################

import time, sys
from twitter import Twitter, OAuth, TwitterHTTPError

########################## GLOBAL CONSTANTS ###################################

CREDENTIALS_FILE = "credentials.txt"
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

WHITELIST_FILE = "whitelist.txt"

# t = Api(username=TWITTER_HANDLE,password=TWITTER_PASSWORD)
# api = t


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

	def login(self):
		try:
			self.api = Twitter(auth=OAuth(self.user_cred.OAUTH_TOKEN, self.user_cred.OAUTH_SECRET, self.user_cred.CONSUMER_KEY, self.user_cred.CONSUMER_SECRET))
			self.t = self.api
			return self.api
		except Exception as e:
			print (e)
			return None

	def getFollowers(self,handle):
		return [(user['id_str'], cleanStr(user['name']), user['screen_name']) for user in self.api.friends.list(screen_name=handle)["users"]]

	def updateWhitelist(self):
		# self.whitelist = [line for line in readFile(WHITELIST_FILE) if line!=""] # This is manual, too easy
		self.whitelist = self.getFollowers(self.user_cred.TWITTER_HANDLE)
		f = open(WHITELIST_FILE,"w")
		for user in self.whitelist:
			f.write("%s\t%s\t%s\n"%(user[0],user[1],user[2]))
		f.close()
		print("Whitelist.txt updated.")
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
			Update Whitelist.txt
			Follow one random person from ToFollow.txt but not in Unfollowed.txt
			Unfollow people if they don't follow back even after 1 week.
			Unfollow unfollowers if they are not in Whitelist.txt.
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

# TODO: 
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
	# print(users_list)

	b = Bot(users_list[1])
	login_count = 0
	while b.login():
		print("Login count: %d" % login_count)
		login_count += 1
		while True:
			b.refresh()
			print("Refreshing in 90 secs..")
			time.sleep(90)
	print("Couldn't Login!! Aborting")
