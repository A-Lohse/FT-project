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

#load the file
tree = ET.parse("ODAXML\\Referat\\samling\\20091\\20091_M32_helemoedet.xml")

root = tree.getroot()


#opbygningen er "Tale" -> "taler" + "TaleSegment" + "TalerTitel" 
taler_list = []
var_list = []
speech_list = []
start = []
end = []

#for each speech in the XML 
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
    #meeting end does not have end times, so last obs needs something else
    if not end_time_list:
        end.append("mødeslut")
    else:
        end.append(end_time_list[-1])
    
#done

df = pd.DataFrame(taler_list, columns = np.unique(var_list)) 
df['tale'] = speech_list
df['start'] = start
df['end'] = end