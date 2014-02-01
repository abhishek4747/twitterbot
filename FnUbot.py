from twitterbot import *


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
                    # Read toFollow
                    toF = b.readFromCache(TOFOLLOW_FILE)
                    
                    # Follow one from toFollow
                    if len(toF)>0:
                        b.follow(handle=toF[0][1])
                    else:
                        b.printLog ("No one to follow")
                    
                    # Read toUnfollow
                    toUf = b.readFromCache(TOUNFOLLOW_FILE)

                    # Unfollow one from toUnfollow
                    if len(toUf)>0:
                        b.unfollow(handle=toUf[0][1])
                    else:
                        b.printLog ("No one to unfollow")

                except Exception as e:
                    b.printLog ("Error in while loop: \n%s" % str(e))

                b.printLog ("While loop sleeping for 60 secs\n")
                time.sleep(60)
        except Exception as e:
            login_failed += 1
            b.printLog ("Login Failed count: %d " % login_failed)
        
        b.printLog ("Outer loop sleeping for 60 secs\n")
        time.sleep(60)

