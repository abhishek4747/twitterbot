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
