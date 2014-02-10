all:
	@echo "make help -- for more detais"
	@echo "\nRules:\n \
rcb: rConsoleBot\n \
rufa: rUnfollowAll\n \
cfe: cfetb cfeb1 cfefnu cfegw \t\t# check for errror\n \
"

##############################################################################
# help : 
##############################################################################
help:
	@echo "help not implemented yet"

##############################################################################
# run : different Bots
##############################################################################
rfnu: FnUbot.py
	python3 FnUbot.py &

rConsoleBot: consoleBot.py twitterbot.py
	@python3 -i consoleBot.py

rUnfollowAll: unFollowAll.py twitterbot.py
	@python3 unFollowAll.py &

rLoopBot: loopBot.py
	python3 loopBot.py &

rLinearBot: linearBot.py
	python3 linearBot.py &

# More bots here

##############################################################################
# cfe : check for error
##############################################################################
cfetb: twitterbot.py
	python3 -m py_compile twitterbot.py

cfsc: scripts.py
	python3 -m py_compile scripts.py

cfefnu: FnUbot.py
	python3 -m py_compile FnUbot.py

cfecb: consoleBot.py
	python3 -m py_compile consoleBot.py

cunfall: unFollowAll.py
	python3 -m py_compile unFollowAll.py

cfeloopb: loopBot.py
	python3 -m py_compile loopBot.py

cfelinearb: linearBot.py
	python3 -m py_compile linearBot.py

cfeinitp: __init__.py
	python3 -m  py_compile __init__.py

cfe: cfetb cfsc cfefnu cfecb cunfall cfeloopb cfelinearb

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
rcb: rConsoleBot

rufa: rUnfollowAll

kill: killbots

ca: cleanAll

cl: cleanLogs

cp: cleanPyc

rlpbot: rLoopBot

rlnbot: rLinearBot