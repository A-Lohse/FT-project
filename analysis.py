# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 11:22:36 2020

@author: august
"""

import pickle
import matplotlib.pyplot as plt
import os
import numpy as np
import statsmodels.formula.api as smf
import pandas as pd
import seaborn as sns


#read in data
#os.chdir("C:\\Users\\augus\\OneDrive - Københavns Universitet\\Documents\\Uni\\Kandidat i Statskundskab\\4. semester kandidat\\Projekt\\FT-project")
os.chdir("C:\\Users\\August\\OneDrive - Københavns Universitet\Documents\\Uni\\Kandidat i Statskundskab\\4. semester kandidat\\Projekt\\FT-project")
pkl_file = open('final_df.pkl', 'rb')
clean_df = pickle.load(pkl_file)
pkl_file.close()



table_tex = []
#add a year variable
clean_df['year'] = [int(clean_df.loc[i,"DateOfSitting"][0:4]) for i in range(0,len(clean_df))]
#clean_df = pd.read_csv("df_sentiment.csv",encoding = "cp1252")
#################################### no grouping - each oberservaition on its own #######################################

#make some plots

#make chi squared for amount of male speaces 
from scipy.stats import chisquare
women = len(clean_df[clean_df['gender'] == 1]['full_name'].unique())
women_speech = len(clean_df[clean_df['gender'] == 1]['second'])
men = len(clean_df[clean_df['gender'] == 0]['full_name'].unique())
men_speech = len(clean_df[clean_df['gender'] == 0]['second'])


women_exp_per = women /(men+women)
men_exp_per = men /(men+women)

women_exp_freq = women_exp_per * (women_speech+men_speech)
men_exp_freq = men_exp_per * (women_speech+men_speech)

chisquare(f_obs= [men_speech,women_speech],f_exp = [women_exp_freq, men_exp_freq]) 
########################### sentida verificatoin 

middle = round(len(clean_df)/2)
up = middle - 5
down = middle  + 5
sent_middle = clean_df.sort_values(by = "sentiment_mean", axis = 0)[up:down]
sent_min = clean_df.nsmallest(10,"sentiment_mean")
sent_max = clean_df.nlargest(10,"sentiment_mean")

sent_middle['position'] = 1
sent_max['position'] = 2
sent_min['position'] = 0


sent_df = pd.concat([sent_middle,sent_min,sent_max])
sent_df = sent_df.sample(30)
sent_df.to_csv("sentiment_verification.csv",sep = ";", encoding=("ANSI"))

sent_df_veri = pd.read_csv("sentiment_verification_coded.csv", sep = ";", encoding=("ANSI"), index_col=("old_index"))

verification_df = sent_df.merge(sent_df_veri,  how= "inner", left_index= True, right_index=True)

for row in verification_df:
    print(row)
verification_df['correct'] = [1 if row['position'] == row['coded_position'] else 0 for i, row in verification_df.iterrows()]
overall_mean = verification_df['correct'].mean()
min_mean = verification_df.loc[verification_df['position'] == 0, 'correct'].mean()
mean_mean = verification_df.loc[verification_df['position'] == 1, 'correct'].mean()
max_mean = verification_df.loc[verification_df['position'] == 2, 'correct'].mean()


print("The overall accuracy is", overall_mean, 
      "\n The accuracy of the lowest sentiment is", min_mean,
      "\n The accuracy of the middle sentiment is", mean_mean,
      "\n The accuracy of the highest sentiment is", max_mean)
verification_df.to_csv("sentiment_verification_with_code.csv",sep = ";", encoding=("ANSI"),decimal=".")

##########################3 done

#make a historgram of all speeches  
sns.set_style("whitegrid",{'axes.grid' : False})
#sns.distplot(clean_df['second'],bins = 91)
#plt.hist(clean_df['second'], bins = 91,color = "tab:blue",  edgecolor='tab:blue', linewidth=2,histtype = "step",fill = True, alpha = 0.3)
plt.hist(clean_df['second'], bins = 91,color = "tab:blue",  edgecolor='tab:blue', linewidth=2,histtype = "step")
plt.xlim(0,90)
plt.ylim(0, 5000)
plt.ylabel("Antal")
plt.title("Fordeling af taletid på alle taler i data")
plt.xlabel("Talelængde i sekunder")
plt.savefig("plots\\minutes_hist.png")
plt.show()


#group by gender and plot wpm 

women = clean_df.loc[clean_df['gender'] == 1, ['full_name','words_per_min', 'minutes','mean_minutes','mean_wpm','second']]
men = clean_df.loc[clean_df['gender'] == 0, ['full_name','words_per_min', 'minutes','mean_minutes','mean_wpm','second']]


#group by gender an
sns.set_style("whitegrid",{'axes.grid' : False})
plt.hist(men['second'], label = "Mænd",alpha = 1,bins = 91, color = "tab:blue",edgecolor='tab:blue', linewidth=2,histtype = "step")
plt.hist(women['second'], label = "Kvinder", alpha = 1,bins = 90, color = "tab:red",edgecolor='tab:red', linewidth=2,histtype = "step")
plt.ylabel("Antal")
plt.xlabel("Talelængde i sekunder")
plt.title("Taletid fordelt på køn")
plt.ylim(0, 3200)
plt.xlim(0,90)
plt.legend()
plt.savefig("plots\\minutes_seconds_gender.png")
plt.show()

#plt.grid()
sns.set_style("whitegrid")
sns.barplot(y="second", x="gender", data=clean_df, palette = ["tab:blue","tab:red"],ci=None)
plt.ylabel("Sekunder")
plt.xlabel("Køn")
plt.ylim(40,50)
plt.xticks(ticks = [0,1],labels = ["Mænd", "Kvinder"])
plt.annotate(round(clean_df[clean_df['gender'] == 0]['second'].mean(),3),(0,45),color = "white",ha="center")
plt.annotate(round(clean_df[clean_df['gender'] == 1]['second'].mean(),3),(1,45),color = "white",ha="center")
plt.title("Gennemsnitlig taletid fordelt på køn")
plt.savefig("plots\\mean_gender_seconds_bar.png")
plt.show()

sns.boxplot(y="second", x="gender", data=clean_df, palette = ["tab:blue","tab:red"])
plt.ylabel("Sekunder")
plt.xlabel("Køn")
plt.ylim(0,100)
plt.xticks(ticks = [0,1],labels = ["Mænd", "Kvinder"])
plt.title("Fordeling af taletid fordelt på køn")
plt.savefig("plots\\box_gender_seconds.png")
plt.show()

### do some summurary stats
print(women.describe())
print(men.describe())


#scatter - with gender


###############do some regressions 

x = np.array(clean_df.loc[:,'gender']).reshape(-1,1)
y = np.array(clean_df.loc[:,'minutes']).reshape(-1,1)


#gender = x
#minutes = y


#with statsmodel 
model1 = smf.ols(formula = 'second ~ gender',data = clean_df).fit()
print(model1.summary())
table_tex.append(model1.summary().as_latex())

model2 = smf.ols(formula = 'second ~ gender + mean_wpm',data = clean_df).fit()
print(model2.summary())
table_tex.append(model2.summary().as_latex())

#lets also control for the year (to control for time variate effects)
model3 = smf.ols(formula = 'second ~ gender + mean_wpm + year',data = clean_df).fit()
print(model3.summary())
table_tex.append(model3.summary().as_latex())


stargazer = Stargazer([model1,model2,model3])
stargazer.title("Regressioner med taletid og kontroller")
stargazer.custom_columns(['Model 1', 'Model 2','Model 3'],[1,1,1,])
stargazer.show_model_numbers(False)
stargazer.significant_digits(2)
stargazer.covariate_order(['gender', 'mean_wpm'])
stargazer.render_latex()

#try to print nice results
#logit_model = sm.GLM(gender,sm.add_constant(minutes),family=sm.families.Binomial())
#logit_model= sm.Logit(endog = x, exog = y)
#result=logit_model.fit()
#print(result.summary())


######### grouoped by politicians full_name  #######################################




#lets try to make a lin reg line as well
grouped_df = clean_df.groupby(['full_name'])[['mean_minutes','mean_wpm','gender']].describe()
#acces this object with at tuple eg: grouped_df.loc[:,('mean_minutes','mean')]

#acces this object with at tuple eg: grouped_df.loc[:,('mean_minutes','mean')]
x1 = grouped_df.loc[grouped_df[('gender','mean')]==1,('mean_minutes','mean')]
y1 = grouped_df.loc[grouped_df[('gender','mean')]==1,('mean_wpm','mean')]

x2 = grouped_df.loc[grouped_df[('gender','mean')]==0,('mean_minutes','mean')]
y2 = grouped_df.loc[grouped_df[('gender','mean')]==0,('mean_wpm','mean')]







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

################# mean minutes 
#with statsmodel 
#do minutes depend on gender
model = smf.ols(formula = 'mean_minutes ~ gender',data = clean_df).fit()
print(model.summary())
table_tex.append(model.summary().as_latex())

#what if i control for personal mean wpm
model = smf.ols(formula = 'mean_minutes ~ gender + mean_wpm',data = clean_df).fit()
print(model.summary())
table_tex.append(model.summary().as_latex())

#lets also control for the year (to control for time variate effects)
model = smf.ols(formula = 'mean_minutes ~ gender + mean_wpm + year',data = clean_df).fit()
print(model.summary())
table_tex.append(model.summary().as_latex())


#try to print nice results
#logit_model = sm.GLM(minutes,sm.add_constant(gender),family=sm.families.Binomial())
#try to print nice results
#result=logit_model.fit()
#print(result.summary())
#seems to be significant. 

#lets plot this logit reg
#plt.scatter(x,model.predict_proba(x)[:,1])
#plt.scatter(y,x,c = grouped_df.loc[:,('gender','mean')], alpha = 0.5)
#plt.ylabel("Gender, 1 = Female, 0 = Male")
#plt.xlabel("Average minutes speaking")

#plt.show()

############################## look at words instead of minutes 


model = smf.ols(formula = 'words ~ gender',data = clean_df).fit()
print(model.summary())
table_tex.append(model.summary().as_latex())

#lets also control for the year (to control for time variate effects)
model = smf.ols(formula = 'words ~ gender + year',data = clean_df).fit()
print(model.summary())
table_tex.append(model.summary().as_latex())

sns.set_style("whitegrid")
sns.barplot(y="words", x="gender", data=clean_df, palette = ["tab:blue","tab:red"],ci=None)
plt.ylabel("Ord")
plt.xlabel("Køn")
plt.ylim(130,140)
plt.xticks(ticks = [0,1],labels = ["Mænd", "Kvinder"])
plt.annotate(round(clean_df[clean_df['gender'] == 0]['words'].mean(),3),(0,135),color = "white",ha="center")
plt.annotate(round(clean_df[clean_df['gender'] == 1]['words'].mean(),3),(1,135),color = "white",ha="center")
plt.title("Gennemsnitligt antal ord fordelt på køn")
plt.savefig("plots\\mean_gender_word_bar.png")
plt.show()

sns.boxplot(y="words", x="gender", data=clean_df, palette = ["tab:blue","tab:red"])
plt.ylabel("Ord")
plt.xlabel("Køn")
plt.ylim(0,450)
plt.xticks(ticks = [0,1],labels = ["Mænd", "Kvinder"])
plt.title("Antal ord fordelt på køn")
plt.savefig("plots\\box_gender_words.png")
plt.show()






########################## Sentiment analysis 


women = clean_df.loc[clean_df['gender'] == 1, ['sentiment_mean']]
men = clean_df.loc[clean_df['gender'] == 0, ['sentiment_mean']]

#distribution 
sns.set_style("whitegrid",{'axes.grid' : False})
plt.hist(men['sentiment_mean'], label = "Mænd",alpha = 1,bins = 300, color = "tab:blue",edgecolor='tab:blue', linewidth=2,histtype = "step")
plt.hist(women['sentiment_mean'], label = "Kvinder",alpha = 1,bins = 300, color = "tab:red",edgecolor='tab:red', linewidth=2,histtype = "step")
plt.ylabel("Antal")
plt.xlabel("Sentiment score")
plt.title("Sentiment score fordelt på talers køn")
plt.xlim(-5,5)
plt.legend()
plt.savefig("plots\\sentiment_gender.png")
plt.show()


#barplot 
sns.set_style("whitegrid")
sns.barplot(y="sentiment_mean", x="gender", data=clean_df, palette = ["tab:blue","tab:red"],ci=None)
plt.ylabel("Mean sentiment")
plt.xlabel("Talers køn")
plt.ylim(0.2,0.4)
plt.xticks(ticks = [0,1],labels = ["Mænd", "Kvinder"])
plt.annotate(round(clean_df[clean_df['gender'] == 0]['sentiment_mean'].mean(),3),(0,0.27),color = "white",ha="center")
plt.annotate(round(clean_df[clean_df['gender'] == 1]['sentiment_mean'].mean(),3),(1,0.27),color = "white",ha="center")
plt.title("Gennemsnitlig sentiment fordelt på talers køn")
plt.savefig("plots\\mean_gender_sentiment_bar.png")
plt.show()


#####



#target 

#distribution 
sns.set_style("whitegrid",{'axes.grid' : False})
plt.hist(clean_df.loc[clean_df['target'] == 0, ['sentiment_mean']]['sentiment_mean'], label = "Tiltalt mand",alpha = 1,bins = 300,color = "tab:blue",edgecolor='tab:blue', linewidth=2,histtype = "step")
plt.hist(clean_df.loc[clean_df['target'] == 1, ['sentiment_mean']]['sentiment_mean'], label = "Tiltalt kvinde",alpha = 1,bins = 300,color = "tab:red",edgecolor='tab:red', linewidth=2,histtype = "step")
plt.ylabel("Antal")
plt.xlabel("Sentiment score")
plt.title("Sentiment score fordelt tiltaltes køn")
plt.xlim(-5,5)
plt.legend()
plt.savefig("plots\\sentiment_target_gender.png")
plt.show()


#barplot 
sns.set_style("whitegrid")
sns.barplot(y="sentiment_mean", x="target", data=clean_df, palette = ["tab:blue","tab:red"],ci=None)
plt.ylabel("Gennemsnitlig sentiment")
plt.xlabel("Tiltaltes køn")
plt.xlim(-0.5,1.5)
plt.ylim(0.2,0.4)
plt.xticks(ticks = [0,1],labels = ["Mænd", "Kvinder"])
plt.annotate(round(clean_df[clean_df['target'] == 0]['sentiment_mean'].mean(),3),(0,0.3),color = "white",ha="center")
plt.annotate(round(clean_df[clean_df['target'] == 1]['sentiment_mean'].mean(),3),(1,0.3),color = "white",ha="center")
plt.title("Gennemsnitlig sentiment fordelt på tiltaltes køn")
plt.savefig("plots\\mean_target_sentiment_bar.png")
plt.show()



#both targets and gender 



#target men
clean_df.loc[clean_df['target'] == 0, ['sentiment_mean']]['sentiment_mean'].mean()
#target women
clean_df.loc[clean_df['target'] == 1, ['sentiment_mean']]['sentiment_mean'].mean()





model = smf.ols(formula = 'sentiment_mean ~ gender',data = clean_df).fit()
print(model.summary())
table_tex.append(model.summary().as_latex())


clean_df.loc[clean_df['target'] == 2,'target'] = np.nan
model = smf.ols(formula = 'sentiment_mean ~ target' ,data = clean_df).fit()
print(model.summary())
table_tex.append(model.summary().as_latex())


model = smf.ols(formula = 'sentiment_mean ~ target + gender',data = clean_df).fit()
print(model.summary())
table_tex.append(model.summary().as_latex())

model = smf.ols(formula = 'sentiment_mean ~ target + gender + year',data = clean_df).fit()
print(model.summary())
table_tex.append(model.summary().as_latex()) 

model = smf.ols(formula = 'sentiment_mean ~ target*gender + year',data = clean_df).fit()
print(model.summary())
table_tex.append(model.summary().as_latex()) 
#chaning for sake of labels
#data['target'] = data['target'].replace(to_replace=0, value="Male")
#data['target'] = data['target'].replace(to_replace=1, value="Female")
clean_df[clean_df['target'] == 2] = np.nan


sns.set_style("whitegrid")
sns.barplot(y="sentiment_mean", x="gender", hue = "target", data=clean_df,palette = ["tab:blue","tab:red"],ci=None)
plt.ylabel("Gennemsnitlig sentiment")
plt.xlabel("Tiltaltes køn")
plt.xlim(-0.5,1.5)
plt.ylim(0.2,0.4)
plt.xticks(ticks = [0,1],labels = ["Mænd", "Kvinder"])
plt.annotate(round(clean_df.loc[(clean_df['target'] == 0) & (clean_df['gender'] == 0),'sentiment_mean'].mean(),3),(-0.2,0.3),color = "white",ha="center")
plt.annotate(round(clean_df.loc[(clean_df['target'] == 1) & (clean_df['gender'] == 0),'sentiment_mean'].mean(),3),(0.2,0.3),color = "white",ha="center")
plt.annotate(round(clean_df.loc[(clean_df['target'] == 0) & (clean_df['gender'] == 1),'sentiment_mean'].mean(),3),(0.8,0.3),color = "white",ha="center")
plt.annotate(round(clean_df.loc[(clean_df['target'] == 1) & (clean_df['gender'] == 1),'sentiment_mean'].mean(),3),(1.2,0.3),color = "white",ha="center")
plt.legend(loc ='upper right',labels = ["Mand","kvinde"],title = "Tiltaltes køn")
plt.title("Gennemsnitlig sentiment og køn")
plt.savefig("plots\\sentiment_target_gender_allthethings.png")
plt.show()




for i,table in enumerate(table_tex):
    file = "textables\\"  + str(i) + "table.txt"
    #print(file)
    with open(file, 'w') as f:
        f.write(table)
