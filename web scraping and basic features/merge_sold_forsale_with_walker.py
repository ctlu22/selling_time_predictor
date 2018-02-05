import pandas as pd
import numpy as np
import re
import datetime
import urllib
import csv
import requests
import time
from bs4 import BeautifulSoup



class MergeSoldForSaleWithWalker:
    '''
    Merge sold and for sale condos together with walkscore
    '''
    
    def __init__(self, zipcode):
        self.zipcode = zipcode
        incsvfile_sold = '/Users/chuntinglu/Desktop/datatest/sold_merged_1_' + 
                           self.zipcode + '.csv'
        incsvfile_forsale = '/Users/chuntinglu/Desktop/datatest/forsale_merged_1_' +
                           self.zipcode + '.csv'
        
        self.columnslist = ['zpid','street', 'latitude', 'longitude','yearbuilt',
                           'taxAssYear', 'taxAss', 'finishedsqft', 'bathrooms',
                           'bedrooms', 'totalrooms', 'zindex', 'url', 'overview',
                           'askingprice', 'description', 'sqft_t', 'avg_sqft_t',
                           'zipcode', 'duration', 'weeks', 'sold', 'starting','ending',
                        'median_avg_sqft', 'walkscore']
        self.df_sold = pd.read_csv(incsvfile_sold)
        self.df_forsale = pd.read_csv(incsvfile_forsale)
        
        medianzipcodefile = '/Users/chuntinglu/Desktop/datatest/zip_median.csv'
        self.median_zip = pd.read_csv(medianzipcodefile)
        self.median_sale_price = 0
        self.median_sold_price_current_month = 0
        
    def compute_year_tillnow(self,row):
        try:
            return int(2018 - row.yearbuilt)
        except ValueError:
            return np.nan 
        
    def set_median_zip(self):
        self.median_zip['zip'] = self.median_zip.RegionName.apply(lambda s:
                                                                  str(s).strip())
        self.median_zip.set_index('zip', inplace = True)
        
    
    def get_time_year(self, string):
        return (string.split("-")[0], "-".join(string.split("-")[:-1]))
    
    def get_end_time_year(self, row):
        return self.get_time_year(row.ending)[1]
    
    def get_median_soldprice_current_month(self):
        tempsolddf = self.df_sold[['ending', 'avg_sqft_t']].copy()
        
        
        tempsolddf['year_month'] = tempsolddf.apply(self.get_end_time_year, 
                                   axis = 1)
        cropped_tempsolddf = tempsolddf[tempsolddf['year_month'] == '2018-01']
        cropped_tempsolddf.dropna(inplace = True)
        
        print cropped_tempsolddf.avg_sqft_t.median()
        return cropped_tempsolddf.avg_sqft_t.median()
    
    
    
    def get_median_price(self,row):
        median_saleprice = self.get_median_saleprice()
        median_soldprice_current_month = self.get_median_soldprice_current_month()
        time_year = self.get_time_year(row.ending)
        if int(time_year[0].strip()) < 2015:
            print "Probelm with price history"
            return np.nan
        else:
            if time_year[1].strip() == '2018-01':
                return median_soldprice_current_month
            return self.median_zip.loc[self.zipcode][time_year[1].strip()]
    
    def get_median_saleprice(self):
        tempdf = self.df_forsale['avg_sqft_t'].copy()
        tempdf.dropna(inplace = True)
        print tempdf.median()
        
        return tempdf.median()
        
    def get_start_date_forsale(self, row):
        
        days_between = int(row.duration)
        return row.ending - datetime.timedelta(days = days_between)
    
    
    def write_csv(self):
        self.set_median_zip()
        today = '2018-01-24'
        self.df_forsale['ending'] = 
                 datetime.datetime.strptime(today, "%Y-%m-%d").date()
        self.df_forsale['starting'] = 
                 self.df_forsale.apply(self.get_start_date_forsale, axis = 1)
        self.df_forsale['median_avg_sqft'] = self.get_median_saleprice()
        self.df_sold['median_avg_sqft'] = 
                 self.df_sold.apply(self.get_median_price, axis = 1)
        
        df_sold_copy = self.df_sold[self.columnslist].copy()
        df_forsale_copy = self.df_forsale[self.columnslist].copy()
        df = pd.concat([df_sold_copy, df_forsale_copy])
        df['year_till_now'] = df.apply(self.compute_year_tillnow, axis = 1)
        outcsvfile = '/Users/chuntinglu/Desktop/datatest/all_merged_2_' + self.zipcode +'.csv'
        df.to_csv(outcsvfile, encoding = 'utf-8', index = None)
        
if __name__ == '__main__':
    #Murray Hills

    #zipcodes = ['10016','10017','10010', '10022' ]
    #zipcodes = ['10014']
    #Greenwich and Soho
    #zipcodes = ['10013', '10014']
    # Lower Manhattan skipped
    #zipcodes = ['10005', '10007', '10038', '10280']
    #zipcodes = '10280'
    # Lower East Side skipeed
    #zipcodes = ['10003']
    # Upper East Side
    #zipcodes = ['10065']
    #zipcodes = ['10021', '10028', '10065', '10075', '10128']
    # Upper West Side
    #zipcodes = ['10023', '10024', '10025']
    #Central Harlem
    #zipcodes = ['10026']
    #Chelsea and Clinton
    #zipcodes = ['10001', '10019', '10036']
    
    for zipcode in zipcodes:
        print zipcode
        mergesoldforsalewithwalker = MergeSoldForSaleWithWalker(zipcode)
        mergesoldforsalewithwalker.write_csv()
        