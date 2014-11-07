#Convenience functions for analyzing the fukuda task, includes plots

#select a subset of fukuda data
fuk.sub = function(data, ttl.stims = 4, change = c('small', 'big')[1]){
	#return(data$ttl.stims == ttl.stims & data$change == change)
	index = data$change == change & data$ttl.stims == ttl.stims
	return(subset(data, index))
}

#plot each fukuda condition against the zlVSTM
plot.vwm = function(data, ttl.stims = c(4, 8), change = c('small', 'big')){
	par(mfcol = c(4,4))
	for (ii in change){
		for (jj in ttl.stims){
			subdat = fuk.sub(data, jj, ii)
			xaxt = c(rep('n', 3), 's')
			yvar = c('zlset4.sd',  'zlset6.sd', 'zlset4.p', 'zlset6.p')			
			xlab = c(paste(jj, ii, 'change (K)', sep = " "),rep('', 3))
			#first column plots only
			if (ii == change[1] & jj == ttl.stims[1]) {
				ylab = yvar
				yaxt = rep('s', 4)				
				mar = matrix(c(c(.1, 3.9, 3.9, .1), rep(c(2,3.9,2,.1), 3)), nrow = 4)
				}
			else {
				ylab = rep('', 4)			
				yaxt = rep('n', 4)
				mar = matrix(c(c(.1, 2, 3.9, 2), rep(c(2,2,2,2), 3)), nrow = 4)
				}
			#draw plots
			for (round in 1:4) {
				print(mar)
				par(mar = mar[,round])
				plot(subdat$k, subdat[, yvar[round]], main = xlab[round], ylab = ylab[round], xaxt = xaxt[round], yaxt = yaxt[round])
				}

		}
	}
}

#comparisons for conditions within fukuda task, takes advantage of plot() with DFs
plot.fuk = function(data, ttl.stims = c(4, 8), change = c('small', 'big')){
	newdat = c()
	for (ii in change){
		for (jj in ttl.stims){
		
		subdat = fuk.sub(data, jj, ii)
		newdat = cbind(newdat, subdat$k)
		}
	}
	colnames(newdat) = paste(rep(change, each = length(ttl.stims)), ttl.stims, sep = "-")
	plot(data.frame(newdat))
}

plot.zl = function(data){
	subdat = fuk.sub(data, 4, 'small') #just need one instance per subject
	plot(subdat[,c('zlset4.sd', 'zlset6.sd', 'zlset4.p', 'zlset6.p')])
}

plot.lots = function(data) {
	index = c('k', 'zlset4.sd', 'zlset6.sd', 'zlset4.p', 'zlset6.p', 'ospan.span_Abs', 'rspan.span_Abs', 'sspan.span_Abs')
	plot(new[, index])
}