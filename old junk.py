# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 11:13:32 2020

@author: August
"""

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
