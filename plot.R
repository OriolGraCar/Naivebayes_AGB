dd <- read.table("/home/helena/Escriptori/2nd_term/AGB/project/Rplot_data.txt", header = T, sep = "\t", dec = ".")

x <- dd$ratio
y<- dd$counts
plot(dd)

y <- (y/37827)

opts = c("p","l","o","b","c","s","S","h")
for(i in 1:length(opts)){
  plot(x, y, type="n", main="NA counts ratio", xlab = "NA ratio", ylab = "Percent of remaining splicing sites")
  lines(x, y, type=opts[i],col="mediumseagreen", main="NA counts")
}
