from twitterbot import *

if __name__ == "__main__":

	users_list = get_credentials(CREDENTIALS_FILE)

	b = Bot(users_list[0]) #Bot no. 0 for F4F

	if b.login():
		print ("Logged in")
		b.followers = b.readFromCache(FOLLOWER_FILE)

		b.followees = b.readFromCache(FOLLOWEE_FILE)

		b.cacheToUnfollow()

		b.unfollowAll()
'''
Bot How To:
Multiple bots.

GenerateWhitelist: [300,300 5 hours to write file.. so once a day or in a while]
    Get abhishek4747 followers: parallel
    Get abhishek4747 followees: parallel
    Read from manualWhitelist.txt

Follow_comp: [Once in a lifetime]
    Cache followers:[Daily] :parallel
    Cache followings:[Daily]:parallel
    Read Whitelist
    Cache toFollow:[FollowBack]
    Cache toUnfollow:[Didn't follow back]
    RefreshWhitelist


FnU:
    Follow one from toFollow
    save in follow_db
    Unfollow one from toUnfollow
    Remove from follow_db




'''

if __name__ == "__main__" and False:
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


