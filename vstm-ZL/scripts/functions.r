#Parameters
#mu: mean
#kappa: analagous to sd for directional distrubtion
#p: probability of "getting it right"



#CONVERSIONS

ktosd = function(k){sqrt(1/k)*(360/(2*pi))}

#Cast data between -180 and 180
calcDiff = function(data){
	data$Diff = data$Response - data$Stim
	data$Diff = data$Diff * 2
	for (ii in 1:length(data$Diff)){
		if (data$Diff[ii] > 180) data$Diff[ii] = data$Diff[ii] - 360
		if (data$Diff[ii] < -180) data$Diff[ii] = 360 + data$Diff[ii]
		}
	data$radD = data$Diff*2*pi/360
	return(data)
}

#VON-MISES + UNIFORM MIXED MODELS
#generate random sample
genvonmixed = function(N, mu, kappa, p){choose = runif(N) < p; c(rvm(sum(choose), mu, kappa), runif(sum(!choose), 0, 2*pi))}
#density with non-vector model parameters
dvonmixed = function(theta, mu, kappa, p){ (abs(p)/100)*dvm(theta, mu, abs(kappa)) + (1-(abs(p)/100))*dunif(abs(theta), 0, 2*pi)}
#likelihood with non-vector model parameters
Lvonmixed = function(theta, mu, kappa, p){-sum(log(dvonmixed(theta,mu,kappa,p)))}
#likelihood with model parameters as vector
L2vonmixed = function(theta, par){
    ret = -sum(log(dvonmixed(theta,par[1],par[2],par[3])))
    if (is.nan(ret)) return(.Machine$double.xmax)
    else return(ret)
}
L2vm = function(theta, kappa){-sum(log(dvm(theta, 0, abs(kappa))))}
#fixed mean at 0
L2vonmixed.fixmew = function(theta, par){-sum(log(dvonmixed(theta,0,par[1],par[2])))}

#MLE ESTIMATORS
optim.grid = function(seqk, seqp, theta){
	bestpar = c()
	bestmle = Inf
	count = 0
	allpars = c()
	for (start.k in seqk){
		for (start.p in seqp){
			new.par = optim(par = c(0,start.k,start.p), L2vonmixed, theta = theta, method = "L-BFGS-B", lower = -99.9, upper = 99.9)$par		#optimize 3 par model
			new.mle = L2vonmixed(theta, new.par)
			if ( !is.nan(new.mle) & (new.mle < bestmle) ) {
				bestmle = new.mle
				bestpar = new.par
				allpars = c(allpars, new.par)
				count = count + 1
			}
		}
	}
	print(count)
	print(allpars)
	print(bestmle)
	return(bestpar)
}


###
#Simulations
sim.vm = function(range.k, range.p, mu,  cycles, N, cross = TRUE){
	if (cross == TRUE){
		output = matrix(nrow = length(range.k)*length(range.p)*cycles, ncol = 5)
		colnames(output) = c("kappa", "p", "mew_hat", "kappa_hat", "p_hat")
		cycle = 0
		for (ii_k in range.k){
			for (ii_p in range.p){
				for (jj in 1:cycles){
					cycle = cycle + 1
					data = genvonmixed(N, mu, ii_k, ii_p)
					output[cycle, 1:2] = c(ii_k, ii_p)
					output[cycle,3:5] = abs(optim(par = c(0,7,50), L2vonmixed, theta = data, method = "L-BFGS-B", lower = -100, upper = 100, control = list(trace = 0))$par)
					
				}
			}
		}
	}
	else{
		output = matrix(nrow = length(range.k)*cycles, ncol = 5)
		colnames(output) = c("kappa", "p", "mew_hat", "kappa_hat", "p_hat")
		for (ii in 1:length(range.k)){
			for (jj in 1:cycles){
				data = genvonmixed(N, mu, range.k[ii], range.p[ii])
				output[ii*jj, 1:2] = c(range.k[ii], range.p[ii])
				output[ii*jj, 3:5] = abs(optim(par = c(0,7,50), L2vonmixed, theta = data, method = "L-BFGS-B", lower = -100, upper = 100, control = list(trace = 0))$par)
			}
		}
	}
	return(output)
}

#2 von-mises distribution model
d2vonmixed = function(theta, mu, kappa, mu2, kappa2, p){ (p/100)*dvm(theta, mu, kappa) + (1-(p/100))*dvm(theta, mu2, kappa2)}
L2d2vonmixed = function(theta, par){-sum(log(d2vonmixed(theta,par[1],par[2],par[3], par[4], par[5])))}


MLE.surface = function(theta, range.K, range.P, L.func){
	M = matrix(ncol = 3, nrow = length(range.K)*length(range.P))
	cycle = 0
	for (K in range.K){
		for (P in range.P){
			cycle = cycle +1
			M[cycle, 1:2] = c(K, P)
			M[cycle, 3] = L.func(theta, c(K, P))
		}
	}
	return(M)
}
