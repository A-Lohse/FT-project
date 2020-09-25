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
os.chdir("C:\\Users\\August\\OneDrive - Københavns Universitet\Documents\\Uni\\Kandidat i Statskundskab\\4. semester kandidat\\Projekt\\FT-project")
pkl_file = open('clean_df.pkl', 'rb')
clean_df = pickle.load(pkl_file)
pkl_file.close()


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


### calculate mean of individual parlamentary member

#grouped_df_minutes = clean_df.groupby(['full_name'])['minutes'].describe()
#grouped_df_wpm = clean_df.groupby(['full_name'])['words_per_min'].describe()


#clean_df['mean_minutes'] = np.nan
#clean_df['mean_wpm'] = np.nan

#for i in range(len(clean_df)):
#    clean_df['mean_minutes'][i] = grouped_df_minutes[grouped_df_minutes.index==clean_df['full_name'][i]]['mean']
#for i in range(len(clean_df)):
#    clean_df['mean_wpm'][i] = grouped_df_minutes[grouped_df_minutes.index==clean_df['full_name'][i]]['mean']


mean_minutes = clean_df['mean_minutes'].unique()
mean_wpm = clean_df['mean_wpm'].unique()

print("the mean minutes of the MF grouped means is", np.mean(mean_minutes))
print("the mean wpm of the MF grouped means is", np.mean(mean_wpm))

### make some histograms 
#minutes
plt.hist(mean_minutes,bins= 50)
plt.xlabel("Means of politicans minutes")
plt.ylabel("count")
plt.title("Distribution of the means of politicians minutes spoken")
plt.show()

#wmp
plt.hist(mean_wpm,bins= 50)
plt.xlabel("Means of politicans wpm")
plt.ylabel("count")
plt.title("Distribution of the means of politicians words per minute")
plt.show()


#scatter - with gender


#lets try to make a lin reg line as well
grouped_df = clean_df.groupby(['full_name'])[['mean_minutes','mean_wpm','gender']].describe()
#acces this object with at tuple eg: grouped_df.loc[:,('mean_minutes','mean')]



#acces this object with at tuple eg: grouped_df.loc[:,('mean_minutes','mean')]
x1 = grouped_df.loc[grouped_df[('gender','mean')]==1,('mean_minutes','mean')]
y1 = grouped_df.loc[grouped_df[('gender','mean')]==1,('mean_wpm','mean')]

x2 = grouped_df.loc[grouped_df[('gender','mean')]==0,('mean_minutes','mean')]
y2 = grouped_df.loc[grouped_df[('gender','mean')]==0,('mean_wpm','mean')]

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
model = LinearRegression().fit(x, y)

#
r_sq = model.score(x, y)
print('coefficient of determination:', r_sq)

print('intercept:', model.intercept_)
print('slope:', model.coef_)

#there does not seem to be a strong correlation with lin reg - try logit 
#switch around y and x for logit reg on dummy var (gender)


model = LogisticRegression().fit(y, x)
r_sq = model.score(y, x)

#print the results
print('coefficient of determination:', r_sq)
print('slope:', model.coef_)

#a small bit better than random (0.5)


#try to print nice results
logit_model= sm.Logit(endog = x, exog = y)
result=logit_model.fit()
print(result.summary())
#seems to be significant. 

#lets plot this logit reg
#plt.scatter(x,model.predict_proba(x)[:,1])
plt.scatter(y,x,c = grouped_df.loc[:,('gender','mean')], cmap = "RdYlGn", alpha = 0.5)
plt.ylabel("Gender, 1 = Female, 0 = Male")
plt.xlabel("Average minutes speaking")

plt.show()


