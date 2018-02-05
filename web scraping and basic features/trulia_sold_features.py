import pandas as pd
import numpy as np
import re
import urllib
import csv
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime


class TruliaSoldFeatures:

    '''

    Parse the basic info scraped from TruliaSoldCleaner and
    generate more basic features. 
    Also, parse the price history to get the duration
    between the listing date and the date the list becomes pending.

    '''
    
    def __init__(self, zipcode):
        self.zipcode = zipcode
        incsvfile = '/Users/chuntinglu/Desktop/datatest/details_sold_'
                                 +zipcode+'.csv'
        self.dfin = pd.read_csv(incsvfile)
        self.temp_columns = ['url', 'overview', 'askingprice',
                           'description', 'pricehistory','sqft_t',
                     'avg_sqft_t', 'zipcode', 'start_date', 'end_date']
        self.temp_dfout = pd.DataFrame(columns = self.temp_columns)
        
        
    
    
    def clean_sold_trulia(self, row):

        '''
        helper function for write_trulia_sold_temp_features
        returns a list of temp features for each row of 'dfin'
        '''
        
        tempsoldfeatures = []
        
        tempsoldfeatures.append(row.url)
        tempsoldfeatures.append(row.overview)
        price = self.get_price(row.askingprice)
        tempsoldfeatures.append(price)
        
        revised_description = self.edit_description(row.description)
        tempsoldfeatures.append(revised_description)
        tempsoldfeatures.append(row.pricehistory)
        
        sqft_t = self.get_sqft(row.overview)
        tempsoldfeatures.append(sqft_t)
        
        avg_sqft_t = self.get_avg_sqft(row)
        tempsoldfeatures.append(avg_sqft_t)
        
        tempsoldfeatures.append(self.zipcode)
        
       
        pricehistorylist = self.clean_price_history(row.pricehistory)
        tempsoldfeatures.append(pricehistorylist[0])
        tempsoldfeatures.append(pricehistorylist[1])
        
        
        return tempsoldfeatures
    
        
       
    
    
    def get_price(self, askingprice):

        '''
        helper function for clean_sold_trulia
        '''
        if askingprice == np.nan or type(askingprice) == float:
            return np.nan
        try:
            return int(re.sub("[^0-9]", "", askingprice.strip()))
        except ValueError:
            return np.nan
            
        
        
    
    
    
    def get_sqft(self, overview):

    '''
    helper function for clean_sold_trulia
    '''
        if len(overview) == 0:
            return np.nan
        else:
            overviewlist = str(overview).split(',')
            for m, item in enumerate(overviewlist):
                if ('sqft' in item) and ('lot' not in item):
                    itemstr = item.strip().split(' ')[0]
           
                    if (m > 0) and (overviewlist[m-1].strip().isdigit()):
                         return int(overviewlist[m-1].strip()+itemstr)
                    elif int(itemstr)>50:
                        return int(itemstr)
            return np.nan
        
    
    
    def get_avg_sqft(self, row):

        '''

        helper function for clean_sold_trulia

        '''
        if (len(row.overview) == 0) or (type(row.askingprice) == float):
            return np.nan
        temp_price = self.get_price(row.askingprice)
        temp_sqft = self.get_sqft(row.overview)
        
        try:
            return int(temp_price/temp_sqft)
        except ValueError:
            return np.nan
            
            
    
                    
                  
    def edit_description(self, description):
        '''
        get rid of the Trulia prefix for part of the description
        in sold condos
        '''
        if (np.isnan(description) or len(description) == 0):
            return np.nan
        else:
            split_sentence = description.split(".")
        if len(split_sentence) <1:
            return np.nan
        else:
            if split_sentence[0].strip() == 
                      "This property is no longer available to rent or buy":
                split_description = re.split(r'\s{2,}', description)
                if len(split_description) > 1:
                    return split_description[1].strip()
                else:
                    return np.nan
            else:
                return description
    
 
    def clean_price_history(self, string):


        '''
        helper function for clean_sold_trulia
        returns listing date as the start date
        returns the 'pending' date as the end date if possible;
        otherwise returns the 'sold' or 'listing removed' date 
        as the end date (whichever comes first)
        '''
        cleaned_history = []
        pattern = re.compile(r'(\d+/\d+/\d+)')
        match = pattern.findall(string)
        iterlist = []
        for match in re.finditer(r'(\d+/\d+/\d+)', string):
            iterlist.append(match.span())
        #print iterlist
        n = len(iterlist)
        triallist = []
        for i, spanrange in enumerate(iterlist):
            if i == n-1:
                triallist.append(string[spanrange[0]:])
            else:
                triallist.append(string[spanrange[0]:iterlist[i+1][0]])
        for trialstring in triallist:
            trialstring = trialstring.strip()
            trialstring = trialstring.replace(",", "").strip()
            trialstring =re.sub(r'\n+',' ', trialstring)
            trialstring = re.sub(r'\s{2,}', ',', trialstring)
            cleaned_history.append(trialstring)
    
        for j, item in enumerate(cleaned_history):
            if 'Sold' in item:
                cleaned_history = cleaned_history[j:]
                break;
    
        for k, item in enumerate(cleaned_history):
            if ('Listed for sale' in item) and (k != len(cleaned_history)-1):
                cleaned_history = cleaned_history[: k+1]
                break;
        if len(cleaned_history) < 2:
            return [np.nan, np.nan]
        if not ('Sold'in cleaned_history[0]):
            return [np.nan, np.nan]
        elif not ('Listed for sale' in cleaned_history[-1]):
            return [np.nan, np.nan]
        else:
            pattern = re.compile(r'(\d+/\d+/\d+)')
            end_time = pattern.findall(cleaned_history[0])
            start_time = pattern.findall(cleaned_history[-1])
            for item in cleaned_history:
                if 'Pending' in item:
                    end_time = pattern.findall(item)
            print start_time, end_time
            return [start_time, end_time]
    
    
    
    
    
    
    def write_trulia_sold_temp_features(self):

    '''
    for all rows in 'incsvfile', create a list of temporary features 
    and write them to a temp csv
    returns the name of the temp csv file
    '''
        temp_outcsvfile = '/Users/chuntinglu/  \
             Desktop/datatest/sold_temp_features_'+zipcode+'.csv'
        self.temp_dfout.to_csv(temp_outcsvfile, encoding = 'utf-8', index = None)
        
        count = 0
        
        for (idx, row) in self.dfin.iterrows():
            
            count += 1
            if count%10 == 0:
                print count
            tempsoldfeatures = self.clean_sold_trulia(row)
            
            itemdf = pd.DataFrame([tempsoldfeatures], columns = self.temp_columns)
    
            itemdf.to_csv(temp_outcsvfile, encoding = 'utf-8', mode = 'a', header = False, index = None)
        
        return temp_outcsvfile
    
    
    
    def convert_time(self, time):

    '''
    helper function for write_trulia_sold_features
    '''
        if len(time) == 10:    
            return datetime.strptime(time, '%m/%d/%Y') 
        else:
            if len(time) == 12:
                time = time[1:-1]
                return datetime.strptime(time, '%m/%d/%Y') 
            else:
                return datetime.striptime('01/01/1900', '%m/%d/%Y')
            
    
    def get_duration(self, row):
    '''
    helper function for write_trulia_sold_features
    '''
        return (row['ending'] - row['starting']).days
    
    
    def write_trulia_sold_features(self):

    '''
    create a dataframe with cleaned features
    and write it to 'outcsvfile'
    '''
        
        
        temp_infile = self.write_trulia_sold_temp_features()
        
        sold = pd.read_csv(temp_infile)
        soldcopy = sold.copy()
        
        #soldcopy['yearbuilt_tillnow_t'] = soldcopy.yearbuilt_t.apply(get_yearbuilt_tillnow)
        soldcopy.dropna(subset = ['askingprice','start_date', 'end_date'], inplace = True)
        soldcopy['starting'] = soldcopy.start_date.apply(self.convert_time)
        soldcopy['ending'] = soldcopy.end_date.apply(self.convert_time)
        soldcopy['duration'] = soldcopy.apply(self.get_duration, axis = 1)
        soldcopy['weeks'] = soldcopy['duration']/7 + 1
        soldcopy['weeks'] = soldcopy.weeks.apply(int)
        soldcopy['sold'] = True
        
        outcsvfile = '/Users/chuntinglu/Desktop/datatest/sold_features_'+zipcode+'.csv'
        soldcopy.to_csv(outcsvfile, encoding = 'utf-8', index = None)
        
        
        
        
        
           
if __name__ == '__main__':
    #Murray Hills
    # zipcodes = ['10010', '10016', '10017','10022']
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
        truliasoldfeatures = TruliaSoldFeatures(zipcode)
        truliasoldfeatures.write_trulia_sold_features()
       
    