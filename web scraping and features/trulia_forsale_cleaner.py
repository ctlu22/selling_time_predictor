import pandas as pd
import numpy as np
import re
from datetime import datetime
import urllib
import requests
import time
from bs4 import BeautifulSoup

class TruliaForSaleCleaner:

	"""

	Scrape basic info for each for sale condos in Manhattan.
    Take the previously scraped links from TruliaGetForSaleLinks as input.
    Output: Trulia url, overview, askingprice, text description 
    for each property.
	"""

    
    def __init__(self, zipcode):
        self.dfin = pd.read_csv('/Users/chuntinglu/Desktop/all/forsale_'+ zipcode + '.csv')['url']
        self.columnslist = ['url', 'overview', 'askingprice', 'description']
        self.dfout = pd.DataFrame(columns = self.columnslist)
    
    def clean_forsale_trulia(self, url):
        forsalelist = []
        forsalelist.append(url)
        time.sleep(5)
        sess = requests.session()
        houseurl = 'https://www.trulia.com' + str(url).strip()
        page = sess.get(houseurl)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        homeoverview = soup.find("div", class_="row mbm")
        overviewlist = []
        if homeoverview != None:
            if homeoverview.find_all("li") == None:
                overviewlist.append(np.nan)
            else:
                for li in homeoverview.find_all("li"):
                    overviewlist.append(li.text.encode('utf-8').strip())
        forsalelist.append(overviewlist)
        #get asking price
        head = soup.find_all("span", class_ = "h3")
        askingprice = head[0].text.encode('utf-8').strip()
        forsalelist.append(askingprice)
        #get description
        descriptionobject = soup.find("p", id = "propertyDescription")
        if descriptionobject == None:
            description = np.nan
        else:
            description = descriptionobject.text.encode('utf-8').strip()
    
        
        forsalelist.append(description)
        
        return forsalelist
        
        
    
    def write_trulia_forsale_cleaned(self):
        outcsvfile = '/Users/chuntinglu/Desktop/datatest/details_forsale_'+zipcode+'.csv'
        self.dfout.to_csv(outcsvfile, encoding = 'utf-8', index = None)
        
        count = 0
        
        for url in self.dfin:
            string = url[url.find(r'-')+1:]
            if string[0].isalpha():
                print "skipped", url
                pass
            else:
                count += 1
                if count%10 == 0:
                    print count
                forsale_cleaned = self.clean_forsale_trulia(url)
            
                itemdf = pd.DataFrame([forsale_cleaned], columns = self.columnslist)
    
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
    #zipcodes = ['10021', '10028', '10065', '10075', '10128']
    # Upper West Side
    #zipcodes = ['10023', '10024', '10025']
    #Central Harlem
    #zipcodes = ['10026']
    #Chelsea and Clinton
    #zipcodes = ['10001', '10019', '10036']
    
    for zipcode in zipcodes:
        truliaforsalecleaner = TruliaForSaleCleaner(zipcode)
        truliaforsalecleaner.write_trulia_forsale_cleaned()
        
    
               
        
