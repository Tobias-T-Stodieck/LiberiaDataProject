# LiberiaDataProject

A collection of the scripts I wrote for the economics department at UC San Diego. These scripts were used to aid in the research of the change in public opinion with regard to the public school system in Liberia. 

LiberiaElectionsPDFScraper.py - Gets PDFs from Liberian National Elections Commission website and saves to a directory called 'PDFs' in another directory called 'VRCData'. Then, scrapes all the PDFs for relevant election data and stores that data as CSVs in a directory called 'CSVs' within 'VRCData'.

LiberiaMapCoordParser.py - Parses a file called 'LiberiaMapText.txt', which I got from an arcGIS map, that contains voter registration center data. Relevant data includes the voting center's coordinates, number of registered voters, etc. Stores data in CSV form.
