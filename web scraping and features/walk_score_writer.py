import pandas as pd
import numpy as np
import re
import urllib
import csv
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
import json
import urllib2




class WalkScoreWriter:
    """
    Get walk score for each property using WalkScore.api
    You'll need your walkscore key.
    """
    def __init__(self, zipcode):
        self.zipcode = zipcode
        incsvfile_sold = '/Users/chuntinglu/Desktop/datatest/sold_merged_1_' 
                     + zipcode + '.csv'
        incsvfile_forsale = '/Users/chuntinglu/Desktop/datatest/forsale_merged_1_' 
                     + zipcode + '.csv'
        self.df_sold = pd.read_csv(incsvfile_sold)
        self.df_forsale = pd.read_csv(incsvfile_forsale)
    
    def get_walkscore_address(self, zillow_street_address):
        zillow_street_address = zillow_street_address.lower()
        
        if len(re.findall('ave|st|pl|broadway|park|dr|cir|yards', 
                             zillow_street_address)) == 0:
            if len(re.findall('apt|ste|#', zillow_street_address)) == 0:
                print "skipped", zillow_street_address
                return np.nan
            endidx = [m.end(0) for m in re.finditer('apt|ste|#',
                     zillow_street_address)][0]
            return zillow_street_address[:endidx].strip()
        elif len(re.findall('apt|ste|#', zillow_street_address)) == 0:
            return zillow_street_address.strip()
        else:
            endidx = [m.start(0) for m in re.finditer('apt|ste|#', 
                                        zillow_street_address)][0]
            return zillow_street_address[: endidx].strip()
    
    def get_walkscore_url(self,row):
        """
        replace <your-walkscore-key> by your walkscore key
        """
        key = <your-walkscore-key>
        url_part1 = 'http://api.walkscore.com/score?format=json&address='
        string = row.walkscore_address
        if type(string) == float:
            return np.nan
        address_list = string.split(" ")
        if address_list[0].isdigit():
            street_number = address_list[0]+'%'
            address_list = address_list[1:]
            street_name = '%20'.join(address_list)
        
            citystate = '%20New%20York%20NY%20'
            zipcode = self.zipcode
            url_part2 = street_number + street_name + citystate + zipcode
        else:
            return np.nan
    
        url_part3 = '&lat='+ str(row.latitude)
        url_part4 = '&lon='+str(row.longitude)
        url_part5 = '&wsapikey='+key
        return url_part1 + url_part2 + url_part3 + url_part4+url_part5
    
    def request_walkscore(self,row):
        try: 
            to_open = urllib2.urlopen(row.walk_url)
            time.sleep(7)
            data = json.load(to_open)
        
            if data['status'] == 1:
                try:
                    print data['walkscore'], row.walk_url
                    return data['walkscore']
                except:
                    print "skipped", row.walkscore_address, self.zipcode
                    return np.nan
            
        except:
            print "error", row.walk_url
            return np.nan
        
            
      
        
    def write_df(self):
        self.df_sold['walkscore_address'] = 
                    self.df_sold.street.apply(self.get_walkscore_address)
        self.df_sold['walk_url'] = 
                    self.df_sold.apply(self.get_walkscore_url, axis = 1)
        self.df_sold['walkscore'] = 
                    self.df_sold.apply(self.request_walkscore, axis = 1)
        self.df_forsale['walkscore_address'] = 
                    self.df_forsale.street.apply(self.get_walkscore_address)
        self.df_forsale['walk_url'] = 
                    self.df_forsale.apply(self.get_walkscore_url, axis = 1)
        self.df_forsale['walkscore'] = 
                    self.df_forsale.apply(self.request_walkscore, axis = 1)
        outcsvfile_sold = outcsvfile =
                    '/Users/chuntinglu/Desktop/datatest/sold_merged_2_' + 
                             self.zipcode + '.csv'
        outcsvfile_forsale = 
                    '/Users/chuntinglu/Desktop/datatest/forsale_merged_2_' +
                             self.zipcode + '.csv'
        self.df_sold.to_csv(outcsvfile_sold, 
                     encoding = 'utf-8', index = None)
        self.df_forsale.to_csv(outcsvfile_forsale,
                     encoding = 'utf-8', index = None)
        
    
    
    
    
    
    
if __name__ == '__main__':
    #Murray Hills
    #zipcodes = ['10022'] done
    #zipcodes = ['10016', '10017','10010'] done
    #Greenwich and Soho
    #zipcodes = ['10014'] done
    #['10013'] done
    # Lower Manhattan    problem
    #zipcodes = ['10038', '10280']
    # 10007 skip, 10005 done
    # Lower East Side
    #zipcodes = ['10003']
    # Upper East Side done
    #zipcodes = ['10021', '10028', '10065', '10075', '10128']
    # Upper West Side done
    #zipcodes = ['10023', '10024', '10025']
    #Central Harlem done
    #zipcodes = ['10026']
    #Chelsea and Clinton
    #zipcodes = ['10001', '10019', '10036']
    
    for zipcode in zipcodes:
        walkscorewriter = WalkScoreWriter(zipcode)
        walkscorewriter.write_df()
        
        
    