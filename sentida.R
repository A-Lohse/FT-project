#if(!require("devtools")) install.packages("devtools")
#install.packages("glue")
#devtools::install_github("Guscode/Sentida")

library(Sentida)
library(openxlsx)
library(svMisc)
setwd("C:\\Users\\August\\OneDrive - Københavns Universitet\\Documents\\Uni\\Kandidat i Statskundskab\\4. semester kandidat\\Projekt\\FT-project")

Sentida::sentida("Abort er mord", output = "mean")
sentida("Abort er mord", output = "total")
sentida("Abort er mord", output = "mean")

df <- read.csv("full_df.csv", encoding = "UTF-8")


df$sentiment_mean = Sentida::sentida(df$tale,output = "mean")
df$sentiment_total = Sentida::sentida(df$tale,output = "total")


for( i in 1:nrow(df)){
  progress(i,nrow(df))
  df$sentiment_mean[i] <- Sentida::sentida(df$tale[i],output = "mean")
  df$sentiment_total[i] <- Sentida::sentida(df$tale[i],output = "total")
}
write.csv(df,"df_sentiment.csv")
