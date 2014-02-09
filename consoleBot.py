from twitterbot import *

b = None
def main():
    global b
    user_list = get_credentials(CREDENTIALS_FILE)
    
    b = Bot(user_list[0],login=True)
    b.printLog = lambda x: [print(x),logToFile("logs/%s.log"%(__file__.split('.')[0]), x)]

    b.printLog ("\n\n#################################################################")  
    b.printLog ("Bot (%s) starting at %s" % (str(b.user_cred.BOT_NAME),str(datetime.now())))
    b.printLog ("Login successful.")

if __name__=="__main__":
    main()
