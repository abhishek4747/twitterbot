###############################################################################
# Twitter Bot: By Abhishek Kumar
# User name : The Legend
# Bot : Twitter Bot Class
###############################################################################

''' See help.py for more detailed documentation (Not Completed) '''

########################### INCLUDED LIBS #####################################

import time, sys
from datetime import datetime, timedelta
from twitter import Twitter, OAuth, TwitterHTTPError
#from help import help
# import os # to be used later to save pids of all the running bots

########################## GLOBAL CONSTANTS ###################################

CREDENTIALS_FILE    = "credentials.txt" 
# soon to replaced by tsv # change Credential constructor to list

FOLLOWER_FILE       = "myFollowers.tsv"
FOLLOWEE_FILE       = "myFollowing.tsv"

TOUNFOLLOW_FILE     = "toUnfollow.tsv"
TOFOLLOW_FILE       = "toFollow.tsv"
WHITELIST_FILE      = "whitelist.tsv"
MANWHITELIST_FILE   = "manwhitelist.tsv"
BLOCKLIST_FILE      = "blocklist.tsv"
FOLLOWEDDB_FILE     = "followedDB.tsv"

FOLLOWER_BANK_FILE  = "followerBank.tsv"

################################ CLASSES ######################################
class Credential:
    """docstring for Credential"""
    def __init__(self, OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, 
                CONSUMER_SECRET, TWITTER_HANDLE, TWITTER_PASSWORD=None, BOT_NAME=None):
        self.OAUTH_TOKEN     = OAUTH_TOKEN     
        self.OAUTH_SECRET    = OAUTH_SECRET    
        self.CONSUMER_KEY    = CONSUMER_KEY    
        self.CONSUMER_SECRET = CONSUMER_SECRET 
        self.TWITTER_HANDLE  = TWITTER_HANDLE  
        self.TWITTER_PASSWORD= TWITTER_PASSWORD
        self.BOT_NAME        = BOT_NAME
        
    def __repr__(self):
        return "\nCredential([%s, %s, %s, %s, %s, %s])"%(self.OAUTH_TOKEN, 
            self.OAUTH_SECRET, self.CONSUMER_KEY, self.CONSUMER_SECRET, 
            self.TWITTER_HANDLE, self.TWITTER_PASSWORD)

class Bot:
    """docstring for Bot"""
    def __init__(self, user_cred, login=None, printLog=None):
        self.user_cred = user_cred
        self.api = None
        if printLog:
            self.printLog = printLog
        else:
            self.printLog = lambda x: print (str(x))
        self.whitelist = self.readFromCache(WHITELIST_FILE)
        self.toUnfollow = self.readFromCache(TOUNFOLLOW_FILE)
        self.toFollow = self.readFromCache(TOFOLLOW_FILE)
        self.followers = self.readFromCache(FOLLOWER_FILE)
        self.following = self.readFromCache(FOLLOWEE_FILE)
        if login:
            self.login()

    def login(self):
        try:
            self.api = Twitter(auth=OAuth(self.user_cred.OAUTH_TOKEN, 
                self.user_cred.OAUTH_SECRET, self.user_cred.CONSUMER_KEY, 
                self.user_cred.CONSUMER_SECRET))
            return self.api
        except Exception as e:
            self.printLog (e)
            return None

    def getFollowers(self, handle=None, cacheFile=None):
        if handle==None:
            handle = self.user_cred.TWITTER_HANDLE
        if cacheFile==None and handle==self.user_cred.TWITTER_HANDLE:
            cacheFile = FOLLOWER_FILE
        
        followers = []
        next = None
        while True:
            if not next:
                followers_list = self.api.followers.list(screen_name=handle)
            else:
                try:
                    followers_list = self.api.followers.list(screen_name=handle, cursor=next)
                except Exception as e:
                    self.printLog ("****************************************\nException: %s" % str(e))
                    time.sleep(65*5)
                    continue
            new_followers = [(user['id_str'], user['screen_name'], 
                    cleanStr(user['name'])) for user in followers_list["users"]]
            followers += new_followers
            self.printLog ("%s's fetched followers count: %d" % (handle, len(followers)))
            next = followers_list['next_cursor']
            self.cacheIt(cacheFile, new_followers if cacheFile[0]=="+" else followers,"%s\'s followers" % handle)
            if followers_list['next_cursor']==0:
                break
            time.sleep(65)
        return set(followers)

    def getFollowing(self, handle=None, cacheFile=None):
        if handle==None:
            handle = self.user_cred.TWITTER_HANDLE
        if cacheFile==None and handle==self.user_cred.TWITTER_HANDLE:
            cacheFile = FOLLOWEE_FILE

        following = []
        next = None
        while True:
            if not next:
                following_list = self.api.friends.list(screen_name=handle)
            else:
                try:
                    following_list = self.api.friends.list(screen_name=handle, cursor=next)
                except Exception as e:
                    self.printLog ("****************************************\nException: %s" % str(e))
                    time.sleep(65*5)
                    continue
            new_friends = [(user['id_str'], user['screen_name'], 
                cleanStr(user['name'])) for user in following_list["users"]]
            following += new_friends
            self.printLog ("%s's fetched following count: %d" % (handle, len(following)))
            next = following_list['next_cursor']
            self.cacheIt(cacheFile, new_friends if cacheFile[0]=="+" else following, "%s\'s following" % handle)
            if following_list['next_cursor']==0:
                break
            time.sleep(65)
        return set(following)

    def cacheIt(self, filename, variable, name):
        if not filename:
            return
        if str(filename)[0]=="+":
            f = open("cache/"+str(filename[1:]),"a")
        else:
            f = open("cache/"+str(filename),"w")
        for var in variable:
            if type(var) is list or type(var) is tuple:
                f.write('\t'.join(var)+"\n")
            else:
                f.write(str(var)+"\n")
        f.close()
        self.printLog ("%d %s cached in %s" % (len(variable), str(name), str(filename) ))

    def readFromCache(self, filename):
        c = set()
        try:
            l = readFile("cache/"+filename)
            for line in l:
                c.add(tuple(line.split('\t')))
            self.printLog ("%d tuples read from %s cached" % (len(l), str(filename) ))
        except Exception as e:
            self.printLog ("Exception readFromCache(%s): %s" % (filename, str(e)))
        return c

    def follow(self, user=None, handle=None, userid=None, force=False):
        if user:
            self.api.friendships.create(user_id=user[0])
            self.following.add(user)
            self.cacheIt(FOLLOWEE_FILE, self.following, "%s following" % self.user_cred.TWITTER_HANDLE)
            self.printLog ("Followed id: %s \thandle: %s \tName: %s" % (str(user[0]), str(user[1]), str(user[2])))
            return
        if handle==None and userid==None:
            return
        if handle!=None:
            self.api.friendships.create(screen_name=handle)
            self.printLog ("followed handle: %s"%str(handle))
        else:
            self.api.friendships.create(user_id=userid)
            self.printLog ("followed userid: %s"%str(userid))

    def cacheToUnfollow(self):
        self.following = self.readFromCache(FOLLOWEE_FILE)
        self.followers = self.readFromCache(FOLLOWER_FILE)
        self.whitelist = self.readFromCache(WHITELIST_FILE)
        self.toUnfollow = self.following - self.followers
        self.toUnfollow = self.toUnfollow - self.whitelist
        self.cacheIt(TOUNFOLLOW_FILE, self.toUnfollow, "toUnfollow")

    def unfollow(self, user=None, handle=None, userid=None, force=False):
        self.whitelist = self.readFromCache(WHITELIST_FILE)
        if user:
            if user in self.whitelist:
                self.printLog ("############################")
                self.printLog ("Whitelisted!! userid: %s \thandle: %s \tName: %s" % (str(user[0]), str(user[1]), str(user[2])))
                if force:
                    self.api.friendships.destroy(user_id=user[0])
                    self.printLog ("Unfollowing forcefully!!")
                else:
                    self.printLog ("Can't be unfollowed!!")
            else:
                self.api.friendships.destroy(user_id=user[0])
                self.printLog ("Unfollowed id: %s \thandle: %s \tName: %s" % (str(user[0]), str(user[1]), str(user[2])))
            try:
                self.following = self.following.remove(user)
            except Exception as e:
                self.printLog ("Error in removing user from self.following: %s" % str(e))
            self.cacheIt(FOLLOWEE_FILE, self.following, "%s following" % self.user_cred.TWITTER_HANDLE)
            return

        if handle==None and userid==None:
            return
        if handle!=None:
            self.api.friendships.destroy(screen_name=handle)
            self.printLog ("Unfollowed handle:%s"%str(handle))
        else:
            self.api.friendships.destroy(user_id=userid)
            self.printLog ("Unfollowed userid:%s"%str(userid))

    def unfollowAll(self):
        self.cacheToUnfollow()
        if len(self.toUnfollow)>0:
            self.printLog ("Now Unfollowing: %d people"%len(self.toUnfollow))
            for i,user in enumerate(self.toUnfollow):
                if type(user) is list or type(user) is tuple:
                    self.unfollow(user=user)
                    self.following.remove(user)
                    self.cacheIt(cacheFile, self.following, "%s\'s following" % handle)
                else:
                    self.unfollow(userid=user)
                self.printLog("%d/%d Unfollowed" % (i+1, len(self.toUnfollow)))
                if i+1!=len(self.toUnfollow): time.sleep(65)
        else:
            self.printLog("No one to unfollow  :D")

    def updateWhitelist(self):
        # self.whitelist = [line for line in readFile(WHITELIST_FILE) if line!=""] # This is manual, too easy
        h = "abhishek4747"
        self.whitelist = set()
        [self.whitelist.add(follower) for follower in self.getFollowers(handle=h, cacheFile=None)]
        [self.whitelist.add(follower) for follower in self.getFollowing(handle=h, cacheFile=None)]
        self.cacheIt(WHITELIST_FILE, self.whitelist, "whitelist: followers and following of %s" % h)
        return self.whitelist

    def w2tofollow(self):
        self.whitelist = self.readFromCache(WHITELIST_FILE)
        self.toFollow = self.readFromCache(TOFOLLOW_FILE)
        self.following = self.readFromCache(FOLLOWEE_FILE)
        self.toFollow = self.toFollow.union(self.whitelist) - self.following
        self.cacheIt(TOFOLLOW_FILE, self.toFollow, "to follow")

    def updateUnfollowed(self):
        pass

    def autoFollowBack(self):
        pass

    def updateToFollow(self):
        pass

    def tweetScheduled(self):
        pass

    def stats(self):
        # TODO: prints stats of requests and caches
        # Independent of any bot
        pass

    
############################# FUNCTIONS #######################################
def logToFile(filename,s):
    open(filename,'a',encoding='utf-8').write(str(s)+"\n")

def cleanStr(string):
    return str(string.encode('ascii', 'ignore')) #ignore, replace, xmlcharrefreplace

def readFile(filename):
    return [s for s in map(lambda x:x.strip(),open(str(filename)).readlines())]

def get_credentials(filename):
    lines = readFile(filename)
    users = []
    lc = 8 # line count per bot
    for i in range(int((len(lines)+1)/lc)):
        users.append(Credential(lines[i*lc+0],lines[i*lc+1],lines[i*lc+2],
                lines[i*lc+3],lines[i*lc+4],lines[i*lc+5],lines[i*lc+6]))
    return users

def dictify(l,index=0):
    d = dict()
    if type(l) is list:
        for i in l:
            if type(i) is list:
                d[i[index]] = i
            else:
                d[i] = i
        return d
    else:
        try:
            return dict(l)
        except Exception as e:
            return None

#   # TODO: 
    # def auto_follow(q, count=100, result_type="recent"):
    #   result = search_tweets(q, count, result_type)
    #   following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
        
    #   for tweet in result['statuses']:
    #       try:
    #           if tweet['user']['screen_name'] != TWITTER_HANDLE and tweet['user']['id'] not in following:
    #               t.friendships.create(user_id=tweet['user']['id'], follow=True)
    #               following.update(set([tweet['user']['id']]))
                    
    #               print ("followed " + tweet['user']['screen_name'])
                    
    #       except TwitterHTTPError as e:
    #           print ("error: ", e)


    # tweets = t.statuses.home_timeline()

    # def search_tweets(q, count=100, result_type="recent"):
    #   return t.search.tweets(q=q, result_type=result_type, count=count)

    # for i,tweet in enumerate(tweets):
    #   print(i,str(tweet['text'].encode('ascii', 'xmlcharrefreplace'))) #ignore, replace, xmlcharrefreplace

    # def fav_tweet(tweet):
    #   try:
    #       result = t.favorites.create(_id=tweet['id'])
    #       print ("Favorited: %s" % (result['text']))
    #       return result
    #   # when you have already favourited a tweet
    #   # this error is thrown
    #   except TwitterHTTPError as e:
    #       print ("Error: ", e)
    #       return None

    # def auto_fav(q, count=100, result_type="recent"):
    #   result = search_tweets(q, count, result_type)
        
    #   for tweet in result['statuses']:
    #       try:
    #           # don't favorite your own tweets
    #           if tweet['user']['screen_name'] == TWITTER_HANDLE:
    #               continue
                
    #           result = t.favorites.create(_id=tweet['id'])
    #           print ("favorited: %s" % (result['text']))
                
    #       # when you have already favorited a tweet this error is thrown
    #       except TwitterHTTPError as e:
    #           print ("error: ", e)

    # def getFollowersOf(thisuser, thispage):
    #   followerlist = api.GetFollowers(user=thisuser, page=str(thispage))

    #   for x in followerlist:
    #       print(x.screen_name)

    #   time.sleep(30)


    # def auto_unfollow_nonfollowers():
    #   following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    #   followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])
        
    #   # put user IDs here that you want to keep following even if they don't follow you back
    #   users_keep_following = set([])
        
    #   not_following_back = following - followers
        
    #   for userid in not_following_back:
    #       if userid not in users_keep_following:
    #           t.friendships.destroy(user_id=userid)

    # getFollowersOf(TWITTER_HANDLE,1)


