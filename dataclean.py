# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 11:21:37 2020

@author: august
"""

import xml.etree.ElementTree as ET
import os

#set wd
os.chdir("C:\\Users\\augus\\OneDrive - Københavns Universitet\\Documents\\Uni\\Kandidat i Statskundskab\\4. semester kandidat\\Projekt\\FT-project")

#load the file
tree = ET.parse("ODAXML\\Referat\\samling\\20091\\20091_M1_helemoedet.xml")

root = tree.getroot()

print('Item #2 attribute:')

print('\nAll attributes:')
for elem in root:
    for subelem in elem:
        print("the text is",subelem)
        #print("the text is",subelem.text)