import pandas as pd
import numpy as np
import re
import urllib
import requests
import time
import csv

from datetime import datetime
from bs4 import BeautifulSoup



class TruliaGetForSaleLinks:
    """
    Scrape Trulia and get a list of urls of all for sale condos in NYC.
    Store the results for each zipcode on local csv files.
    """
    
    def __init__(self, zipcode):
        self.forsaleurl = 'https://www.trulia.com/for_sale/'+zipcode+'_zip/CONDO_type/'
        
    def get_links_stats(self):
        zipstats = requests.session().get(self.forsaleurl)
        soup =  BeautifulSoup(zipstats.text, 'html.parser')
        pagestats = soup.find("div", class_="txtC h6 typeWeightNormal typeLowlight")
        if (pagestats == None):
            
            print (zipcode + 'skipped')
            return None
        else:
            pagelimit = int(pagestats.text.encode('utf-8').strip().split(' ')[-2])
            if pagelimit < 30:
                return None
        return pagelimit
        
    def get_forsale_links(self):
        pagelimit = self.get_links_stats()
        if pagelimit == None:
            print "failed to process zip code" +zipcode
            return None
        
        forsalelist = []
        numpages = pagelimit/30 + 1
        print(str(pagelimit) + ' resulsts ', str(numpages)+' pages')
        for i in range(1, numpages + 1):
            sess = requests.session()
            pageurl = self.forsaleurl+str(i)+ '_p/'
            page = sess.get(pageurl)
            soup = BeautifulSoup(page.text, 'html.parser')
            soupobject = soup.find_all("a", class_ = "tileLink")
            if i!= numpages:
                #print pageurl
                for j in range(0, 30):
                    if 2*j < len(soupobject):
                        #soupobject = soup.find_all("a", class_ = "tileLink")
                        #print len(soupobject)
                        addresslink = soupobject[j*2].get("href")
                        if addresslink[1] == 'f':
                            forsalelist.append([np.nan, zipcode])
                        else:
                            forsalelist.append([addresslink, zipcode])
                    else: 
                        forsalelist.append([np.nan, zipcode])
                    
            else:
                num_links_lastpage = pagelimit - 30*(numpages-1)
                soupobject = soup.find_all("a", class_ = "tileLink")
                for j in range(0, num_links_lastpage):
                    #soupobject = soup.find_all("a", class_ = "tileLink")
                    if 2*j < len(soupobject):
                        addresslink = soupobject[j*2].get("href")
                        # exclude foreclosures and builder plans
                        if (addresslink[1] == 'f') or (addresslink[1] == 'b'):
                            forsalelist.append([np.nan, zipcode])
                        else:
                            forsalelist.append([addresslink, zipcode])
                    else: 
                        forsalelist.append([np.nan, zipcode])
            
            time.sleep(5)
        
        return forsalelist
    
    def write_lists(self):
        forsalelist = self.get_forsale_links()
        urllist = pd.DataFrame(forsalelist, columns = ['url', 'zipcode'])
        urllist.dropna(inplace = True)
        urllist.to_csv('/Users/chuntinglu/Desktop/all/forsale_'+ zipcode + '.csv', 
                       encoding = 'utf-8', index = None)
        print('collected all links from ', zipcode)
        
    
    


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
        trulia_forsale_links = TruliaGetForSaleLinks(zipcode)
        trulia_forsale_links.write_lists()
        
        
