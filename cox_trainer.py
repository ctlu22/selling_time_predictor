import pandas as pd
import numpy as np
import re
import datetime
import csv
from lifelines import CoxPHFitter


class CoxTrainer:
    
    """
    trains a Cox regression model
    input: zipcodes and features that you would like to select
    For example, if you would like to perform basic subgroup analysis 
    for Murray Hill neighborhood,
    zipcodes = ['10016', '10017','10010', '10022']
    features = ['avg_sqft_t', 'weeks', 'sold', 'bathrooms']
    outputs a summary of the regression model,
    a plot that indicates the coefficients of features,
    and histogram for each of the features.
    """
    def __init__(self, zipcodes, features):
        self.zipcodes = zipcodes
        self.features = features
        
        
        self.df_for_test = pd.DataFrame(columns = features)
        self.cph = CoxPHFitter()
    
    def merge_zips(self):
        #path_prefix = '/Users/chuntinglu/Desktop/datatest/all_merged_2_'
        incsvfile = '/Users/chuntinglu/Desktop/datatest/zips_merged_3.csv' 
        zips_merged_df= pd.read_csv(incsvfile)
        dflist = [zips_merged_df[zips_merged_df ['zipcode'] == zipcode].copy()
                               for zipcode in zipcodes]
        cur_df = dflist[0]
        for i, zipcode in enumerate(zipcodes):
            if i > 0:
                cur_df = pd.concat([cur_df, dflist[i]])
        #outcsvfile = '/Users/chuntinglu/Desktop/datatest/zips_merged.csv'
        #df_origin.to_csv(outcsvfile, encoding = 'utf-8', index = None)
        return cur_df
        
   

    def transform_cur_df(self):
        self.df_for_test = self.merge_zips()
        
        self.df_for_test = self.df_for_test[self.features].copy()
        self.df_for_test = self.df_for_test.dropna()
    
    def get_test_df(self):
        return self.df_for_test
        
    
    def get_cph(self):
        return self.cph
    
    def fit_cox(self):
        #print "here"
        #print self.df_for_test.columns
        self.cph.fit(self.df_for_test, duration_col = 'weeks', event_col = 'sold')
        
    def print_cox_summary(self):
        self.cph.print_summary()
    
    def plot_cox_coefficients(self):
        self.cph.plot()
    
    def plot_hist(self):
        self.df_for_test.hist()
        
    def display_results(self):
        self.transform_cur_df()
        self.fit_cox()
        self.print_cox_summary()
        
        
if __name__ == '__main__':
    
    #Murray Hills
    #zipcodes = ['10016', '10017','10010', '10022']
    #Greenwich and Soho
    #zipcodes = ['10013', '10014']
    # Upper East Side
    #zipcodes = ['10021', '10028', '10065', '10075', '10128']
    # Upper West Side
    #zipcodes = ['10023', '10024', '10025']
    #Chelsea and Clinton
    #zipcodes = ['10001', '10019', '10036']
    
    
    coxtrainer = CoxTrainer(zipcodes, features)
    coxtrainer.display_results()