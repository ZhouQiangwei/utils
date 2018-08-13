##bion
norm.test<- function(input.data,alpha=0.05,pic=TRUE){
  if(pic==TRUE){#画图形
    dev.new()
    par(mfrow=c(2,1))
    qqnorm(input.data,main="qq图")
    qqline(input.data)
    hist(input.data,frep=F,main="直方图和密度估计曲线")
    lines(density(input.data),col="blue") #密度估计曲线
    x<- c(round(min(input.data)):round(max(input.data)))
    lines(x,dnorm(x,mean(input.data),sd(input.data)),col="red") #正态分布曲线
  }
  sol<- shapiro.test(input.data)
  if(sol$p.value>alpha){
    print(paste("success:服从正态分布,p.value=",sol$p.value,">",alpha))    
  }else{
    print(paste("error:不服从正态分布,p.value=",sol$p.value,"<=",alpha))
  }
  sol
}

##

ggplot(a,aes(a$V2, a$V1)) + geom_line(aes(color=a$V3)) +geom_point(aes(color=a$V3)) + xlim(0,10000) + xlab("Discordant") + ylab("Concordant") + ggtitle("101bp real Illumina (1 Million)") + theme_bw() + scale_colour_hue("Aligner")

##删除网格线：
# theme(panel.grid =element_blank())
##去掉灰色背景：
# theme_bw()


##run
library(ggplot2)
a<-read.table("C:\\Users\\qwzhou\\Desktop\\bt2\\compare.new.len101.txt")
pdf("test.pdf",width=12, height=7)
outpng<-paste(gsub("pdf","",outFile),"png")
png("test.png",width=860, height=480)
ggplot(a,aes(a$V2, a$V1)) + geom_line(aes(color=a$V3)) + scale_shape_manual(values=c(1,2,3,4,5,6,7)) + geom_point(aes(shape=a$V3,color=a$V3)) + xlim(0,10000) + xlab("Discordant") + ylab("Concordant") + ggtitle("101bp real Illumina (1 Million)") + theme_bw() + scale_colour_hue("Aligner")
dev.off()

# Check if necessary libraries are installed 
check_pkg <- function(pkg) {
  if(require(pkg, character.only = TRUE)){
    print(paste("Package", pkg, "is loaded correctly", sep = " "))
  } else {
    print(paste("Trying to install package", pkg, sep = " "))
    install.packages(pkg, repos="http://cran.us.r-project.org", dep = TRUE)
    if(require(pkg, character.only = TRUE)){
      print(paste("Package", pkg, "is installed and loaded correctly", sep = ""))
    } else{
      install.packages(pkg, repos="http://cran.rstudio.com/", dep = TRUE)
      if(require(pkg, character.only = TRUE)){
        print(paste("Package", pkg, "is installed and loaded correctly", sep = ""))
      } else{
        stop(paste("Couldn't install package", pkg, sep = " "));
      }
    }
  }
}
check_pkg("xtable")
#check_pkg("RCircos")
#check_pkg("grid")



install.packages("xtable", repos = "http://cran.us.r-project.org", dep = TRUE)
library(xtable)
filename<-"outfiles"
a<-read.table(paste("C:/Users/qwzhou/Desktop/bt2/BatMeth2_Report/files/", filename, ".txt", sep=""), header=T, sep="\t")
##

c <- xtable(a, align = c("c", "c", "c"))
header<-"<!DOCTYPE HTML>
<html lang=\"en-US\">
<meta charset=\"UTF-8\">
<link rel=\"stylesheet\" type=\"text/css\" href=\"../style.css\" media=\"all\" />"
write(header, file=paste("C:\\Users\\qwzhou\\Desktop\\bt2/BatMeth2_Report/files/", filename, ".html", sep = ""))
print(c, type='html', file=paste("C:\\Users\\qwzhou\\Desktop\\bt2/BatMeth2_Report/files/", filename , ".html",sep = ""), include.rownames = F, append = T, html.table.attributes = "class = 'mytable'")

##############################
ggplot(a,aes(a$V2, a$V1)) + geom_line(aes(color=a$V3)) + scale_shape_manual(values=c(1,2,3,4,5,6,7)) + geom_point(aes(shape=a$V3,color=a$V3)) + xlim(0,10000) + xlab("Discordant") + ylab("Concordant") + ggtitle("90bp real Illumina (1 Million)") + theme_bw() + theme(panel.grid =element_blank())

##动态图
install.packages("plotly")
library(plotly)
p<-ggplotly(p)


###############
Methylp<-read.table("C:\\Users\\qwzhou\\Desktop\\bt2\\bwameth.methBins.txt")
colnames(Methylp) <- c('chr', 'pos', 'Methyl', 'context')
Methyl<-Methylp[Methylp$Methyl>=0,]
chrMethyl<-Methyl[Methyl$context=="CG",]
chr<-levels(chrMethyl$chr)
chrNum=length(chr)
maxMeth=1:chrNum
maxMethOri=1:chrNum
POINT=FALSE
for (i in 1:chrNum){ 
  ndx <- which(chrMethyl[, 1]==chr[i] )
  lstMeth <- max(chrMethyl[ndx, 2])
  if(i > 1) maxMeth[i] <- (lstMeth - maxMethOri[i-1])
  else maxMeth[i] <- lstMeth
  maxMethOri[i] <- lstMeth
  if(maxMeth[i]<=1000) POINT=TRUE
  if (i < chrNum) ndx2 <- which(chrMethyl[, 1]== chr[i+1] )
  if (i < chrNum) chrMethyl[ndx2, 2] <- chrMethyl[ndx2, 2] + lstMeth
}

ggplot() + stat_smooth(se=F,size=1,data=chrMethyl,aes(x=pos, y=Methyl,group=as.factor(gsub("Chr|chr","CG",chr) ), colour="indianred1" ), method="loess", linetype=1, span = 1)
