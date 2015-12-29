library(tm)
library(xlsx)
getwd()
setwd("D:/使用者/skywayoo/Desktop/trainset")

#give label
#Apparel give label
Apath <- DirSource("D:/使用者/skywayoo/Desktop/trainset/Apparel")
apparel <- data.frame()
for(i in 1:length(Apath$filelist)){
        box <- read.xlsx(Apath$filelist[i],sheetIndex = 1,encoding = 'UTF-8')
        box <- box[,1:10]
        box <- subset(box,box$KeywordId!="NA")
        apparel <- rbind(apparel,box)
}
write.csv(apparel,file="apparel.csv")
#Beauty_Personal_Care give label
setwd("D:/使用者/skywayoo/Desktop/trainset/Beauty_Personal_Care")
BPCpath <- DirSource("D:/使用者/skywayoo/Desktop/trainset/Beauty_Personal_Care")
BPC <- data.frame()
for(i in 1:length(BPCpath$filelist)){
        box <- read.xlsx(BPCpath$filelist[i],sheetIndex = 1,encoding = 'UTF-8')
        box <- box[1:500,1:10]
        box <- subset(box,box$KeywordId!="NA")
        BPC <- rbind(BPC,box)
}
write.csv(BPC,file="BPC.csv")
#Business_Industrial give label
setwd("D:/使用者/skywayoo/Desktop/trainset/Business_Industrial")
BIpath <- DirSource("D:/使用者/skywayoo/Desktop/trainset/Business_Industrial")
BI <- data.frame()
for(i in 1:length(BIpath$filelist)){
        box <- read.xlsx(BIpath$filelist[i],sheetIndex = 1,encoding = 'UTF-8')
        box <- box[1:500,1:10]
        box <- subset(box,box$KeywordId!="NA")
        BI <- rbind(BI,box)
}
write.csv("BI.csv",BI)
#Computers_Consumer_Electronics give label
setwd("D:/使用者/skywayoo/Desktop/trainset/Computers_Consumer_Electronics")
CCEpath <- DirSource("D:/使用者/skywayoo/Desktop/trainset/Computers_Consumer_Electronics")
CCE <- data.frame()
for(i in 1:length(CCEpath$filelist)){
        box <- read.xlsx(CCEpath$filelist[i],sheetIndex = 1,encoding = 'UTF-8')
        box <- box[1:500,1:10]
        box <- subset(box,box$KeywordId!="NA")
        CCE <- rbind(CCE,box)
}
write.csv("CCE.csv",CCE)
#Finance give label
setwd("D:/使用者/skywayoo/Desktop/trainset/Finance")
Fpath <- DirSource("D:/使用者/skywayoo/Desktop/trainset/Finance")
Finance <- data.frame()
for(i in 1:length(Fpath$filelist)){
        box <- read.xlsx(Fpath$filelist[i],sheetIndex = 1,encoding = 'UTF-8')
        box <- box[1:500,1:10]
        box <- subset(box,box$KeywordId!="NA")
        Finance <- rbind(Finance,box)
}
write.csv("Finance.csv",Finance)
#Jobs_Education give label
setwd("D:/使用者/skywayoo/Desktop/trainset/Jobs_Education")
JEpath <- DirSource("D:/使用者/skywayoo/Desktop/trainset/Jobs_Education")
JE <- data.frame()
for(i in 1:length(JEpath$filelist)){
        box <- read.xlsx(JEpath$filelist[i],sheetIndex = 1,encoding = 'UTF-8')
        box <- box[1:500,1:10]
        box <- subset(box,box$KeywordId!="NA")
        JE <- rbind(JE,box)
}
write.csv("JE.csv",JE)
