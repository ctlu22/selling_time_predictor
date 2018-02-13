import pandas as pd
import numpy as np
import re
import urllib
import csv
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime




class TruliaForSaleFeatures:
    
    def __init__(self, zipcode):
        self.zipcode = zipcode
        incsvfile = '/Users/chuntinglu/Desktop/datatest/details_forsale_'
                      +zipcode+'.csv'
        self.dfin = pd.read_csv(incsvfile)
        self.temp_columns = ['url', 'overview', 'askingprice', 
                 'description','sqft_t','avg_sqft_t', 'zipcode', 'duration']
        self.temp_dfout = pd.DataFrame(columns = self.temp_columns)
        
        
    
   
    def clean_forsale_trulia(self, row):
        """
        helper function for write_trulia_forsale_temp_features
        returns a lsit of temp features 
        """
        print row
        tempsalefeatures = []
        
        tempsalefeatures.append(row.url)
        tempsalefeatures.append(row.overview)
        price = self.get_price(row.askingprice)
        tempsalefeatures.append(price)
        tempsalefeatures.append(row.description)
        
        sqft_t = self.get_sqft(row.overview)
        tempsalefeatures.append(sqft_t)
        
        avg_sqft_t = self.get_avg_sqft(row)
        tempsalefeatures.append(avg_sqft_t)
        
        tempsalefeatures.append(self.zipcode)
        
        duration = self.get_duration(row.overview)
        tempsalefeatures.append(duration)
        
        
        return tempsalefeatures
    
        
       
    
    
    def get_price(self, askingprice):
        """
        helper function for clean_forsale_trulia
        """
        
        if askingprice == np.nan or type(askingprice) == float:
            return np.nan
        #else:
            #tempaskprice = askingprice
            #return int(re.sub("[^0-9]", "", tempaskprice).strip())
        try:
            return int(re.sub("[^0-9]", "", askingprice).strip())
        
        except ValueError:
            return np.nan
            
        
        
    
    
    
    def get_sqft(self, overview):
        """
        helper function for clean_forsale_trulia
        """
        if len(overview) == 0:
            return np.nan
        else:
            overviewlist = str(overview).split(',')
            for m, item in enumerate(overviewlist):
                if 'sqft' in item:
                    itemstr = item.strip().split(' ')[0]
           
                    if (m > 0) and (overviewlist[m-1].strip().isdigit()):
                         return int(overviewlist[m-1].strip()+itemstr)
                    elif int(itemstr)>50:
                        return int(itemstr)
            return np.nan
        
    
    
    def get_avg_sqft(self, row):
        """
        helper function for clean_forsale_trulia
        """
        if (type(row.askingprice) == float) or (len(row.overview) ==0):
            return np.nan
        temp_price = self.get_price(row.askingprice)
        temp_sqft = self.get_sqft(row.overview)
        
        try:
            return int(temp_price/temp_sqft)
        except ValueError:
            return np.nan
            
            
    def get_duration(self, overview):
       
        overviewlist = str(overview[1:-1]).split(',')
        for item in overviewlist:
            if 'days on Trulia' in item:
                return int(item.strip().split(' ')[0])
        return np.nan


    
    
    
    
    
    
    def write_trulia_forsale_temp_features(self):
        temp_outcsvfile = '/Users/chuntinglu/Desktop/datatest/forsale_temp_features_'+zipcode+'.csv'
        self.temp_dfout.to_csv(temp_outcsvfile, encoding = 'utf-8', index = None)
        
        count = 0
        
        for (idx, row) in self.dfin.iterrows():
            
            count += 1
            if count%10 == 0:
                print count
            tempsalefeatures = self.clean_forsale_trulia(row)
            
            itemdf = pd.DataFrame([tempsalefeatures], columns = self.temp_columns)
    
            itemdf.to_csv(temp_outcsvfile, encoding = 'utf-8', mode = 'a', header = False, index = None)
        
        return temp_outcsvfile
    
    
    
    
    def write_trulia_forsale_features(self):
        
        
        temp_infile = self.write_trulia_forsale_temp_features()
        
        forsale = pd.read_csv(temp_infile)
        forsalecopy = forsale.copy()
        
        #soldcopy['yearbuilt_tillnow_t'] = soldcopy.yearbuilt_t.apply(get_yearbuilt_tillnow)
        forsalecopy.dropna(subset = ['askingprice','duration'], inplace = True)
        
        
        forsalecopy['weeks'] = forsalecopy['duration']/7 + 1
        forsalecopy['weeks'] = forsalecopy.weeks.apply(int)
        forsalecopy['sold'] = False
        
        outcsvfile = '/Users/chuntinglu/Desktop/datatest \
                         /forsale_features_'+zipcode+'.csv'
        forsalecopy.to_csv(outcsvfile, encoding = 'utf-8', index = None)
        
        
        
        
        
           
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
    #zipcodes = ['10023', '10024', '10025', '10026', '10001', '10019', '10036']
    #zipcodes = ['10023', '10024', '10025']
    #Central Harlem
    #zipcodes = ['10026']
    #Chelsea and Clinton
    #zipcodes = ['10001', '10019', '10036']
    
    for zipcode in zipcodes:
        truliaforsalefeatures = TruliaForSaleFeatures(zipcode)
        truliaforsalefeatures.write_trulia_forsale_features()
        
    