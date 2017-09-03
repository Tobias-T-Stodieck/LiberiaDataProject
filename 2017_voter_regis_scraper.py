'''
File Name: 2017_voter_regis_scraper.py
Author: Tobias Stodieck
Date Created: Sept 1, 2017
Date Last Modified: Sept 2, 2017
Python Version: 3.6

Written for the UC San Diego Economics Department

Grabs and saves the 2017 voter registration PDFs located on the Liberian 
National Elections Commission website.
Converts the PDFs into CSVs by scraping through Tabula.
Aggregates all the county data into one big master CSV file.
'''
import os
import requests as req
import tabula as tab
import pandas as pd
from bs4 import BeautifulSoup

#Working directory paths
base_dir = '/Users/Tobias/Desktop/Liberia Project/2017_voter_regis_data'
pdf_dir = base_dir + '/2017_voter_regis_PDFs'
csv_dir = base_dir + '/2017_voter_regis_CSVs'

#This web page contains the links to each county's voter registration PDFs
regis_page = 'http://www.necliberia.org/page_info.php?&7d5f44532cbfc489b8db9e12e44eb820=MjAz'
#Gets a parseable copy of the HTML in the registration page
regis_soup = BeautifulSoup(req.get(regis_page).content, 'lxml')
#The links to all the PDFs start with this base
base_page = 'http://www.necliberia.org/'
#Master data frame that all county data will be aggregated into
voter_regis = pd.DataFrame()
#Finds all the hyperlink tags in the soup
for link in regis_soup.findAll('a'):
    pdf_link = link.get('href')
    #If the href contains 'VRC', then we know it'll be a link to a PDF
    if 'VRC' in pdf_link:
        #Gets the PDF directly from the website
        pdf_page = req.get(base_page + pdf_link)
        #File name will be county name
        file_name = pdf_link.split('FINAL_')[1]      
        #Writes PDF to new file to save
        pdf_path = os.path.join(pdf_dir, file_name)
        with open(pdf_path, 'wb') as pdf:
            pdf.write(pdf_page.content)       
            pdf.close()
        #Reads PDF tables into a pandas dataframe by scraping with tabula    
        df = tab.read_pdf(pdf_path, pages='all')    
        #Drops empty rows due to awkward formatting
        df.dropna(inplace=True)
        #Sets the column headers of the dataframe to the ones used in the PDF
        cols = ['serial_num', 'precinct_code', 'county', 'magisterial_area', \
                'locality', 'center_name', 'elec_dist', 'status']
        df.columns = cols
        #Sets the index to 'precinct_code' and drops the default index
        df.set_index(keys='precinct_code', drop=True, inplace=True)
        #Saves dataframe for each county as a csv file
        df.to_csv(os.path.join(csv_dir, os.path.splitext(file_name)[0]+'.csv'))
        #Appends all county dataframes into master frame
        voter_regis = voter_regis.append(df)
        #Writes to csv file
        voter_regis.to_csv(os.path.join(base_dir, '2017_voter_regis.csv'))
