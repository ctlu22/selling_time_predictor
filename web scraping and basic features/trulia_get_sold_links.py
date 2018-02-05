import pandas as pd
import numpy as np
import re
import urllib
import requests
import time
import csv

from datetime import datetime
from bs4 import BeautifulSoup

class TruliaGetSoldLinks:
    '''
    Scrape Trulia and get links for all recently sold condos
    (in the last 9 months) in Manhattan.
    Store the results for each zipcode locally as csv files.
    '''

    def __init__(self, zipcode):
        self.soldurl = 'https://www.trulia.com/sold/'+zipcode+'_zip/CONDO_type/'
        
    def get_links_stats(self):
        zipstats = requests.session().get(self.soldurl)
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
        
    def get_sold_links(self):
        pagelimit = self.get_links_stats()
        if pagelimit == None:
            print "failed to process zip code" +zipcode
            return None
        
        soldlist = []
        numpages = pagelimit/30 + 1
        print(str(pagelimit) + ' resulsts ', str(numpages)+' pages')
        for i in range(1, numpages + 1):
            sess = requests.session()
            pageurl = self.soldurl+str(i)+ '_p/'
            page = sess.get(pageurl)
            soup = BeautifulSoup(page.text, 'html.parser')
            if i!= numpages:
                #print pageurl
                for j in range(0, 30):
                    soupobject = soup.find_all("a", class_ = "tileLink")
                    #print len(soupobject)
                    addresslink = soupobject[j*2].get("href")
                    soldlist.append([addresslink, zipcode])
                time.sleep(5)
            else:
                num_links_lastpage = pagelimit - 30*(numpages-1)
        
                for j in range(0, num_links_lastpage):
                    soupobject = soup.find_all("a", class_ = "tileLink")
                    addresslink = soupobject[j*2].get("href")
                    soldlist.append([addresslink, zipcode])
                time.sleep(5)
        
        return soldlist
    
    def write_lists(self):
        soldlist = self.get_sold_links()
        urllist = pd.DataFrame(soldlist, columns = ['url', 'zipcode'])
        urllist.to_csv('/Users/chuntinglu/Desktop/all/sold_'+ zipcode + '.csv', encoding = 'utf-8', index = None)
        print('collected all links from ', zipcode)
        
    
    


if __name__ == '__main__':

    #Murray Hills
    #zipcodes = ['10010', '10016', '10017','10022']
    #Greenwich and Soho
    #zipcodes = ['10012', '10013', '10014']
    # Lower Manhattan
    #zipcodes = ['10004', '10005', '10006', '10007', '10038', '10280']
    # Lower East Side
    #zipcodes = ['10002', '10003', '10009']
    # Upper East Side
    #zipcodes = ['10021', '10028', '10044', '10065', '10075', '10128']
    # Upper West Side
    #zipcodes = ['10023', '10024', '10025']
    # Central Harlem
    #zipcodes = ['10026', '10027', '10030', '10037', '10039']
    #Chelsea and Clinton
    #zipcodes = ['10001', '10019', '10036']
    # East Harlem
    #zipcodes = ['10029', '10035']
    for zipcode in zipcodes:
        trulia_sold_links = TruliaGetSoldLinks(zipcode)
        trulia_sold_links.write_lists()



