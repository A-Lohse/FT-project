# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 12:13:16 2020

@author: august
"""
######################################################### TO-Do list
#Items to fix

######################################################### importing packages
import pickle
import pandas as pd
import os
import numpy as np
import sys

########################################################read in data
os.chdir("C:\\Users\\augus\\OneDrive - Københavns Universitet\\Documents\\Uni\\Kandidat i Statskundskab\\4. semester kandidat\\Projekt\\FT-project")

#os.chdir("C:\\Users\\August\\OneDrive - Københavns Universitet\Documents\\Uni\\Kandidat i Statskundskab\\4. semester kandidat\\Projekt\\FT-project")

############################### Run R script first
R = True
if not R:
    print("The R variable is set to False. If this is the first time you run the code, you should run the r script called 'sentida.R' first. This will generate the sentiments analysis. Afterwards set the R variable to True")
    sys.exit()    
pkl_file = open('full_df.pkl', 'rb')
full_df = pickle.load(pkl_file)
pkl_file.close()


#data is now a pandas dataframe

############################################## removing any speech made by "formand or any supstitute of these"
speaker_df = full_df[(full_df['OratorRole'] != "formand") &
                     (full_df['OratorRole'] != "midlertidig formand") &
                     (full_df['OratorRole'] != "Pause") & 
                     (full_df['OratorRole'] != "MødeSlut") & 
                     (full_df['OratorRole'] != "aldersformanden")]

speaker_df['OratorRole'].unique()
print("NAs before clean", speaker_df.isna().any())

###################################################### Remove NAs / doing something about them
#the 530 with "None" in the name and tile etc. are all statements saying that questions has been taken of the agenda.
## It has no author and is therefore delete

#start by reseting the index
speaker_df =  speaker_df.reset_index(drop=True)  
#get the missing indicies
indicies = speaker_df[speaker_df['OratorFirstName'].isna()].index
#drtop the rows 
speaker_df.drop(indicies,axis = 0,inplace = True)
#check to make sure that is was the same rows that was removed (the same 530)
speaker_df.isna().any()
#it sure was 

#some speeches were not done being recorded at the time om scraping, so they are "under construction" 
# i delete these (1 speech - 25 people talking )
speaker_df =  speaker_df.reset_index(drop=True)  
indicies = speaker_df[speaker_df['tale'] == "(Talen er under udarbejdelse)"].index
speaker_df.drop(indicies,axis = 0,inplace = True)
 




print("NAs after clean", speaker_df.isna().any())


############################################################ renaming 
speaker_df = speaker_df.rename(columns = {"GroupNameShort": "first_name", "OratorFirstName": "last_name", "OratorLastName":"party"})

############################################################ making a full name varaible

speaker_df['full_name'] = speaker_df.apply(lambda row: row.first_name + " " + row.last_name, axis = 1) 

#making a list of all the people so that i can handcode the party and gender 
##people = speaker_df['full_name'].unique()
##people = pd.Series(people)
##people.to_csv("politikere.csv",sep = ";", index = False, encoding=("ANSI"))

########################################################### making a list of the ministers without parties

#ministers = speaker_df['full_name'][speaker_df['party'].isnull()].unique()
#ministers = pd.Series(ministers)
#ministers.to_csv("ministers.csv",sep = ";", index = False, encoding=("ANSI"))

############################################################# adding parties and gender back in 
ministere = pd.read_csv("ministers.csv",encoding=("ANSI"), sep = ";")
politikere = pd.read_csv("politikere.csv",encoding=("ANSI"), sep = ";")


######################## parties

#reset index
speaker_df =  speaker_df.reset_index(drop=True) 

#for each row in the data set
for i in range(len(speaker_df)):
    #if the party is missing
    if speaker_df['party'][i] is None:
        #what is the name - assign
        name = speaker_df['full_name'][i]
        
        #if the name is of Astrid krag, make an exeption (she has beenn minister for two different parties)
        if name == "Astrid Krag":
            #if we are after 2015 assign "S"
            if int(speaker_df['ParliamentarySession'][i]) > 20151:
                   speaker_df['party'][i] = "S"
            #ekse assign "SF
            else:
                speaker_df['party'][i] = "SF"   
        #If it is any other minister - assign the party descirbed in the ministere dataframe
        else: 
            speaker_df['party'][i] = list(ministere['party_1'][ministere['full_name']==name])[0]


## list in excel ark  - correct all the names


##################### gender
#i assign gender manually an then import the gender data, and assign it to the dataframe (each obs)
for i in politikere.index:
    #print(i)
    name = politikere['full_name'][i]
    gender = politikere['gender'][i]
    #print(name,gender)
    speaker_df.loc[speaker_df['full_name']==name,'gender'] = gender

#print("NAs after clean", speaker_df.isna().any())

#############  correct names 
## some of the names are doublicates 
old_names = ["Flemming Møller",
             "Ane Halsboe-Jørgensen",
             "Kaare Dybvad",
             "Marlene B. Lorentzen",
             "Peter Hummelgaard",
             "Peter Juel Jensen",
             "Peter Kofod",            
             "Simon Emil Ammitzbøll"]

new_names = ["Flemming Møller Mortensen",
             "Ane Halsboe-Larsen",
             "Kaare Dybvad Bek",
             "Marlene Borst Hansen",
             "Peter Hummelgaard Thomsen",
             "Peter Juel-Jensen",
             "Peter Kofod Poulsen",
             "Simon Emil Ammitzbøll-Bille"]

for i, name in enumerate(old_names):
    speaker_df.loc[speaker_df['full_name']==name,'full_name'] = new_names[i]
    
    
###############################################Add timestamps and minutes etc.
import datetime as dt
speaker_df =  speaker_df.reset_index(drop=True) 

# test if dates times stamps are correct
#start = dt.datetime.strptime(speaker_df['start'][0],"%Y-%m-%dT%H:%M:%S")
#end = dt.datetime.strptime(speaker_df['end'][0],"%Y-%m-%dT%H:%M:%S")
#time = end - start

#speaker_df['start'][0]
#speaker_df['end'][0]

# add timestamps
speaker_df['second'] = speaker_df.apply(lambda row: dt.datetime.strptime(row.end,"%Y-%m-%dT%H:%M:%S") - 
                                  dt.datetime.strptime(row.start,"%Y-%m-%dT%H:%M:%S"), axis = 1)

#convert to seconds
speaker_df['second'] = speaker_df.apply(lambda row: row.second.total_seconds(), axis = 1)

#convert to minutes
#
speaker_df['minutes'] = speaker_df['second'] / 60


##########################################make words per minute variable and a word count variable 

#count - removing trailing whitespace with strip, and then counting the number of splits on " "
speaker_df['words'] = speaker_df.apply(lambda row: len(row['tale'].strip().split(" ")), axis =1 )

#make a func to count words per min because some speaces are 0 min / and 0 sec there fore we need a try statement
def word_pm(word,minutes = 0, alpha = False):
    if alpha:
        try:
            x = len(word) / 5
        except:
            x = 0
    else:
        try:
            x = word/ minutes 
        except: 
            x = 0
    return x
speaker_df['words_per_min']= np.nan
speaker_df['words_per_min_alphanumeric'] = np.nan
#assign the values
for i in range(len(speaker_df)):
    if speaker_df['minutes'][i] == 0:
         speaker_df['words_per_min'][i] = 0
         speaker_df['words_per_min_alphanumeric'] = 0
    else:
        speaker_df['words_per_min'][i] = word_pm(speaker_df['words'][i],speaker_df['minutes'][i])
        speaker_df['words_per_min_alphanumeric'][i] = word_pm(speaker_df['tale'][i], alpha = True)

############################################### clean word per min for bad data (more than 1000 word per minute? maybe more)

#there are some very extreme values that i now sift out- some of them at least is due to human error in data set - 
# i have checked manually 
# world record seems to be 637 wpm - maybe cut it there
# soruce https://virtualspeech.com/blog/average-speaking-rate-words-per-minute
ind = speaker_df[speaker_df['words_per_min'] > 627].index

speaker_df['words_per_min'][ind] = np.nan
speaker_df['words_per_min_alphanumeric'][ind] = np.nan



############################################### group by politician and calculate mean wpm and minutes talked
grouped_df_minutes = speaker_df.groupby(['full_name'])['minutes'].describe()
grouped_df_wpm = speaker_df.groupby(['full_name'])['words_per_min'].describe()


speaker_df['mean_minutes'] = np.nan
speaker_df['mean_wpm'] = np.nan

for i in range(len(speaker_df)):
   speaker_df['mean_minutes'][i] = grouped_df_minutes[grouped_df_minutes.index==speaker_df['full_name'][i]]['mean']
for i in range(len(speaker_df)):
    speaker_df['mean_wpm'][i] = grouped_df_wpm[grouped_df_minutes.index==speaker_df['full_name'][i]]['mean']


sent_df = pd.read_csv("df_sentiment.csv",encoding = "cp1252")

grouped_df_sentiment = sent_df.groupby(['full_name'])['sentiment_mean'].describe()
grouped_df_sentiment_total = sent_df.groupby(['full_name'])['sentiment_total'].describe()

sent_df['mean_personal_sentiment'] = np.nan
sent_df['mean_total_personal_sentiment'] = np.nan

for i in range(len(sent_df)):
   sent_df['mean_personal_sentiment'][i] = grouped_df_sentiment[grouped_df_sentiment.index==sent_df['full_name'][i]]['mean']
for i in range(len(sent_df)):
   sent_df['mean_total_personal_sentiment'][i] = grouped_df_sentiment_total[grouped_df_sentiment_total.index==sent_df['full_name'][i]]['mean']

speaker_df['mean_personal_sentiment'] = sent_df['mean_personal_sentiment']
speaker_df['mean_total_personal_sentiment']= sent_df['mean_total_personal_sentiment']
speaker_df['sentiment_mean'] = sent_df['sentiment_mean']
speaker_df['sentiment_total'] = sent_df['sentiment_total']



#add targets of tale 
# add indicator for who the text is towards 
speaker_df['target'] = np.nan
for i in range(len(speaker_df)):
    text = speaker_df['tale'][i].lower().replace("hr. formand","")
    text = text.replace("hr formand","")
    text = text.replace("fru formand","")
    text = text.replace("fru. formand","")

    if "fru " in speaker_df['tale'][i].lower() and "hr." not in speaker_df['tale'][i].lower():
        speaker_df['target'][i] = 1
    elif "hr." in speaker_df['tale'][i].lower() and "fru " not in speaker_df['tale'][i].lower():
        speaker_df['target'][i] = 0
    else:
        speaker_df['target'][i] = 2

#make new datasets
makenew = True
if not makenew:
    print("The make new argument is set to false. This means that the code does not overwrite the data in directory. Do you want to generate new data? then set the argument to True" )
if makenew:
    
    speaker_df.to_csv("final_df.csv")
#############################################save dataset
    file_name = "final_df.pkl"
    output = open(file_name, 'wb')
    pickle.dump(speaker_df, output)
    output.close()

print("All done")