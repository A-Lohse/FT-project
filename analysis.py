# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 11:22:36 2020

@author: augus
"""

import pickle
import matplotlib.pyplot as plt
import os
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
import statsmodels.api as sm
import pandas as pd


#read in data
os.chdir("C:\\Users\\augus\\OneDrive - Københavns Universitet\\Documents\\Uni\\Kandidat i Statskundskab\\4. semester kandidat\\Projekt\\FT-project")
#os.chdir("C:\\Users\\August\\OneDrive - Københavns Universitet\Documents\\Uni\\Kandidat i Statskundskab\\4. semester kandidat\\Projekt\\FT-project")
pkl_file = open('full_df.pkl', 'rb')
clean_df = pickle.load(pkl_file)
pkl_file.close()


#clean_df = pd.read_csv("df_sentiment.csv",encoding = "cp1252")
#################################### no grouping - each oberservaition on its own #######################################

#make some plots

#make a historgram of all speeches under 6 min 
plt.hist(clean_df['minutes'],bins = 300)
plt.xlim(0,12)
plt.ylim(0, 50000)
plt.ylabel("Count")
plt.xlabel("Minutes of speech")
plt.show()


#make a historgram of all speeches under 6 min 
plt.hist(clean_df['words_per_min'],bins = 300)
#plt.xlim(0,12)
#plt.ylim(0, 50000)
plt.ylabel("Count")
plt.xlabel("Words per minute")
plt.show()


#group by gender and plot wpm 

women = clean_df.loc[clean_df['gender'] == 1, ['full_name','words_per_min', 'minutes','mean_minutes','mean_wpm']]
men = clean_df.loc[clean_df['gender'] == 0, ['full_name','words_per_min', 'minutes','mean_minutes','mean_wpm']]


plt.hist(men['words_per_min'], label = "Men",alpha = 0.5,bins = 300)
plt.hist(women['words_per_min'], label = "Women", alpha = 0.7,bins = 300)
plt.xlim(0, 400)
plt.ylabel("Count")
plt.xlabel("Words per minute")
plt.legend()
plt.show()

#group by gender an

plt.hist(men['minutes'], label = "Men",alpha = 0.5,bins = 500)
plt.hist(women['minutes'], label = "Women", alpha = 0.7,bins = 500)
plt.ylabel("Count")
plt.xlabel("Minutes of speech")
plt.ylim(0, 20000)
plt.xlim(0,12)
plt.legend()

plt.show()


### do some summurary stats
print(women.describe())
print(men.describe())


#scatter - with gender


###############do some regressions 

x = np.array(clean_df.loc[:,'gender']).reshape(-1,1)
y = np.array(clean_df.loc[:,'minutes']).reshape(-1,1)


gender = x
minutes = y


#with statsmodel 
model = sm.OLS(minutes, gender).fit()
print(model.summary())



#try to print nice results
logit_model = sm.GLM(gender,sm.add_constant(minutes),family=sm.families.Binomial())
#logit_model= sm.Logit(endog = x, exog = y)
result=logit_model.fit()
print(result.summary())

plt.scatter(y,x,c = clean_df.loc[:,'gender'], alpha = 0.5)
plt.ylabel("Gender, 1 = Female, 0 = Male")
plt.xlabel("Minutes speaking")

plt.show()


#################################### grouoped by politicians full_name  #######################################




#lets try to make a lin reg line as well
grouped_df = clean_df.groupby(['full_name'])[['mean_minutes','mean_wpm','gender']].describe()
#acces this object with at tuple eg: grouped_df.loc[:,('mean_minutes','mean')]

#acces this object with at tuple eg: grouped_df.loc[:,('mean_minutes','mean')]
x1 = grouped_df.loc[grouped_df[('gender','mean')]==1,('mean_minutes','mean')]
y1 = grouped_df.loc[grouped_df[('gender','mean')]==1,('mean_wpm','mean')]

x2 = grouped_df.loc[grouped_df[('gender','mean')]==0,('mean_minutes','mean')]
y2 = grouped_df.loc[grouped_df[('gender','mean')]==0,('mean_wpm','mean')]





#histogram of distribution of means og minutes between male and female 
plt.hist(x2, label = "Men",alpha = 0.5,bins = 30)
plt.hist(x1, label = "Women", alpha = 0.7,bins = 30)
plt.title("Distribution of mean minutes of speach")
plt.ylabel("Count")
plt.xlabel("Mean minutes of speech")
#plt.ylim(0, 20000)
#plt.xlim(0,12)
plt.legend()
plt.show()


#histogram of distribution of means of Wpm between male and female 
plt.hist(y2, label = "Men",alpha = 0.5,bins = 40)
plt.hist(y1, label = "Women", alpha = 0.7,bins = 40)
plt.title("Distribution of mean minutes of speach")
plt.ylabel("Count")
plt.xlabel("Mean wpm")
#plt.ylim(0, 20000)
#plt.xlim(0,12)
plt.legend()

plt.show()



#scatter plot 
plt.scatter(x1,y1, label = "Women", c = "green", alpha = 0.9)
plt.scatter(x2,y2, label = "Men", c = "red", alpha = 0.5)
plt.legend()
plt.xlabel("Mean minutes spoken for each MF")
plt.ylabel("Mean word per minute spoken for each MF")
plt.title("Mean minutes vs mean wors per minute for each MF")
plt.annotate(s = 'Women mean minutes: {}'.format(round(x1.describe()['mean'],3)), xy = (2.8,190),size = "small")
plt.annotate(s = 'Men mean minutes: {}'.format(round(x2.describe()['mean'],3)), xy = (2.8,180),size = "small")

plt.show()





#mean of men and women when grouped
print("the mean length of a woman MP's speech is:", round(x1.describe()['mean'],3),"minutes, When grouped by individual MP")
print("the mean length of a man MP's speech is:", round(x2.describe()['mean'],3),"minutes, When grouped by individual MP")
print("this is a difference of", round((x2.describe()['mean'] -x1.describe()['mean'] ),3)*60, "seconds more to men")


########################################### regressions 
#first reg parameter is gender and y is time to speak
x = np.array(grouped_df.loc[:,('gender','mean')]).reshape(-1,1)
y = np.array(grouped_df.loc[:,('mean_minutes','mean')]).reshape(-1,1)


gender = x
minutes = y


#with statsmodel 
model = sm.OLS(minutes, gender).fit()
print(model.summary())



#try to print nice results
logit_model = sm.GLM(gender,sm.add_constant(minutes),family=sm.families.Binomial())
#try to print nice results
result=logit_model.fit()
print(result.summary())
#seems to be significant. 

#lets plot this logit reg
#plt.scatter(x,model.predict_proba(x)[:,1])
plt.scatter(y,x,c = grouped_df.loc[:,('gender','mean')], alpha = 0.5)
plt.ylabel("Gender, 1 = Female, 0 = Male")
plt.xlabel("Average minutes speaking")

plt.show()


#################################### grouped by individual session  #######################################



########################## Sentiment analysis 

#### i make personal means of the mean and the total - only run once
#grouped_df_sentiment = clean_df.groupby(['full_name'])['sentiment_mean'].describe()
#grouped_df_sentiment_total = clean_df.groupby(['full_name'])['sentiment_total'].describe()

#clean_df['mean_personal_sentiment'] = np.nan
#clean_df['mean_total_personal_sentiment'] = np.nan

#for i in range(len(clean_df)):
   #clean_df['mean_personal_sentiment'][i] = grouped_df_sentiment[grouped_df_sentiment.index==clean_df['full_name'][i]]['mean']
#for i in range(len(clean_df)):
   #clean_df['mean_total_personal_sentiment'][i] = grouped_df_sentiment_total[grouped_df_sentiment_total.index==clean_df['full_name'][i]]['mean']

#clean_df.to_csv("clean.csv")

