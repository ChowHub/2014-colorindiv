library('convenience.r')


ovals = LETTERS[1:6]
rects = LETTERS[13:18]

all(data$stim.probe %in% c(ovals, rects))
all(ovals %in% data$stim.probe)
all(rects %in% data$stim.probe)

data$trial.shape = ifelse(data$stim.probe %in% ovals, 'oval', 'rect')


d = ddply(data, .(Subject, change.type, ttl.stims, trial.shape), calc.prop)
scored = ddply(d, .(Subject, trial.shape, ttl.stims), calc.k)
mscored = melt(scored, measure.vars='k')
d.k = cast(mscored, Subject ~ change.type + ttl.stims + trial.shape + variable)



head(d.k, 15)
d.k$small_oval = d.k$small_4_oval_k + d.k$small_8_oval_k
d.k$small_rect = d.k$small_4_rect_k + d.k$small_8_rect_k
d.k$big_oval = d.k$big_4_oval_k + d.k$big_8_oval_k
d.k$big_rect = d.k$big_4_rect_k + d.k$big_8_rect_k

cor(d.k[,c("big_oval", "big_rect", "small_oval", "small_rect")])
plot(d.k[,c("big_oval", "big_rect", "small_oval", "small_rect")])
cor(data.frame(d.k[,grep("_k", names(d.k))]))
