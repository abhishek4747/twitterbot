from twitterbot import *

# datetime.strptime(str(a),"%Y-%m-%d %H:%M:%S.%f")

if __name__=="__main__":
    
    user_list = get_credentials(CREDENTIALS_FILE)
    
    b = Bot(user_list[0])
    b.printLog = lambda x: logToFile("FnUbotLogs.txt", x)

    b.printLog ("\n\n\n\n#################################################################")  
    b.printLog ("Bot starting at %s" % str(datetime.now()))
    login_count = 0
    login_failed= 0
    while True:
        try:
            while b.login():
                login_count += 1
                b.printLog ("Login successful count: %d " % login_count)
                try:
                    # read followedDB
                    followedDB = readFromCache(FOLLOWED_DB)
                    # if not following back 100 entries per request
                    # add to tounfollow
                    pass
                except Exception as e:
                    b.printLog ("Error in while loop: \n%s" % str(e))

                b.printLog ("While loop sleeping for 60 secs\n")
                time.sleep(60)
        except Exception as e:
            login_failed += 1
            b.printLog ("Login Failed count: %d " % login_failed)
        
        b.printLog ("Outer loop sleeping for 60 secs\n")
        time.sleep(60)

