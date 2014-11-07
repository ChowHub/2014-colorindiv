#hack to source scripts from same folder as script
source_local <- function(fname){
    argv <- commandArgs(trailingOnly = FALSE)
    base_dir <- dirname(substring(argv[grep("--file=", argv)], 8))
    source(paste(base_dir, fname, sep="/"))
}

library(CircStats)
source_local('functions.r')

#INPUTS#
dirname = commandArgs(trailingOnly=TRUE)
outdir = 'out'

#MAIN#
#Cycle through data
vnames = c('Stim', 'Response', 'SetSize')
numSubs = length(dir(dirname))
for (ii in dir()){
	if (substr(ii,1,5)=="VSTMz" && substr(ii, nchar(ii)-2, nchar(ii)) != 'mat') numSubs = numSubs +1
}
M = matrix(nrow = numSubs, ncol = 11)
dimnames(M) = list(c(), c('Subject', 'set4.mu', 'set4.kappa', 'set4.p', 'set6.mu', 'set6.kappa', 'set6.p', 'set4.mle', 'set4.mle.justk', 'set6.mle', 'set6.mle.justk'))
row = 1
for (ii in dir(dirname, full.names=TRUE)){
    print(ii)
    data = read.csv(ii)
    names(data) = vnames
    data = calcDiff(data)
    for (numstims in c(4,6)){
        data.sub = subset(data, data$SetSize == numstims)
        #TODO: optimize across a grid of starting pars
        #par = optim(par = c(0,10,50), L2vonmixed, theta = data.sub$radD, method = "L-BFGS-B", lower = -100, upper = 100)$par		#optimize 3 par model
        par = optim.grid(seq(.2, 20, .2), seq(10, 99, 10), data.sub$radD)
        justK = optim(par = c(5), L2vm, theta = data.sub$radD, method = "L-BFGS-B", lower = -100, upper = 100)$par					#optimize fixed mean and p
        logL = L2vonmixed(data.sub$radD, par)																						#Log likelihoods
        print(logL)
        logL.justk = Lvonmixed(data.sub$radD, 0, justK, 1)
        cols = paste('set', rep(numstims, 5), c('.mu', '.kappa', '.p', '.mle', '.mle.justk'), sep = '')								#write to matrix
        print(cols)
        print(dimnames(M))
        M[row,cols] = c(par, logL, logL.justk)				
        M[row, "Subject"] = as.integer(strsplit(ii, '_')[[1]][3])
    }
    row = row + 1		
    #hist(genvonmixed(1000, pi, justK, 1))
    #hist(genvonmixed(1000, pi + par[1], par[2], par[3]))
}
zldata = data.frame(abs(M))
#for (name in names(zldata)[-1]){zldata[,name] = as.real(as.matrix(zldata[,name]))}
zldata$set4.sd = ktosd(zldata$set4.kappa)
zldata$set6.sd = ktosd(zldata$set6.kappa)
save(zldata, file=file.path(outdir,"zldata"))
