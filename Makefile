all:
	@echo "Running main command"

cache:
	@echo "cache"

# r : run
rfnu: FnUbot.py
	python3 FnUbot.py &


# cfe : check for error
cfetb: twitterbot.py
	python3 -m py_compile twitterbot.py

cfeb1: b1.py
	python3 -m py_compile b1.py

cfefnu: FnUbot.py
	python3 -m py_compile FnUbot.py

cfe: cfetb cfeb1 cfefnu

# clean:
killbots:
	pkill python3

