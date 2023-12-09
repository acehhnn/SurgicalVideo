# 任务一调参
# x = read.table('E:\\project\\operation_video\\变点分析\\changepoint\\Manuscript\\data\\new_para\\2.txt') # F1
x1 = read.table("D:\\THU\\3spring\\_denglab\\learning\\fakeblood_test\\result_8_6\\error_report_rtrain.txt") # err_report
x2 = read.table("D:\\THU\\3spring\\_denglab\\learning\\fakeblood_test\\result_8_6\\missing_report_rtrain.txt") # miss_report
x3 = read.table("D:\\THU\\3spring\\_denglab\\learning\\fakeblood_test\\result_8_6\\sensitivity_rtrain.txt") # sen
x4 = read.table("D:\\THU\\3spring\\_denglab\\learning\\fakeblood_test\\result_7_6\\specificity_rtrain.txt") # spe

# x1 = read.table('C:\\Users\\abc\\Desktop\\1.txt') # err_report
# x2 = read.table('C:\\Users\\abc\\Desktop\\2.txt') # miss_report
# x3 = read.table('C:\\Users\\abc\\Desktop\\3.txt') # sen
# x4 = read.table('C:\\Users\\abc\\Desktop\\4.txt') # spe

# train = unlist(y)
train = unlist(x4)
train = as.numeric(train)
threshold = seq(from=0.005,to=0.1,length.out=20)
threshold = round(threshold,3)
Beta = c(rep('Beta=50',20),rep('Beta=60',20),
         rep('Beta=70',20),rep('Beta=80',20),
         rep('Beta=90',20),rep('Beta=100',20),
         rep('Beta=110',20),rep('Beta=120',20),
         rep('Beta=130',20),rep('Beta=140',20))
Data1 = rbind(train[Beta=='Beta=50'],train[Beta=='Beta=60'],
              train[Beta=='Beta=70'],train[Beta=='Beta=80'],
              train[Beta=='Beta=90'],train[Beta=='Beta=100'],
              train[Beta=='Beta=110'],train[Beta=='Beta=120'],
              train[Beta=='Beta=130'],train[Beta=='Beta=140'])
rownames(Data1) <- c('50','60','70','80',
                     '90','100','110','120','130','140')
colnames(Data1) <- as.factor(sprintf("%0.3f", threshold))
Data2 = round(Data1,2)
library(pheatmap)
library(ggsci)
# pheatmap(Data2,cluster_rows = F,display_numbers=Data2,
#          fontsize_number=14,fontsize_row=14,fontsize_col=14,
#          cluster_cols = F,
#          color = colorRampPalette(c('#D26763','white','#1F77B4'))(100))
pheatmap(Data2,cluster_rows = F,display_numbers=Data2,
         fontsize_number=14,fontsize_row=14,fontsize_col=14,
         cluster_cols = F,
         color = colorRampPalette(c('#1F77B4','white','#D26763'))(100))
# 1600,400

# Error 绘图
# x = read.table('C:\\Users\\abc\\Desktop\\dif1.txt')
x = read.table('/Users/hantingxuan/Desktop/Research/Project/operation_video/code-summary/PELT-changepoint-paper1/new_dif2/dif1.txt')
train = unlist(x)
train = as.numeric(train)
mean(abs(train))
# x = read.table('C:\\Users\\abc\\Desktop\\dif2.txt')
x = read.table('/Users/hantingxuan/Desktop/Research/Project/operation_video/code-summary/PELT-changepoint-paper1/new_dif2/dif2.txt')
test = unlist(x)
test = as.numeric(test)
mean(abs(test))
Error = c(train,test)
mean(abs(Error))
# Error = abs(Error)
label = c(rep('Train',length(train)),rep('Test',length(test)))
ID = c(1:length(Error))
data = data.frame(ID,Error,label)

label = rep('Train',length(train))
# train = abs(train)
data_train = data.frame(train,label)
label = rep('Test',length(test))
# test = abs(test)
data_test = data.frame(test,label)
library(ggplot2)

p1 = ggplot(data_train,aes(train,fill=label))+
  geom_histogram(position="identity",alpha = 1,
                 aes(y=..count..),binwidth = 3,
                 colour = "white")+
  xlab('Detection Error') + ylab('Count')+
  ggtitle('Training Set')+
  theme_bw()+
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.position="none")+
  scale_fill_manual(values = c('#1F77B4'))+xlim(-55,55)#+xlim(-300,100)+ylim(0,17)
#  +xlim(-10,300)
p1 = p1+scale_y_continuous(expand = c(0,0), limits = c(0,10))
p1
p2 = ggplot(data_test,aes(test,fill=label))+
  geom_histogram(position="identity",alpha = 1,
                 aes(y=..count..),binwidth = 3,
                 colour = "white")+
  xlab('Detection Error') + ylab('Count')+
  ggtitle('Test Set')+
  theme_bw()+
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.position="none")+
  scale_fill_manual(values = c('#D26763'))+xlim(-55,55)#+xlim(-300,100)+ylim(0,17)

p2 = p2+scale_y_continuous(expand = c(0,0), limits = c(0,10))
p2
p3 = ggplot(data,aes(Error))+
  geom_histogram(position="identity",alpha = 1,
                 aes(y=..count..),binwidth = 3,
                 colour = "white",fill='black')+
  xlab('Detection Error') + ylab('Count')+
  ggtitle('Full Set')+
  theme_bw()+
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        legend.position="none")+xlim(-55,55)#+xlim(-300,100)+ylim(0,17)
p3 = p3+scale_y_continuous(expand = c(0,0), limits = c(0,10))
p3
library(ggpubr)
p <- ggarrange(p1,p2,p3, labels = c(),
               label.x = 0, label.y = 1.02, # 调整标签位置
               ncol = 3, nrow = 1,common.legend = F)
p
ggsave('C:\\Users\\abc\\Desktop\\error.png',p,height=3,width=6)

# ROC curve
# x3 = read.table('/Users/hantingxuan/Desktop/Research/Project/operation_video/code-summary/PELT-changepoint-paper1/new_para2/3.txt') # sen
# x4 = read.table('/Users/hantingxuan/Desktop/Research/Project/operation_video/code-summary/PELT-changepoint-paper1/new_para2/4.txt') # spe
# TPR = x3
# FPR = 1-x4
# rocs = data.frame(TPR,FPR)
# names(rocs) = c('TPR','FPR')
# head(rocs)
# threshold = seq(from=0.005,to=0.1,length.out=20)
# threshold = round(threshold,3)
# Beta = c(rep('Beta=50',20),rep('Beta=60',20),
#          rep('Beta=70',20),rep('Beta=80',20),
#          rep('Beta=90',20),rep('Beta=100',20),
#          rep('Beta=110',20),rep('Beta=120',20))
# Data1 = rocs[which(Beta=='Beta=50'),]
# 
# library(ggplot2)
# ggplot(Data1, aes(FPR,TPR))+
#   geom_point(size=2,color="red")+
#   geom_path()+
#   # coord_fixed()+
#   theme_bw()


# ROC curve for videos
library(pROC)
# K=50 96.6
data1 = read.csv('/Users/hantingxuan/Desktop/Research/Project/operation_video/code-summary/PELT-changepoint-paper1/roc/K_50.csv',
         header = T)
# K=60 96.9
data1 = read.csv('/Users/hantingxuan/Desktop/Research/Project/operation_video/code-summary/PELT-changepoint-paper1/roc/K_60.csv',
                 header = T)
# K=70 96.6
data1 = read.csv('/Users/hantingxuan/Desktop/Research/Project/operation_video/code-summary/PELT-changepoint-paper1/roc/K_70.csv',
                 header = T)
# K=80 97.3
data1 = read.csv('/Users/hantingxuan/Desktop/Research/Project/operation_video/code-summary/PELT-changepoint-paper1/roc/K_80.csv',
                 header = T)
# K=90 96.8
data1 = read.csv('/Users/hantingxuan/Desktop/Research/Project/operation_video/code-summary/PELT-changepoint-paper1/roc/K_90.csv',
                 header = T)
# K=100 97.5
data1 = read.csv('/Users/hantingxuan/Desktop/Research/Project/operation_video/code-summary/PELT-changepoint-paper1/roc/K_100.csv',
                 header = T)
# K=110 97.5
data1 = read.csv('/Users/hantingxuan/Desktop/Research/Project/operation_video/code-summary/PELT-changepoint-paper1/roc/K_110.csv',
                 header = T)
# K=120 97.0
data1 = read.csv('/Users/hantingxuan/Desktop/Research/Project/operation_video/code-summary/PELT-changepoint-paper1/roc/K_120.csv',
                 header = T)

data1 = data1[,2:3]
head(data1)
# roc1 <- roc(real~increase_max,data=data1)
# plot.roc(roc1,print.auc=TRUE,auc.polygon=TRUE,print.thres = TRUE)
# library(dplyr)
# ci.auc(roc1)

library(pROC)
rocobj <- plot.roc(data1$real, data1$increase_max,
                   main="ROC Curve of Bleeding Video Classification", percent=TRUE,
                   ci=TRUE, # compute AUC (of AUC by default)
                   print.auc=TRUE,
                   # thresholds="best", # 基于youden指数选择roc曲线最佳阈值点
                   # print.thres='best',
                   # print.thres.pattern="Cut-off: %.3f",
                   print.auc.x = 80,
                   print.auc.y = 80,
                   auc.polygon=TRUE) # print the AUC (will contain the CI)
ciobj <- ci.se(rocobj, # CI of sensitivity
               specificities=seq(0, 100, 5)) # over a select set of specificities
plot(ciobj, type="shape", col="#1c61b6AA") # plot as a blue shape\

#---- training set
data1 = read.csv('/Users/hantingxuan/Desktop/Research/Project/operation_video/code-summary/PELT-changepoint-paper1/roc/train/K_110.csv',
                 header = T)
data1 = data1[,2:3]
head(data1)
library(pROC)
rocobj <- plot.roc(data1$real, data1$increase_max,
                   main="ROC of Training Set", percent=TRUE,
                   ci=TRUE, # compute AUC (of AUC by default)
                   print.auc=TRUE,
                   # thresholds="best", # 基于youden指数选择roc曲线最佳阈值点
                   # print.thres='best',
                   # print.thres.pattern="Cut-off: %.3f",
                   print.auc.x = 80,
                   print.auc.y = 80,
                   auc.polygon=TRUE) # print the AUC (will contain the CI)
ciobj <- ci.se(rocobj, # CI of sensitivity
               specificities=seq(0, 100, 5)) # over a select set of specificities
plot(ciobj, type="shape", col="#1c61b6AA") # plot as a blue shape\

#---- test set
data1 = read.csv('/Users/hantingxuan/Desktop/Research/Project/operation_video/code-summary/PELT-changepoint-paper1/roc/test/K_110.csv',
                 header = T)
data1 = data1[,2:3]
head(data1)
library(pROC)
rocobj <- plot.roc(data1$real, data1$increase_max,
                   main="ROC of Test Set", percent=TRUE,
                   ci=TRUE, # compute AUC (of AUC by default)
                   print.auc=TRUE,
                   # thresholds="best", # 基于youden指数选择roc曲线最佳阈值点
                   # print.thres='best',
                   # print.thres.pattern="Cut-off: %.3f",
                   print.auc.x = 80,
                   print.auc.y = 80,
                   auc.polygon=TRUE) # print the AUC (will contain the CI)
ciobj <- ci.se(rocobj, # CI of sensitivity
               specificities=seq(0, 100, 5)) # over a select set of specificities
plot(ciobj, type="shape", col="#1c61b6AA") # plot as a blue shape\


################################################################################
# Fake data information
fakedata = data.frame(
  ID = c(1:16),
  Event = c(1441,672,1194,1733,2074,832,397,1592,2066,2705,2098,2900,1764,1206,2036,3693),
  Total = c(7520,1980,2834,3820,3840,3800,2980,2700,3860,4060,5940,5420,3720,3000,4260,4919)
)
fakedata_plot = data.frame(
  ID = as.factor(rep(fakedata$ID,2)),
  Frame = c(fakedata$Total-fakedata$Event,fakedata$Event),
  flag = rep(c("A","B"),each=16)
)
library(ggplot2)
library(RColorBrewer)
ggplot(fakedata_plot,aes(x=ID,y=Frame,fill=flag)) + geom_col() + 
  geom_hline(yintercept=2000, color = "yellow", linewidth = 1, lty = 4) +
  scale_fill_brewer(palette = "Set1") + theme_minimal()
