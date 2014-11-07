setwd("Data/IQ")
dir()
d = read.csv("scored_surfdev.csv", check.names = FALSE, stringsAsFactors = FALSE)
scored = apply(d[,-1], 1, FUN = match.fun("=="), e2 = key)  		#I don't know why simply d == key, or some transpose didn't work
key = d[1,-1]
