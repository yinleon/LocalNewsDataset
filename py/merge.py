import re
import json

import pandas as pd
from tqdm import tqdm as tqdm
import urlexpander

from config import *

'''
After downloading metadata bout state-level media outlets, this script can be run
to merge rows and standardize the columns.

Leon Yin
2018-05-31
'''

def remove_www(site_str):
    '''
    Best attempt to standardize websites.
    '''
    if site_str:
        return site_str.replace('www.', '').replace('http://', '').replace('https://', '').rstrip('/')
    else: return site_str

   
def load_custom_stations(filepath):
    '''Reads a json file with custom station info.'''
    data = []
    with open(filepath, 'r') as f:
        for row in f: 
            data.append(json.loads(row))
    df_ = pd.DataFrame(data)
    df_['collection_date'] = today
    
    return df_

def get_domain(url):
    '''Returns the domain name for any given url.'''
    if isinstance(url, str):
        return urlexpander.get_domain(url) 
    
def process_twitter_name(name):
    '''cleans up twitter name fields'''
    if isinstance(name, str):
        return name.split('/twitter.com/')[-1].lstrip('@')

def merge_stations():
    '''
    To be run after `download_data.py`, opens the newly downloaded TV station data, and returns a merged dataframe.
    '''
    # load the files
    df_stationindex = pd.read_csv(stationindex_file, sep='\t')
    df_meridith = pd.read_csv(meredith_file, sep='\t')
    df_nexstar = pd.read_csv(nexstar_file, sep='\t')
    df_sinclair = pd.read_csv(sinclair_file, sep='\t')
    df_hearst = pd.read_csv(hearst_file, sep='\t')
    df_tribune = pd.read_csv(tribune_file, sep='\t')
    
    # fix-up col names and owner names
    df_stationindex.columns = [station_index_mapping.get(c, c) for c in df_stationindex.columns]
    df_stationindex.broadcaster = df_stationindex.broadcaster.replace(owner_mapping)
    
    # merge the files
    df_super = (df_stationindex.append(df_meridith)
                    .append(df_nexstar)
                    .append(df_tribune)
                    .append(df_hearst)
                    .append(df_sinclair))
    
    # standardize the domain names
    df_super['website_standard'] = df_super['website'].fillna('').apply(remove_www)

    # Here we're dropping duplicates (prioritizing parent company info)
    df_tv = pd.DataFrame()
    for state, df_ in df_super.groupby('state'):
        #if state == 'MO':
        #    df_ = df_[df_['website_standard']!='fox4kc.com']
        df_tv = df_tv.append(
            df_.drop_duplicates(subset=['station', 'website_standard'], 
                                keep='last'))
    
    # set some new columns
    df_tv['medium'] = 'TV station'
    df_tv['state'] = df_tv['state'].replace(look_up)
        
    return df_tv


def merge_tv_and_media():
    '''
    Takes merged station data and newspapers and joins them together.
    '''
    # load files
    df_tv = merge_stations()
    df_usnpl = pd.read_csv(usnpl_file, sep='\t')
    df_custom = load_custom_stations(custom_station_file)
    
    # add new columns
    df_usnpl['source'] = 'usnpl.com'
    df_custom['source'] = 'User Input'
    df_usnpl['owner'] = None # this can be a future function that looks up known owners.
    
    # normalize column names
    df_usnpl.columns = [c.lower() for c in df_usnpl.columns]
    df_usnpl.columns = [col_standard.get(c, c) for c in df_usnpl.columns]
    df_tv.columns = [col_standard.get(c, c) for c in df_tv.columns]
    df_custom.columns = [col_standard.get(c, c) for c in df_custom.columns]
    
    # append the dataframes
    df_state = df_tv[cols].append(df_usnpl[cols])
    df_state = df_state[cols].append(df_custom[cols])
    
    # create a domain column
    df_state['domain'] = df_state['website'].apply(get_domain)
    df_state['twitter'] = df_state['twitter'].apply(process_twitter_name)
    df_state['state'] = df_state['state'].str.upper()
    
    # write the results to a csv
    df_state[cols_final].to_csv(local_news_dataset_file.replace('.csv', '_with_national.csv'), index=False)
    
    # filter out national domains 
    filter_out = urlexpander.datasets.load_us_national_media_outlets().tolist()
    df_state = df_state[~df_state['domain'].isin(filter_out)]
    
    df_state['owner'] = df_state['owner'].str.lstrip(' ')
    
    # write the results to a csv
    df_state[cols_final].to_csv(local_news_dataset_file, index=False)
    
if __name__ == "__main__":
    merge_tv_and_media()
