import getopt

opts, args = getopt.getopt(sys.argv[1:], "hvs:d;i:n:")
server = ""
dest    = ""
interval = 600
start     = 0
for op, value in opts:
if op == "-s":
server = value
elif op = "-d":
dest = value
elif op = "-i":
interval = int(value)
(在开始的getopt中最后的：n需要加上。)