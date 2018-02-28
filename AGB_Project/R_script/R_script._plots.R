library(ggplot2) ## install.packages("package_name") if you do not have any library
library(reshape)
library(scales)
library(lattice)

#### Histogram for NA #####
dd <- read.table("/home/helena/Escriptori/2nd_term/AGB/project/NA_tissue_sum.txt", header = T, sep = "\t", dec = ".")#loads the file with the NA ratio accumuative count 

x <- dd$ratio
y<- dd$counts

y <- (y/37827)*100 

plot(x, y, type="h", main="NA counts ratio", xlab = "NA ratio", ylab = "Percent of remaining splicing sites",
     #col="mediumseagreen" #for tissue
     col="chocolate1" #for brain
     ) #plotting the histogram

### % correct per quant of attributes############
# quants encertem amb un attribut, quants amb 2, quants amb 3.... -> GRAPH DE UNA SOLA LINIA CURVA
dd <- read.table("/home/helena/Escriptori/2nd_term/AGB/project/NA_tissue_sum.txt", header = T, sep = "\t", dec = ".")#loads the file with the NA ratio accumuative count 

x <- dd$ratio
y<- dd$counts

y <- (y/37827)*100 

plot(x, y, type="p", main="Percent of correct predictions per attribute", xlab = "Number of attributes", ylab = "Percent of correct predictions",
     #col="mediumseagreen",
     col="chocolate1"
) #plotting the line with the results.

##### PLOT correct versus fail##############
#dat <-read.table(text = " tissue tissue tissue
#                Correct 15 252 333
#               Incorrect 857 525 847", sep = "", header=TRUE)
dat <-read.table("/home/helena/Escriptori/2nd_term/AGB/project/NA_tissue_sum.txt", header = T, sep = "\t", dec = ".")

datm <- melt(cbind(dat, ind = rownames(dat)), id.vars = c('ind'))

ggplot(datm,aes(x = variable, y = value, fill = ind)) + 
  geom_bar(position = "fill",stat = "identity") +
  scale_y_continuous(labels = percent_format())

##### 10-FOLD graphic #####
dat <-read.table("/home/helena/Escriptori/2nd_term/AGB/project/NA_tissue_sum.txt", header = T, sep = "\t", dec = ".")

datm <- melt(cbind(dat, ind = rownames(dat)), id.vars = c('ind'))

ggplot(datm,aes(x = variable, y = value, fill = ind)) + 
  geom_bar(position = "fill",stat = "identity") +
  scale_y_continuous(labels = percent_format())

##### COMPARISON with and without pseudocounts####
dat <-read.table("/home/helena/Escriptori/2nd_term/AGB/project/NA_tissue_sum.txt", header = T, sep = "\t", dec = ".")

datm <- melt(cbind(dat, ind = rownames(dat)), id.vars = c('ind'))

ggplot(datm,aes(x = variable, y = value, fill = ind)) + 
  geom_bar(position = "fill",stat = "identity") +
  scale_y_continuous(labels = percent_format())






### ROC curve####
# x=y i una linia per cada teixit(color diferent cada un). 
#test <- read.table(text= "FPR	TPR	Tissue	Tr
#                          1	3	hola	2
 #                         2	5	hola	3
  #                        3	8	hola	5
   #                       1	3	adeu	3
    #                      3	5	adeu	2
     #                     5	7	adeu	2", sep="\t", header=TRUE)
x<-test$FPR
y<-test$TPR
xyplot(x~y,type="o",groups= Tissue,data=test,auto.key=T)


