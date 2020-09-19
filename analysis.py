# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 11:22:36 2020

@author: augus
"""

import pickle
import matplotlib.pyplot as plt
import os

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
