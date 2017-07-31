'''
File name: LiberiaElectionsPDFScraper.py
Author: Tobias Stodieck
Date Created: Jul 28, 2017
Date Last Modified: July 30, 2017
Python Version: 3.6

This was written for the UC San Diego Economics Department

Grabs PDFs from Liberian National Elections Commission website
Scrapes PDFs for voter registration data
Pipes data to CSV files
'''
import re
import os
import requests as req
import bs4
import tabula
import pandas as pd

#Makes directory if it doesn't exist
def makeDirectory(direc):
    if not os.path.exists(direc):
        os.makedirs(direc)
        
#Directories to save everything into
master_dir = os.path.join(os.path.expanduser('~'), 'Desktop/VRCData')
pdf_dir = os.path.join(master_dir, 'PDFs')
csv_dir = os.path.join(master_dir, 'CSVs')
#Makes directories
makeDirectory(master_dir)
makeDirectory(pdf_dir)
makeDirectory(csv_dir)

#Requests page containing all the PDF files from website
web_page = req.get(  \
    '''http://www.necliberia.org/'''
    '''page_info.php?&7d5f44532cbfc489b8db9e12e44eb820=MjAz''')
#Error checking
web_page.raise_for_status()

#Creates text object to be parsed
soup = bs4.BeautifulSoup(web_page.text, 'html.parser')
elems = str(soup.select('#table17')[0])
#Finds all instances of hrefs to be filtered later
href_list = [m.end() for m in re.finditer('href="', elems)]

#Sets working directory to PDFs
os.chdir(pdf_dir)
#Gets links to PDFs by finding hrefs in html retrieved by bs4
for href in href_list:
    pdf_str = elems[href:elems.find('"', href)]
    #Filters anything that is not a pdf or voter registration center data
    if pdf_str.endswith('.pdf') and 'VRC' in pdf_str:
        pdf = req.get('http://www.necliberia.org/' + pdf_str)
        #Extracts the name of the county to be used as the filename
        pdf_name = pdf_str.split('FINAL_')[1]
        #Writes PDFs to folder
        with open(pdf_name, 'wb') as f:
            f.write(pdf.content)
            f.close()
    else:
        continue

#Columns for the data frame to combine all the data together into 
df_cols = ['serial_num', 'rccode', 'county', 'magisterial_area',    \
           'locality', 'center', 'elec_dist', 'status']

#Sets working directory to CSVs
os.chdir(csv_dir)
for pdf in os.listdir(pdf_dir):        
    #Converts PDF to CSV
    try:
        #Reads table data from PDFs 
        df = tabula.read_pdf(os.path.join(pdf_dir, pdf), pages='all') 
        #Removes empty rows due to awkward formatting
        df.dropna(inplace=True)
        #Set columns
        df.columns = df_cols
        #Set index
        df.set_index(keys='rccode', drop=True, inplace=True)
        csv_file = (os.path.splitext(pdf)[0] + '.csv')
        df.to_csv(csv_file)
    except:
        continue

#Creates master data frame and concatenates the data from all the counties 
master_df = pd.DataFrame(columns=df_cols)
master_df.set_index(keys='rccode', drop=True, inplace=True) 
#Reads the newly created CSVs and concatenates all of them into a master file
for csv in os.listdir(os.getcwd()):
    try:
        df = pd.read_csv(csv)
        master_df = pd.concat([master_df, df])
    except:
        continue    
master_df.to_csv('master_list.csv')