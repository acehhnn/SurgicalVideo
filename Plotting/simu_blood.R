nonblood = read.csv("D:\\THU\\3spring\\_denglab\\learning\\fakeblood_test\\xml_2\\nonblood.csv", header = T)
blood = read.csv("D:\\THU\\3spring\\_denglab\\learning\\fakeblood_test\\xml_2\\blood.csv",header = T)
nonblood = nonblood[,2:5]
blood = blood[,2:5]

nonblood = nonblood[sample(nrow(nonblood), nrow(blood), replace = F),]

summary(blood$R)
summary(nonblood$R)

summary(blood$G)
summary(blood$B)
summary(blood$Gray)

sum(blood$Gray==0) # 0
sum(blood$R==0) # 0
sum(blood$G==0) # 0
sum(blood$B==0) # 507

blood$B = ifelse(blood$B==0,.1,blood$B)

sum(nonblood$Gray==0) # 4
sum(nonblood$R==0) # 4
sum(nonblood$G==0) # 11
sum(nonblood$B==0) # 13

nonblood$Gray = ifelse(nonblood$Gray==0,0.1,nonblood$Gray)
nonblood$R = ifelse(nonblood$R==0,0.1,nonblood$R)
nonblood$G = ifelse(nonblood$G==0,0.1,nonblood$G)
nonblood$B = ifelse(nonblood$B==0,0.1,nonblood$B)

boxplot(blood$B,nonblood$B, names = c("Blood", "Nonblood"), main = "Blue")
t.test(blood$B,nonblood$B) # 2.2e-16
boxplot(blood$G,nonblood$G, names = c("Blood", "Nonblood"), main = "Green")
t.test(blood$G,nonblood$G) # 2.2e-16
boxplot(blood$R,nonblood$R, names = c("Blood", "Nonblood"), main = "Red")
t.test(blood$R,nonblood$R) # 2.2e-16
boxplot(blood$Gray,nonblood$Gray, names = c("Blood", "Nonblood"), main = "Gray")
t.test(blood$Gray,nonblood$Gray) # 2.2e-16
summary(nonblood$B/nonblood$Gray)

boxplot(blood$Gray/blood$B,nonblood$Gray/nonblood$B, 
        names = c("Blood", "Nonblood"), main = "Gray / Blue")
summary(blood$Gray/blood$B)
summary(nonblood$Gray/nonblood$B)
boxplot(blood$Gray/blood$G,nonblood$Gray/nonblood$G, 
        names = c("Blood", "Nonblood"), main = "Gray / Green")
boxplot(blood$Gray/blood$R,nonblood$Gray/nonblood$R,
        names = c("Blood", "Nonblood"), main = "Gray / Red")

boxplot(blood$B/blood$Gray,nonblood$B/nonblood$Gray)
boxplot(blood$G/blood$Gray,nonblood$G/nonblood$Gray)
boxplot(blood$R/blood$Gray,nonblood$R/nonblood$Gray)

boxplot(blood$G/blood$B,nonblood$G/nonblood$B)
boxplot(blood$G/blood$R,nonblood$G/nonblood$R)
boxplot(blood$R/blood$B,nonblood$R/nonblood$B)
summary(blood$B/blood$R)
summary(nonblood$B/nonblood$R)


