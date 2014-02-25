from twitterbot import *

if __name__=="__main__":
    
    user_list = get_credentials(CREDENTIALS_FILE)
    b = Bot(user_list[0])
    b.printLog = lambda x: [print(x),logToFile(__file__.split('.')[0]+".log", x)]

    b.printLog ("\n\n#################### %s ########################" % __file__)  
    b.printLog ("Loop Bot Template (%s) starting at %s" % (b.user_cred.BOT_NAME, str(datetime.now())))
    login_count = 0
    login_failed= 0
    while True:
        try:
            while b.login():
                login_count += 1
                b.printLog ("Login successful count: %d " % login_count)
                try:
                    # Do something
                    b.printLog("Do something!!")

                except Exception as e:
                    b.printLog ("Error in while loop: \n%s" % str(e))

                b.printLog ("While loop sleeping for 60 secs\n")
                time.sleep(60)
        except Exception as e:
            login_failed += 1
            b.printLog ("Login Failed count: %d " % login_failed)
        
        b.printLog ("Outer loop sleeping for 60 secs\n")
        time.sleep(60)

    b.printLog("I don't know how but Loop Bot is exiting.")

