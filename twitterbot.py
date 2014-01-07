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

1. Read globals from file: credentials.txt as array of users
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

BOT = True

if BOT:
	OAUTH_TOKEN     = "2267641183-MXOegYKXPJOB429UzyeYnDMXMwtff6KjWkj8BB3"
	OAUTH_SECRET    = "ztkd3VzDftt2mpKONCd7cNOGgeYLB5XFwh6knj8r9cDIJ"
	CONSUMER_KEY    = "rWGVHoCIca5sLh9aRN2ZA"
	CONSUMER_SECRET = "ygX2aJVZHCY00vOnQSZ9HkA1hUczSNf80sCQr4Z0DWU"

	TWITTER_HANDLE  = "ak47_thelegend"
	TWITTER_PASSWORD= "twitteriscool"

else:
	OAUTH_TOKEN     = "970751431-IX2SzkAQsAzsXV0Orh7GAfhtu01mlMEUIfAfkQRv"
	OAUTH_SECRET    = "K2412DLIaX4rUulQgt4i7zQzTeKaPYGKqlv2gRadMAFhx"
	CONSUMER_KEY    = "NveQ1ByeXWDSgKfqJrCng"
	CONSUMER_SECRET = "7E8XiYpgKrdyy9j2GGgvvPoYNhFckPndNlY4Lb4"

	TWITTER_HANDLE  = "abhishek4747"
	TWITTER_PASSWORD= "twitteriscool"

CREDENTIALS_FILE = "credentials.txt"

# t = Api(username=TWITTER_HANDLE,password=TWITTER_PASSWORD)
# api = t


################################ CLASSES ######################################
class credential(object):
	"""docstring for credential"""
	def __init__(self, OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET, TWITTER_HANDLE, TWITTER_PASSWORD):
		self.OAUTH_TOKEN     = OAUTH_TOKEN     
		self.OAUTH_SECRET    = OAUTH_SECRET    
		self.CONSUMER_KEY    = CONSUMER_KEY    
		self.CONSUMER_SECRET = CONSUMER_SECRET 
		self.TWITTER_HANDLE  = TWITTER_HANDLE  
		self.TWITTER_PASSWORD= TWITTER_PASSWORD
		
		
	def __repr__(self):
		return "\n[%s, %s, %s, %s, %s, %s]"%(self.OAUTH_TOKEN, self.OAUTH_SECRET, self.CONSUMER_KEY, self.CONSUMER_SECRET, self.TWITTER_HANDLE, self.TWITTER_PASSWORD)

############################# FUNCTIONS #######################################
# TODO: get credentials from file 
def get_credentials(filename):
	lines = [s for s in map(lambda x:x.strip(),open(filename).readlines())]
	users = []
	for i in range(int((len(lines)+1)/7)):
		users.append(credential(lines[i*7+0],lines[i*7+1],lines[i*7+2],lines[i*7+3],lines[i*7+4],lines[i*7+5]))
	return users

# TODO: login using credentials
# def login():
# 	try:
# 		return Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,CONSUMER_KEY, CONSUMER_SECRET))
# 	except Exception as e:
# 		return None

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
	users_list = get_credentials("credentials.txt")
	print(users_list)
	pass
	# t = login()
	# if not t:
	# 	sys.exit(0)
	# else:
	# 	print("%s bot logged in successfully" % TWITTER_HANDLE)


