all:
	@echo "make help -- for more detais"
	@echo "\nRules:\n\
rcb: runConsoleBot\n\
ufa: unfollowAll\n\
cfe: cfetb cfeb1 cfefnu cfegw \t\t# check for errror\n\
"

help:
	@echo "help not implemented yet"

# r : run
rfnu: FnUbot.py
	python3 FnUbot.py &

runConsoleBot: consoleBot.py twitterbot.py
	@python3 -i consoleBot.py

unfollowAll: unFollowAll.py twitterbot.py
	@python3 unFollowAll.py &

##############################################################################
# cfe : check for error
##############################################################################
cfetb: twitterbot.py
	python3 -m py_compile twitterbot.py

cfeb1: b1.py
	python3 -m py_compile b1.py

cfefnu: FnUbot.py
	python3 -m py_compile FnUbot.py

cfegw: genWhite.py
	python3 -m py_compile genWhite.py

cfecb: consoleBot.py
	python3 -m py_compile consoleBot.py
 
cfe: cfetb cfeb1 cfefnu cfegw cfecb

##############################################################################
# clean:
##############################################################################
cleanLogs:
	rm logs/*.log
	rm *.log

cleanPyc:
	rm *.pyc

cleanAll: cleanLogs cleanPyc

killbots:
	pkill python3

##############################################################################
# shortcuts of rules
##############################################################################
rcb: runConsoleBot

ufa: unfollowAll

kill: killbots



