'''
File Name: 2011_elections_scraper.py
Author: Tobias Stodieck
Date Created: Sept 1, 2017
Date Last Modified: Oct 15, 2017
Python Version: 3.6

Written for the UC San Diego Economics Department

Scrapes the Liberian National Elections Commission website for presidential and
vice presidential (initial and run-off), senate, and house representative
election data. 
'''

import os
from time import sleep
import requests as req
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup, SoupStrainer

os.chdir('/Users/Tobias/Desktop/Liberia Project/2011_election_data')
#The starting web page--all links use this as a base
results_2011_page = 'http://www.necliberia.org/results2011/'

#Returns a list of the links found on the specified webpage constrained by an 
#html tag and a common phrase that the links share
def search_webpage(webpage, html_tag, phrase):
    #Gets webpage
    content = req.get(webpage).content
    #Gets soup object containing only the data with the specified html tag
    soup = BeautifulSoup(content, 'lxml', parse_only=SoupStrainer(html_tag))
    #Gets all links contained within the html tag
    link_list = []  
    for link in soup.find_all(html_tag):
        href = link.get('href')
        if phrase in href:
            link_list.append(results_2011_page + href)
    return link_list

#Returns a two-index list containing a precinct code and county name
def _get_name_code(soup):
    #The precinct code is always the last 5 indices of the string
    CODE_INDEX = -5
    #Used to splice strings so the last 7 indices aren't included
    #Removes the word 'county' from the string
    NAME_INDEX = -7
    #Pages without the two html header attributes are empty, so returns None
    try:
        precinct_code = soup.find('h4').text[CODE_INDEX:]
        county_name = soup.find('h2').text[:NAME_INDEX]
    except AttributeError:
        return None
    return [int(precinct_code), county_name]
    
#Gets basic information from election results page
def _get_results(center_links):
    #Four lists for runoff, pres/vp, senate, and house elections   
    runoff_frame = []
    pvp_frame = []
    senate_frame = []
    house_frame = []
    
    #Iterates through each center link getting the appropriate information
    for center in center_links:
        #Gets soup for each individual center page
        soup = BeautifulSoup(req.get(center).content, 'lxml')
        #Gets the precinct code and county name for each center  
        center_ID = _get_name_code(soup)
        #Blank pages are skipped
        if center_ID is None:
            continue
        #This signifies a runoff election page
        if 'r.html' in center:            
            row_data = center_ID + _get_runoff(soup)        
            runoff_frame.append(row_data)
        #Gets data for the pres/vp, senate, and house elections
        else:
            data = _get_data(soup, center_ID)         
            pvp_frame.extend(data[0])
            senate_frame.extend(data[1])
            house_frame.extend(data[2])
    #Column names for the data frames
    runoff_cols = ['precinct_code', 'county', 'johnson_count', 'tubman_count',
                   'valid', 'invalid', 'total']
    data_cols = ['precinct_code', 'county', 'candidate', 'votes']               
    #Creates a dictinary where each data frame's key is its name
    dfs = {'runoff.csv' : pd.DataFrame(runoff_frame, columns=runoff_cols),
           'pvp.csv' : pd.DataFrame(pvp_frame, columns=data_cols),
           'senate.csv' : pd.DataFrame(senate_frame, columns=data_cols),
           'house.csv' : pd.DataFrame(house_frame, columns=data_cols)}     
                
    return dfs

#Gets data from a runoff table
def _get_runoff(soup):
    #The number of voting groups for each center
    groups = len(soup.find_all('th')[1:])
    #There will always be 5 categories (tubman, johnson, valid, invalid, total)
    CATEGORIES = 5
    #An array of all the voting values
    vote_vals = np.array([int(val.text) for val in soup.find_all(class_='b')])
    #Reshapes the array to have dimensions equal to the number of categories by
    #the number of voting groups  
    if groups > 1:
        vote_vals = vote_vals.reshape(CATEGORIES, groups)
        #Sums the voting totals across all groups for each category
        vote_vals = np.sum(vote_vals, axis=1)        
    #Returns voting data 
    return vote_vals.tolist()

#Gets the results of the pvp, senate, and house elections
def _get_data(soup, center_ID):    
    #Each index is a 2D list that contains data frames for the pres/vp, senate,
    #and house election data for each precinct 
    dfs = [[],[],[]]
    #Finds the three data tables, one for each election
    tables = soup.find_all(class_='res')
    #Each data frame in dfs corresponds to a table in the web page
    #for each precinct
    for df, table in zip(dfs, tables):
        #Finds the rows of data
        for row in table.find_all('tr'):
            #Creates a new list for the row starting with the precinct code
            #and county
            row_data = list(center_ID)
            #Gets the individual pieces of data from the row
            for datum in row.find_all('td'):
                cell = datum.text
                if cell.isnumeric():
                    cell = int(cell)
                #Total number of columns
                MAX_COLS = 4
                if (len(row_data) == MAX_COLS):
                    #Column that contains the sum of the vote totals
                    VOTE_COL = 3
                    row_data[VOTE_COL] = row_data[VOTE_COL] + cell
                else:
                    row_data.append(cell)
            df.append(row_data)
       
    return dfs
 
def main():
    #Gets links to all individual county pages
    county_links = search_webpage(results_2011_page, 'area', 'county')
    #Gets links to all individual precinct pages across all counties
    precinct_links = []
    for county in county_links:
        precinct_links.extend(search_webpage(county, 'a', 'vp'))
        sleep(0.5)
    #Gets the results for all four elections from each voting center
    center_links = []  
    for precinct in precinct_links:
        center_links.extend(search_webpage(precinct, 'a', 'pp_results'))
        sleep(0.5)
    #Gets results for each election and writes all four dfs to csvs
    dfs = _get_results(center_links)   
    for name in dfs:
        dfs[name].to_csv(name)
        
if __name__ == '__main__':
    main()


