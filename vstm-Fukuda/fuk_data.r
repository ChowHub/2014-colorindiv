fuk$small_8_k = with(fuk, (WOVAL8 + WRECT8)/2)
fuk$small_4_k = with(fuk, (WOVAL4 + WRECT4)/2)
fuk$cd_4 = with(fuk, (BOVAL4 + BRECT4)/2)
fuk$cd_8 = with(fuk, (BOVAL8 + BRECT8)/2)
plot(fuk[,c(grep('small', names(fuk)), grep('cd', names(fuk)))])
plot(fuk[,c(grep('small', names(fuk)), grep('cd', names(fuk)))], col=ifelse(fuk$cd_8 > 6, 'red', 'black'))

with(fuk,plot(small_8_k ~ cd_8))
fit = lm(small_8_k ~ cd_8, data=fuk)
abline(fit, col='blue')
abline(0,0, lty=2, col='grey')

with(fuk, plot(small_4_k ~ cd_4))
fit = lm(small_4_k ~ cd_4, data=fuk)
abline(fit, col='blue')
abline(0,0, lty=2, col='grey')


fuk.ord = fuk[order(fuk$cd_8),]
corrs = 1:nrow(fuk.ord)
for (ii in 1:nrow(fuk.ord)){
  corrs[ii] = with(fuk.ord[1:ii,], cor(cd_8, small_8_k))
}

plot(fuk[,c('WOVAL', 'WRECT', 'BOVAL', 'BCUBE')])