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
FOLLOWEE_FILE       = "myFollowees.tsv"

TOUNFOLLOW_FILE     = "toUnfollow.tsv"
TOFOLLOW_FILE       = "toFollow.tsv"
WHITELIST_FILE      = "whitelist.tsv"
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
    def __init__(self, user_cred,login=None):
        self.user_cred = user_cred
        self.api = None
        self.t = self.api
        self.whitelist = None
        self.toUnfollow = None
        self.followers = None
        self.followees = None
        self.followersCached = True
        self.followeesCached = True
        self.printLog = lambda x: print (str(x))
        if login:
            self.login()

    def login(self):
        try:
            self.api = Twitter(auth=OAuth(self.user_cred.OAUTH_TOKEN, 
                self.user_cred.OAUTH_SECRET, self.user_cred.CONSUMER_KEY, 
                self.user_cred.CONSUMER_SECRET))
            self.t = self.api
            return self.api
        except Exception as e:
            self.printLog (e)
            return None

    def getFollowers(self,handle=None,cacheFile=None):
        if handle==None:
            handle = self.user_cred.TWITTER_HANDLE
        if cacheFile==None:
            cacheFile = FOLLOWER_FILE
        
        self.followers = []
        next = None
        while True:
            if not next:
                followers_list = self.api.followers.list(screen_name=handle)
            else:
                followers_list = self.api.followers.list(screen_name=handle, 
                                                        cursor=next)
            new_followers = [(user['id_str'], user['screen_name'], 
                    cleanStr(user['name'])) for user in followers_list["users"]]
            self.followers += new_followers
            self.printLog ("fetched followers count: %d" % len(new_followers))
            next = followers_list['next_cursor']
            self.cacheIt(FOLLOWER_FILE,self.followers,"%s\'s followers" % handle)
            if followers_list['next_cursor']==0:
                break
            time.sleep(60)
        return self.followers

    def getFollowing(self,handle=None):
        if handle==None:
            handle = self.user_cred.TWITTER_HANDLE
        self.followees = []
        next = None
        while True:
            if not next:
                following_list = self.api.friends.list(screen_name=handle)
            else:
                following_list = self.api.friends.list(screen_name=handle, 
                                                        cursor=next)
            new_friends = [(user['id_str'], user['screen_name'], 
                cleanStr(user['name'])) for user in following_list["users"]]
            self.followees += new_friends
            self.printLog ("fetched friends count: %d" % len(new_friends))
            next = following_list['next_cursor']
            self.cacheFollowees()
            if following_list['next_cursor']==0:
                break
            time.sleep(60)
        return self.followees


    def cacheToUnfollow(self):
        followers = set(list(map(lambda x: x[0],self.getFollowers())))
        following = set(list(map(lambda x: x[0],self.getFollowing())))
        self.toUnfollow = list(following - followers)
        self.cacheIt(TOUNFOLLOW_FILE, self.toUnfollow, "toUnfollow")

    def cacheFollowers(self,FILE_NAME=None,):
        if FILE_NAME==None:
            FILE_NAME=FOLLOWER_FILE
        f = open(FILE_NAME,"w")
        for follower in self.followers:
            f.write("%s\t%s\t%s\n"%(follower[0],follower[1],follower[2]))
        f.close()
        self.printLog ("%d followers cached" % len(self.followers))

    def cacheFollowees(self):
        f = open(FOLLOWEE_FILE,"w")
        for followee in self.followees:
            f.write("%s\t%s\t%s\n"%(followee[0],followee[1],followee[2]))
        f.close()
        self.printLog ("%d followees cached" % len(self.followees))

    def cacheIt(self, filename, variable, name):
        f = open(filename,"w")
        for var in variable:
            if type(var) is list:
                f.write('\t'.join(var)+"\n")
            else:
                f.write(str(var)+"\n")
        f.close()
        self.printLog ("%d %s cached in %s" % (len(variable), str(name), str(filename) ))

    def readFromCache(self, filename):
        l = readFile(filename)
        c = []
        for line in l:
            c.append(line.split('\t'))
        self.printLog ("%d read from %s cached" % (len(l), str(filename) ))
        return c


    def follow(self,handle=None, userid=None):
        if handle==None and userid==None:
            return
        if userid!=None:
            self.api.friendships.create(user_id=userid)
            self.printLog ("followed userid:%s"%str(userid))
        else:
            self.api.friendships.create(screen_name=handle)
            self.printLog ("followed handle:%s"%str(handle))

    def unfollow(self,handle=None, userid=None):
        if handle==None and userid==None:
            return
        if userid!=None:
            self.api.friendships.destroy(user_id=userid)
            self.printLog ("Unfollowed userid:%s"%str(userid))
        else:
            self.api.friendships.destroy(screen_name=handle)
            prinLog("Unfollowed handle:%s"%str(handle))

    def unfollowAll(self):
        self.cacheToUnfollow()
        if len(self.toUnfollow)>0:
            self.printLog ("Now Unfollowing: %d people"%len(self.toUnfollow))
            for user in self.toUnfollow:
                if type(user) is list:
                    self.unfollow(userid=user[0])
                else:
                    self.unfollow(userid=user)
                time.sleep(60)
        else:
            self.printLog("No one to unfollow  :D")

    def updateWhitelist(self):
        # self.whitelist = [line for line in readFile(WHITELIST_FILE) if line!=""] # This is manual, too easy
        self.whitelist = self.getFollowers(self.user_cred.TWITTER_HANDLE)
        f = open(WHITELIST_FILE,"w")
        for user in self.whitelist:
            f.write("%s\t%s\t%s\n"%(user[0],user[1],user[2]))
        f.close()
        self.printLog (len(self.whitelist))
        self.printLog ("whitelist.tsv updated.")
        return self.whitelist

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

    def saveFollowersToFile(self):
        self.cacheIt(FOLLOWER_FILE,self.getFollowers(),"followers ")
        pass

    def saveFolloweesToFile(self):
        self.cacheIt(FOLLOWEE_FILE,self.getFollwing(),"followings ")
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


