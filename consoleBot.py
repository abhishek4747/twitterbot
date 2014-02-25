from twitterbot import *
try:
	from scripts import *
except Exception as e:
	pass

b = None
def main():
    global b

    user_list = get_credentials(CREDENTIALS_FILE)
    if "__file__" not in locals():	__file__="consoleBot.py"
    b = Bot(user_list[0], login=True, printLog= lambda x: [print(x),logToFile("logs/%s.log"%(__file__.split('.')[0]), x)])

    b.printLog ("\n\n#################### %s ########################" % __file__)  
    b.printLog ("Bot (%s) starting at %s" % (str(b.user_cred.BOT_NAME),str(datetime.now())))
    b.printLog ("Login successful.\n")

if __name__=="__main__":
    main()
