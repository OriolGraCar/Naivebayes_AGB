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
dd <- read.table("/home/helena/Escriptori/2nd_term/AGB/project/ratio_counts.txt", header = T, sep = "\t", dec = ".")#loads the file with the NA ratio accumuative count 

x <- dd$ratio
y<- dd$counts

#y <- (y/37827)*100 

plot(x, y, type="o", main="Percent of correct predictions per attribute", xlab = "Number of attributes", ylab = "Percent of correct predictions",
     col="mediumseagreen"
     #col="chocolate1"
) #plotting the line with the results.

##### PLOT correct versus fail##############
#dat <-read.table(text = " tissue tissue tissue
#                Correct 15 252 333
#               Incorrect 857 525 847", sep = "", header=TRUE)
dat <-read.table(text = "Cerebellum	Cerebellar_Hemisphere	Cingulate_Cortex	Cortex	Hippocampus	Amygdala	Caudate	Hypothalamus	Nucleus_Accumben	Frontal_Cortex	Putamen	Spinal_Cord	Substantia_Nigra
                  Correct	55	35	4	32	12	1	33	8	30	28	6	4	1
                  Incorrect	9	7	24	18	17	13	21	19	19	19	20	1	1", header = T, sep = "\t", dec = ".")

datm <- melt(cbind(dat, ind = rownames(dat)), id.vars = c('ind'))

ggplot(datm,aes(x = variable, y = value, fill = ind)) + 
  geom_bar(position = "fill",stat = "identity") +
  scale_y_continuous(labels = percent_format())

##### COMPARISON with and without pseudocounts####
dat <-read.table(text = "ratio	counts
                          0.562929061784897	p
                          0.5697940503432495	m", header = T, sep = "\t", dec = ".")

barplot(dat$ratio, main="Correct ratio", horiz=TRUE, 
        names.arg=c("No-pseudocounts", "Pseudocounts"),col="mediumseagreen",xlim = c(0,0.6))

### Redundancy ######
dat <-read.table(text = "ratio	counts
                          0.47368421052631576	r
                          0.5697940503432495	m", header = T, sep = "\t", dec = ".")

barplot(dat$ratio, main="Correct ratio", horiz=TRUE, 
        names.arg=c("Redundancy", "No-redundancy"),col="mediumseagreen",xlim = c(0,0.6))




### ROC curve####
# x=y i una linia per cada teixit(color diferent cada un). 
test<-read.table("/home/helena/Escriptori/2nd_term/AGB/project/ROC_data_plot.txt", header = T, sep = "\t", dec = ".")#loads the file with the NA ratio accumuative count 

x<-test$FPR
y<-test$TPR
pdf("./ROC_brain.pdf")
xyplot(y~x,groups= Tissue,data=test,auto.key=T, col=rainbow(14), type="p",
       xlab="FPR",ylab = "TPR",main="ROC curve for brain tissues"

)
dev.off()

