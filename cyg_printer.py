import sys
for line in sys.stdin:
	print (line.replace('\\n','\n').replace('\\t','\t'))
