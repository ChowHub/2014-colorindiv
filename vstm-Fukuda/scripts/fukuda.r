###################################################################################
#Script for scoring visual working memory task which replicates Fukuda et al (2010)
#
# Michael Chow (2012)
###################################################################################
library(reshape)

#FUNCTIONS
#merge all data frames in folder specified by mypath
multmerge = function(mypath){
    filenames=list.files(path=mypath, full.names=TRUE)
    datalist = lapply(filenames, function(x){read.csv(file=x, sep='\t', header=T)})
    Reduce(function(x,y) {merge(x,y, all.x = TRUE, all.y = TRUE)}, datalist)
}

#COMMAND LINE ARGS
args = commandArgs(trailingOnly = TRUE)
folder = args[1]
out = args[2]
if (is.na(folder)) folder = 'data'
if (is.na(out)) out = 'scored.csv'
paste('Folder: ', folder, '\n', 'Output: ', out)

#MAIN
data = multmerge(folder)
data = data[with(data, order(Subject, block, TrialNumber)),]     #order by subject, block, trial

#determine whether response is correct
data$corr[data$match == "True"] = data$resp[data$match=="True"] == "z"                  #correct same trial response
data$corr[data$match == "False"] = data$resp[data$match=="False"] == "slash"            #correct change trial response

#seperate into 3 conditions (big, small, no change)
bigchange = as.logical((data$stim.probe %in% c(LETTERS[1:6])) & data$stim.corr %in% c(LETTERS[13:18]) | (data$stim.probe %in% c(LETTERS[13:18]) & data$stim.corr %in% c(LETTERS[1:6])))
nochange = data$stim.probe == data$stim.corr
smallchange = !(bigchange | nochange)
sum(smallchange) + sum(bigchange) + sum(nochange)       #print sums of all conditions

#label conditions
data$change.type[nochange] = "same"
data$change.type[bigchange] = "big"
data$change.type[smallchange] = "small"
data$wght = 1

#find proportion correct, derive k
calc.prop = function(df) { 
	df$prop.corr = sum(df$corr) / length(df$corr)
	return(df[1, c("Subject", "change.type", "ttl.stims", "prop.corr")])
}
calc.k = function(df) {
	false.hits = (1 - df[df$change.type == "same", "prop.corr"])
	df$k = df$ttl.stims * (df$prop.corr - false.hits)
	df$false.hits = false.hits
	subset(df, change.type != "same")
}
d = ddply(data, .(Subject, change.type, ttl.stims), calc.prop)
scored = ddply(d, .(Subject, change.type, ttl.stims), calc.k)                                #returns k for set sizes and big / small changes per subject
scored$ttl.stims = as.integer(as.character(scored$ttl.stims))
mscored = melt(scored, id=c("Subject", "change.type", "ttl.stims"))     		#melted
cscored = cast(mscored, Subject ~ change.type + ttl.stims + variable)		#recast so each subject has one row
write.csv(cscored, file = out)
