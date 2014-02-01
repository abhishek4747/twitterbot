''' APPENDIX: Extra knowledge '''

''' TODO: Make it intactive help '''


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


