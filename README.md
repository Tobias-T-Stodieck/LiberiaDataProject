# LiberiaDataProject

A collection of the scripts I wrote for the economics department at UC San Diego. These scripts were used to aid in the research of the change in public opinion with regard to the public school system in Liberia. 

2011_elections_scraper.py - Scrapes the results of Liberia's 2011 presidential, presidential run-off, senate, and house elections and stores the results in four data frames and csv files. Uses BeautifulSoup to get election data from the HTML of each individual precinct's election page, and uses Pandas and Numpy to manipulate and store data.

2017_voter_regis_scraper.py - Uses BeautifulSoup to navigate Liberian National Elections Commission website HTML for PDFs containing registration data for each county. Grabs and saves those PDFs, then uses Tabula to scrape PDFs into Pandas dataframes and convert to CSV files. Finally, creates an aggregated master CSV file.

LiberiaMapCoordParser.py - Parses a file called 'LiberiaMapText.txt', which I got from an arcGIS map, that contains voter registration center data. Relevant data includes the voting center's coordinates, number of registered voters, etc. Stores data in CSV form.
