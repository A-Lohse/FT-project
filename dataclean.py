# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 12:13:16 2020

@author: august
"""
######################################################### TO-Do list
#Items to fix
#  - name and party variables should be renamed. 
# missing values on party affiliation are due to the person being a minister - assign party (around 44k obs)
# add gender 
    # i do this by making a full list of full name (unique) and manually add gender by their name. 
    # this way i can also add party if they are ministers 
    
    
######################################################### importing packages
import pickle
import pandas as pd
import os
import matplotlib.pyplot as plt


########################################################read in data
os.chdir("C:\\Users\\August\\OneDrive - Københavns Universitet\Documents\\Uni\\Kandidat i Statskundskab\\4. semester kandidat\\Projekt\\FT-project")
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

#############  correct names 

## list in excel ark  - correct all the names


##################### gender




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



############################################### check for name duplicates in data (where for example middle name is missing)

#############################################save dataset
file_name = "clean_df.pkl"
output = open(file_name, 'wb')
pickle.dump(speaker_df, output)
output.close()