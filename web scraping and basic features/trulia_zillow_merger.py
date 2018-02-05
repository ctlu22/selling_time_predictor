import pandas as pd
import numpy as np
import re
import urllib
import csv
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime

class TruliaZillowMerger:

	'''
	Merge Trulia and Zillow Features for each zipcode
	'''

    def __init__(self, zipcode):
        self.zipcode = zipcode
       
        
    
    def merge_sold_frames(self):
        incsvfile_trulia = '/Users/chuntinglu/Desktop/datatest/ \
            sold_deepsearch_' + self.zipcode + '.csv'
        incsvfile_zillow = '/Users/chuntinglu/Desktop/datatest/ \
            sold_features_'+ self.zipcode + '.csv'
        truliadf = pd.read_csv(incsvfile_trulia)
        zillowdf = pd.read_csv(incsvfile_zillow)
        merged = truliadf.merge(zillowdf, on = 'url', how = 'inner')
        outcsvfile = '/Users/chuntinglu/Desktop/datatest/  \
            sold_merged_1_' + self.zipcode + '.csv'
        merged.to_csv(outcsvfile, encoding = 'utf-8', index = None)
        
        
    def merge_forsale_frames(self):
        incsvfile_trulia = '/Users/chuntinglu/Desktop/datatest/ \
            forsale_deepsearch_' + self.zipcode + '.csv'       
        incsvfile_zillow = '/Users/chuntinglu/Desktop/datatest/ \
            forsale_features_' + self.zipcode + '.csv'
        truliadf = pd.read_csv(incsvfile_trulia)
        zillowdf = pd.read_csv(incsvfile_zillow)
        merged = truliadf.merge(zillowdf, on = 'url', how = 'inner')
        outcsvfile = '/Users/chuntinglu/Desktop/datatest/ \
            forsale_merged_1_' + self.zipcode + '.csv'
        merged.to_csv(outcsvfile, encoding = 'utf-8', index = None)
        
if __name__ == '__main__':
    #Murray Hills
    #zipcodes = ['10010', '10016', '10017','10022']
    #Greenwich and Soho
    #zipcodes = ['10013', '10014']
    # Lower Manhattan
    #zipcodes = ['10005', '10007', '10038', '10280']
    # Lower East Side
    #zipcodes = ['10003']
    # Upper East Side
    #zipcodes = ['10021', '10028', '10065', '10075', '10128']
    # Upper West Side
    #zipcodes = ['10023', '10024', '10025']
    #Central Harlem
    #zipcodes = ['10026'] 
    #Chelsea and Clinton
    #zipcodes = ['10001', '10019', '10036']
    
    for zipcode in zipcodes:
        merged = TruliaZillowMerger(zipcode)
        merged.merge_sold_frames()
        merged.merge_forsale_frames()
        
        