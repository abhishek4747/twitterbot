from twitterbot import *


if __name__=="__main__":
    printLog ("\n\n\n\n#################################################################")  
    printLog ("Bot starting at %s" % str(datetime.now()))
    
    user_list = get_credentials(CREDENTIALS_FILE)
    
    b = Bot(user_list[0])
    b.printLog = lambda x: logToFile("FnUbotLogs.txt", x)

    login_count = 0
    login_failed= 0
    while True:
        try:
            while b.login():
                login_count += 1
                b.printLog ("Login successful count: %d " % login_count)
                try:
                    # Read toFollow
                    toF = dictify(b.readFromCache(TOFOLLOW_FILE))
                    # Follow one from toFollow
                    # Read toUnfollow
                    # Unfollow one from toUnfollow
                    printLog ("Yo")
                except Exception as e:
                    b.printLog ("Error in while loop: \n%s" % str(e))

                b.printLog ("While loop sleeping for 60 secs\n")
                time.sleep(60)
        except Exception as e:
            login_failed += 1
            b.printLog ("Login Failed count: %d " % login_failed)
        
        b.printLog ("Outer loop sleeping for 60 secs\n")
        time.sleep(60)


