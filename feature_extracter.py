import pandas as pd
import numpy as np
import re
import datetime
import csv
import spacy
import textacy
import en_core_web_sm




class FeatureExtracter:
    """
    This class takes the basic features generated in the "webscraping and basic features"
    folder as input and generate more features (e.g. textual).
    Input is provided in the repository as zips_merged_2.csv.
    You have to specify your output directory to store the results.
    
    """
    
    def __init__(self, incsvfile):
        
        
        self.incsvfile = incsvfile
        self.df = pd.read_csv(incsvfile)
    
    
        
    def get_time_year(self, row):
        if np.isnan(row.ending):
            return np.nan
        else:
            return (row.ending.split("-")[0], "-".join(string.split("-")[:-1]))
    
    
    def get_newer_buildings(self, row):
       """
       returns if a building is less than 10 years old
       """
        if np.isnan(row.year_till_now):
            return np.nan
        else:
            return (row.year_till_now < 10)
    
    def drop_long_weeks(self):
        self.df['long_weeks'] = self.df.weeks.apply(lambda x: x>= 110)
        self.df = self.df.drop(['long_weeks'], axis = 1)
        
    def revise_description(self,row):
        if np.isnan(row.description):
            return np.nan
        elif 'This property is no longer available to rent or buy' in row.description:
            split_list = re.split(r'\s{2,}', row.description)
            if len(split_list) > 1:
                return split_list[1]
            else:
                return np.nan
        else:
            return row.description
        
    def get_revised_description(self):
        self.df['revised_description'] = self.df.apply(self.revise_description, axis = 1)
        
        
    def create_descriptionlist(self, row):
    
        try:
            row.revised_description.decode('utf-8')
        except UnicodeError:
            print "string is not UTF-8"
        return np.nan
        
        content = unicode(row.revised_description, "utf-8")
        doc = textacy.Doc(content)
        termslist = list(doc.to_terms_list(ngrams = 1, as_strings = True))
        return terms
     
    def get_descriptionlist(self):
        self.df['description_list'] = self.df.apply(self.create_descriptionlist, axis = 1)
        
    
    
    def create_sold_words(self):
        sold_words = ['subway', 'condo', 'assessment', 'alcove', 'train', 'bus', 'deck',
             'hill', 'transportation', 'king', 'roof', 'newly', 'pet', 'doorman', 'monthly',
             'location', 'laundry']
        for word in sold_words:
             self.df[word] = self.df.description_list.apply(lambda x: int(word in x))

    def create_sale_words(self):
        forsale_words = ['residence', 'term', 'suite', 'design', 'bath','interior', 'file',
                'offering', 'master', 'heated', 'radiant', 'slab', 'backsplash', 
                'miele', 'oak', 'art', 'island', 'ceiling', 'en', 'vanity',
                'height', 'penthouse', 'collection', 'lead']
        for word in forsale_words:
            self.df[word] = self.df.description_list.apply(lambda y: int(word in y))
    
    
    
        


    
    
    
    def write_csv(self):
        
        """
        replace the outcsvfile with your local directory
        """
        self.drop_long_weeks()
        self.df['newer_buildings'] = self.df.apply(self.get_newer_buildings, axis = 1)
        self.get_revised_description()
        self.get_descriptionlist()
        self.create_sold_words()
        self.create_sale_words()
        
        outcsvfile = '/Users/chuntinglu/Desktop/datatest/zips_merged_3.csv' 
                     
        
        self.df.to_csv(outcsvfile, encoding = 'utf-8', index = None)
        
    
if __name__ == '__main__':
    
    """
    replace the incsvfile with your local directory which 
    stores the zips_merged_2.csv provided in the repository
    """
    incsvfile = '/Users/chuntinglu/Desktop/datatest/zips_merged_2_' + zipcode +'.csv'
    featureextracter = FeatureExtracter(incsvfile)
    featureextracter.write_csv()
        
        
        
        
        