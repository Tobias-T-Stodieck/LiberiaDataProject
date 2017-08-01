'''
Created on Jul 30, 2017

File Name: LiberiaMapCoordParser.py
Author:  Tobias Stodieck
Date Created: July 7, 2017
Date Last Modified: July 31, 2017
Python Version 3.6

Written for the UC San Diego Economics Department

Parses LiberiaMapText.txt for Liberian voter registration center data
'''

import os
import re
import pandas as pd

#Set working directory
os.chdir(os.path.join(os.path.expanduser('~'), 'Desktop/Liberia Project'))

#Reads LiberiaMapText.txt; it only contains one line
with open('LiberiaMapText.txt') as f:
    #Text file only has one line
    line = f.readline()
    f.close()

#Returns pandas series of strings containing names parsed from the text file  
def read_str(st):  
    #Finds the location of the strings specified in str_dict  
    indices = [m.end() for m in re.finditer(st, line)]
    str_list = []
    #Gets the actual strings from the text file using the index numbers
    for i in indices:
        str_list.append(line[i:line.find('"', i)])
    return pd.Series(str_list)  
    
#Returns pandas series of numbers (coordinates and center codes) 
#parsed from the text file    
def read_int(num):   
    #Finds location of the numbers specified in num_dict 
    indices = [m.end() for m in re.finditer(num, line)]
    num_list = []
    #Gets the integers from the text file using the index numbers
    for i in indices:
        num_list.append(int(line[i:line.find(',', i)]))
    return pd.Series(num_list)

#The names of the places    
str_dict = {'magisterial_area': 'Magisterial_Area":"', 
                'locality': 'Locality":"',
                'center': 'Center":"', 
                'status': 'Status":"' } 
#The integer values of the places' coordinates and ID codes    
num_dict = {'x_utm': 'X_UTM":', 'y_utm': 'Y_UTM":', 
            'rccode': 'RCCode":', 'vrcid': 'VRCID":'}   
    
df = pd.DataFrame()
#Iterates through the two dictionaries, creates dataframe columns using
#the dictionary keys and adds the series returned from the read functions
for col, search in str_dict.items():
    df[col] = read_str(search).values
  
for col, search in num_dict.items():
    df[col] = read_int(search).values    

#Sorts by rccode because that's how we'll identify the registration centers
df.sort_values(by='rccode', inplace=True)
df.set_index(keys='rccode', drop=True, inplace=True)
df.to_csv('LiberiaMapData.csv')