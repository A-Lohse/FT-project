# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 11:21:37 2020

@author: august
"""

import xml.etree.ElementTree as ET
import pandas as pd
import os
import math
import numpy as np 

#set wd
os.chdir("C:\\Users\\augus\\OneDrive - Københavns Universitet\\Documents\\Uni\\Kandidat i Statskundskab\\4. semester kandidat\\Projekt\\FT-project")


documents = []
os.listdir("ODAXML\\Referat\\samling")
for i in os.listdir("ODAXML\\Referat\\samling"):
    path = "ODAXML\\Referat\\samling\\" + i
    
    for n in os.listdir(path):
        real_path = path+"\\"+n
        documents.append(real_path)



def df_func(path):
    """ This is a docstring """
        
    taler_list = []
    var_list = []
    speech_list = []
    start = []
    end = []
       
    #load the file
    tree = ET.parse(path)

    root = tree.getroot()

    
    
    for tale in root.iter('Tale'):
        #reset text list for later
        most_text = []
        start_time_list = []
        end_time_list = []
        #for each subelement in each speech - there are both metadata and the actual speech text - the first part in the metadata
        for subelem in tale:   
            #if it is "Taler"
            if subelem.tag == "Taler":
                #for each subelem in subelem
                for subsubelem in subelem:
                    #get names position etc.
                    if subsubelem.tag == "MetaSpeakerMP":
                        speaker_data = []
                        #another elem deeper
                        for subsubsubelem in subsubelem:                 
                            #print(subsubsubelem.tag,subsubsubelem.text)
                            #append the text of the varaibles
                            speaker_data.append(subsubsubelem.text)
                            #append the variable name
                            var_list.append(subsubsubelem.tag)
                        taler_list.append(speaker_data)
            #In this part i extract the extual text of the speech
            elif subelem.tag == "TaleSegment":
                #get metadata of speech 
                for start_time in subelem.iter('StartDateTime'):
                    #print("start",start_time.text)
                    start_time_list.append(start_time.text)
                for end_time in subelem.iter('EndDateTime'):
                    #print("end",end_time.text)
                    end_time_list.append(end_time.text)
                #for each piece of text in the speech (it is sometimes divied up)
                for speech in subelem.iter('Char'):
    
                    most_text.append(speech.text)
        #join all the text elements of the same speech - therefore indent matches speech level
        all_text = " ".join(most_text)
        #Append it to same list            
        speech_list.append(all_text)
        
        #append timestamps
        start.append(start_time_list[0])
        #meeting end does not have end times, so last obs needs something else. if statement check if length is == 0 (implicit boolean)
        if not end_time_list:
            end.append("mødeslut")
        else:
            end.append(end_time_list[-1])
    
    df = pd.DataFrame(taler_list, columns = np.unique(var_list)) 
    df['tale'] = speech_list
    df['start'] = start
    df['end'] = end
    
    return df

#getting all the data
final_df = pd.DataFrame()
length = len(documents)
i = 0
percentages = [0.10,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.99]
perc = [round(length * p) for p in percentages]

for path in documents: 
    if i == 0: 
        print("Starting")
    if i in perc:
        print(round(100*(i/length)),"% done with the loop")
    if i == length:
        print("done")
    dataframe = df_func(path)
    final_df = final_df.append(dataframe)
    i = i +1

final_df.to_csv("FT_speechdata.csv",encoding = "UTF-8", index = False)
