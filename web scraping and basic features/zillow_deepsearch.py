import pandas as pd
import numpy as np
import re
import urllib
import csv
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime


class ZillowDeepSearch:

    '''
    parse url from trulia to get ZillowDeepSearch results from Zillow api
    You may want to replace <ZWS-ID> with your zillow id
    Get more features on Zillow (as well as some basic features
        to supplement the missing values on Trulia later) 
    '''
    def __init__(self, zipcode):
        incsvfile = '/Users/chuntinglu/Desktop/datatest/forsale_features_'+zipcode+'.csv'
        #incsvfile = '/Users/chuntinglu/Desktop/datatest/sold_features_'+zipcode+'.csv'
        self.dfin = pd.read_csv(incsvfile)['url']
        self.columnslist = ['zpid', 'street', 'latitude', 'longitude','yearbuilt', 
                            'taxAssYear', 'taxAss', 'finishedsqft', 'bathrooms',
                            'bedrooms','totalrooms','zindex', 'url']
        self.dfout = pd.DataFrame(columns = self.columnslist)
       
    def get_zillow_address(self,url):
        '''
        replace <ZWS-ID> with your zillow id
        '''
       # example: url = '/homes/New_York/New_York/sold/1000700523-45-E-30th-St-6A-New-York-NY-10016'
       # string = '45-E-30th-St-6A-New-York-NY-10016'
        string = url[url.find(r'-')+1:]
       # citystate = 'New-York-NY-10016'
        citystate_idx = string.find('New')
        citystate = string[citystate_idx:]
       #  street_address'45-E-30th-St-6A'
        street_address = string[:citystate_idx-1]
       # create the url for zillow deep search
        zurl = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm? \
               zws-id=<ZWS-ID>&address='+
               street_address+'&citystatezip='+citystate
        return zurl
    
    def get_deepsearch(self,zurl):
        ds = []
        #print(zurl)
        time.sleep(5)
        zpage = requests.session().get(zurl)
        soup = BeautifulSoup(zpage.text, 'html.parser')
        if soup.find_all('code') == None or (len(soup.find_all('code')) == 0 ):
            print "skipped", zurl
            return None
    
        if soup.find_all('code')[0].text.encode('utf-8') != '0':
            print "skipped", zurl
            return None
   
        if soup.find_all("zpid") == None:
            ds.append(np.nan)
        else:
            ds.append(soup.find_all("zpid")[0].text.encode('utf-8'))
        
        if soup.find("street") == None:
            ds.append(np.nan)
        else:
            streetstr = soup.find("street").get_text().encode('utf-8')
            ds.append(streetstr)
        
        if soup.find("latitude") == None:
            ds.append(np.nan)
        else:
            latitudestr = soup.find("latitude").get_text().encode('utf-8')
            ds.append(latitudestr)
            
        if soup.find("longitude") == None:
            ds.append(np.nan)
        else:
            longitudestr = soup.find("longitude").get_text().encode('utf-8')
            ds.append(longitudestr)
        
        if soup.find_all("yearbuilt")== [] or soup.find_all("yearbuilt") == None : 
            ds.append(np.nan)
        else:
            ds.append(soup.find_all("yearbuilt")[0].text.encode('utf-8'))
   
        if soup.find_all("taxassessmentyear") == [] or soup.find_all("taxassessmentyear") == None:
            ds.append(np.nan)
        else:
            ds.append(soup.find_all("taxassessmentyear")[0].text.encode('utf-8'))
   
        if soup.find_all("taxassessment") == [] or soup.find_all("taxassessment") == None:
            ds.append(np.nan)
        else:
            ds.append(soup.find_all("taxassessment")[0].text.encode('utf-8'))
   
        if soup.find_all("finishedsqft") == [] or soup.find_all("finishedsqft") == None:
            ds.append(np.nan)
        else:
            ds.append(soup.find_all("finishedsqft")[0].text.encode('utf-8'))
   
        if soup.find_all("bathrooms") == [] or soup.find_all("bathrooms") == None:
            ds.append(np.nan)
        else:
            ds.append(soup.find_all("bathrooms")[0].text.encode('utf-8'))
   
        if soup.find_all("bedrooms") == [] or soup.find_all("bedrooms") == None:
            ds.append(np.nan)
        else:
            ds.append(soup.find_all("bedrooms")[0].text.encode('utf-8'))
   
        if soup.find_all("totalrooms") == [] or soup.find_all("totalrooms") == None:
            ds.append(np.nan)
        else:
            ds.append(soup.find_all("totalrooms")[0].text.encode('utf-8'))
   
        
       
        if soup.find_all("zindexvalue") == [] or soup.find_all("zindexvalue") == None:
            ds.append(np.nan)
        else:
            ds.append(soup.find_all("zindexvalue")[0].text.encode('utf-8'))
        print ds
        return ds




        


    def write_deepsearch(self):
        outcsvfile = '/Users/chuntinglu/Desktop/datatest/forsale_deepsearch_'+zipcode+'.csv'
        #outcsvfile = '/Users/chuntinglu/Desktop/datatest/sold_deepsearch_'+zipcode+'.csv'
        
        self.dfout.to_csv(outcsvfile, encoding = 'utf-8', index = None)
        count = 0
        
        for url in self.dfin:
            print url
            count += 1
            if count%10 == 0:
                print count
            zurl = self.get_zillow_address(url)
            print zurl
            deepsearch_list = self.get_deepsearch(zurl)
            if deepsearch_list is None:
                continue
            deepsearch_list.append(url)
            itemdf = pd.DataFrame([deepsearch_list], columns = self.columnslist)
    
            itemdf.to_csv(outcsvfile, encoding = 'utf-8', mode = 'a', header = False, index = None)
        
           
    
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
    #zipcodes = ['10021','10028', '10065', '10075', '10128']
    # Upper West Side
    #zipcodes = ['10023', '10024', '10025']
    #Central Harlem
    #zipcodes = ['10026','10001', '10019', '10036']
    #Chelsea and Clinton
    #zipcodes = ['10001', '10019', '10036']
    
    for zipcode in zipcodes:
        zillowdeepsearch = ZillowDeepSearch(zipcode)
        zillowdeepsearch.write_deepsearch()
       
    