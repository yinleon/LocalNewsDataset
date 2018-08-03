import re
import requests
import time

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import pandas as pd
from tqdm import tqdm as tqdm
from bs4 import BeautifulSoup

from config import *

'''
This script contains scrapers for tribune, sinclair, nexstar, hearst, stationindex, and usnpl.

Metadata about the stations in each of the stations is saved as tsvs.

Note that these scrapers are super similar codebases!

Written By Leon Yin
On 2018-05-31
Updated 2018-08-02
'''


def download_tribune():
    '''Scrapes ther Tribune homepage.'''
    def parse_channel_html(channel_html, website=None):
        '''Parses bs4 html to create a dictionary (row in the dataset)'''
        if website == None:
            website = channel_html.find('a').get('href')
        station = channel_html.find('div', class_='q_team_title_holder').find("h3").text
        city = channel_html.find('div', class_='q_team_title_holder').find('span').text
        social = channel_html.find('div', class_='q_team_social_holder')
        network = None
        
        row = dict(
            network = network,
            city = city,
            website = website,
            station = station,
        )

        if social:
            for s in social.find_all('span', class_='q_social_icon_holder normal_social'):
                link = s.find('a').get('href')
                if 'facebook' in link:
                    row['facebook'] = link
                elif 'twitter' in link:
                    row['twitter'] = link
                elif 'youtube' in link:
                    row['youtube'] = link
        return row
    
    print("Downloading Tribune")
    url = 'http://www.tribunemedia.com/our-brands/'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    tables = soup.find_all('div', class_='vc_row wpb_row section vc_row-fluid ')
    channels = soup.find_all('div', class_='wpb_wrapper')

    metadata = []
    for i, channel in tqdm(enumerate(channels)):
        try:
            channel_meta = parse_channel_html(channel)
            metadata.append(channel_meta)
        except:
            try:
                website = channels[i-8].find('a').get('href')
                channel_meta = parse_channel_html(channel, website)
                metadata.append(channel_meta)
            except:
                print(i)

    df = pd.DataFrame(metadata)
    df['broadcaster'] = 'Tribune'
    df['source'] = 'tribunemedia.com'
    df['state'] = df['city'].replace(city_state)
    df['collection_date'] = today
    update = 1
    
    if os.path.exists(tribune_file):
        # appending to old
        df_ = pd.read_csv(tribune_file, sep='\t')
        df = df[~df['station'].isin(df_['station'])]
        df = df_.append(df)
   
    df.to_csv(tribune_file, index=False, sep='\t')


def download_sinclair():
    '''Scrapes ther Sinclair homepage.'''
    def camel_split(text):
        geo_split = re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', text)
        state = geo_split[-1]
        city = ' '.join(geo_split[:-1])
        return city, state

    def parse_channel_html(channel_html):
        '''Parses bs4 html to create a dictionary (row in the dataset)'''
        network = channel_html.get('class')[2]
        city, state = camel_split(channel_html.get('class')[-2])
        website = channel_html.find('a', class_='work-image').get('href')
        if website == 'http://sbgi.net':
            website = None
        station = channel_html.find('span', class_='callLetters').text
        geo = channel_html.find('span', class_='cityState').text.replace(' - ', '')

        row = dict(
            network = network,
            city = city,
            state = state,
            website = website,
            station = station,
            geo = geo
        )

        return row
    
    print("Downloading Sinclair")
    url = 'http://sbgi.net/tv-channels/'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    port = soup.find('div', class_='portfolio')
    channels = port.find_all('div', class_=re.compile('^item five*'))
    metadata = []
    for channel in tqdm(channels):
        try:
            channel_meta = parse_channel_html(channel)
            metadata.append(channel_meta)
        except:
            print(channel)

    df = pd.DataFrame(metadata)
    df['broadcaster'] = 'Sinclair'
    df['source'] = 'sbgi.net'
    df['collection_date'] = today
    
    if os.path.exists(sinclair_file):
        # appending to old
        df_ = pd.read_csv(sinclair_file, sep='\t')
        df = df[~df['station'].isin(df_['station'])]
        df = df_.append(df) 
        
    df.to_csv(sinclair_file, index=False, sep='\t')


def download_nexstar():
    '''Scrapes ther Nexstar homepage.'''
    def get_geo(row):
        row = row.replace('  (3)', '')
        state = row.split(',')[-1]
        city = row.replace(',' + state, '')

        state = state.strip()
        return city, state
    
    def fix_up_mismatched_stations(row):
        '''
        The table that the Nexstar dataset is scraped from is no aligned.
        This is a way to automate alignment
        '''
        stations = row['station'].split()
        websites = row['website'].split()

        if len(stations) > 1:
            if len(websites) == 1:
                # if there is one website it applies to all the stations
                for station in stations:
                    row_ = row.copy()
                    row_['station'] = station
                    yield row_

            elif len(stations) == len(websites):
                # if the number of websites is equal to that of the stations,
                # we can just align them like this
                for s, w in zip(stations, websites):
                    row_ = row.copy()
                    row_['station'] = s
                    row_['website'] = w
                    yield row_

            else:
                # These are the hardest to align, we make a make a manual mapping
                # and map the correct station to the website
                for w in websites:
                    custom_mapping = nexstar_alignment.get(w)
                    if custom_mapping:
                        for s in custom_mapping:
                            row_ = row.copy()
                            row_['station'] = s
                            row_['website'] = w
                            yield row_
                    else:
                        print(f"{w} is an edge case that needs to be updated on `nexstar_mapping`")
        else:
            yield row
    
    print("Downloading Nexstar")
    url = 'https://www.nexstar.tv/stations/'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    table = soup.find('table', class_='tablepress tablepress-id-1 dataTable no-footer tablepress--responsive')
    df = pd.read_html(str(table))[0]
    df['city'], df['state'] = zip(*df['Market'].apply(get_geo))
    df.columns = [cols_standard_nexstar.get(c, c) for c in df.columns]
    df['broadcaster'] = 'Nexstar'
    df['source'] = 'nexstar.tv'
    df = df[cols_nexstar]
    df['collection_date'] = today
    
    # align stations and websites! many to one relationship per row...
    data = []
    for i, row in df.iterrows():
        for _ in fix_up_mismatched_stations(row):
            data.append(_)
    df = pd.DataFrame(data)
    
    if os.path.exists(nexstar_file):
        # appending to old
        df_ = pd.read_csv(nexstar_file, sep='\t')
        df = df[~df['station'].isin(df_['station'])]
        df = df_.append(df) 
        
    df.to_csv(nexstar_file, sep='\t', index=False)
    

def download_meredith():
    '''Scrapes ther Meredith homepage.'''
    def parse_channel_html(channel_html):
        '''Parses bs4 html to create a dictionary (row in the dataset)'''
        station = channel_html.get('data-station-name')
        geo = channel_html.find('div', class_='city').text
        city, state = geo.split(', ')
        website = channel_html.find('div', class_='links').find('a').get('href')
        try:
            facebook = channel_html.find('a', class_='icon-FACEBOOK icon').get('href')
        except:
            facebook = None
        try:
            google = channel_html.find('a', class_='icon-GOOGLE icon').get('href')
        except:
            google = None
        try:
            twitter = channel_html.find('a', class_='icon-TWITTER icon').get('href')
        except:
            twitter = None 

        data = dict(
            station = station,
            city = city,
            state = state,
            website = website,
            network = None,
            facebook = facebook,
            twitter = twitter,
            google = google
        )

        return data
    
    print("Downloading Meredith")
    url = 'http://www.meredith.com/local-media/broadcast-and-digital'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    channels = soup.find_all('li', class_=re.compile('^dot station-id-*'))
    metadata = []
    for i, channel in tqdm(enumerate(channels)):
        channel_meta = parse_channel_html(channel)
        metadata.append(channel_meta)
    df = pd.DataFrame(metadata)
    df['broadcaster'] = 'Meredith'
    df['source'] = 'meridith.com'
    df['collection_date'] = today
    
    if os.path.exists(meredith_file):
        # appending to old
        df_ = pd.read_csv(meredith_file, sep='\t')
        df = df[~df['station'].isin(df_['station'])]
        df = df_.append(df) 
        
    df.to_csv(meredith_file, index=False, sep='\t')


def download_hearst():
    '''Scrapes ther Hearst homepage.'''
    def parse_channel_html(channel_html):
        '''Parses bs4 html to create a dictionary (row in the dataset)'''
        website = channel_html.find('a').get('href')
        station = channel_html.find('h3').text
        geo = channel_html.find('div', class_='freeform').text.strip()
        state = geo.split(',')[-1].strip().upper()
        city = ' '.join(geo.split(',')[:-1]).strip().replace('\r\n', '')

        try:
            twitter = channel_html.find('a', class_='circle-icon share-twitter').get('href')
        except:
            twitter = None
        try:
            fb = channel_html.find('a', class_='circle-icon share-fb').get('href')
        except:
            fb = None

        network = None

        context = dict(
            network = network,
            city = city,
            state = state,
            website = website,
            station = station,
            twitter = twitter,
            facebook = fb
        )

        return context
    
    print("Downloading Hearst")
    url = 'http://www.hearst.com/broadcasting/our-markets'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    channels = soup.find_all('div', class_='td')
    metadata = []
    for i, channel in tqdm(enumerate(channels)):
        channel_meta = parse_channel_html(channel)
        metadata.append(channel_meta)
    df = pd.DataFrame(metadata)
    df['broadcaster'] = 'Hearst'
    df['source'] = 'hearst.com'
    df = df.iloc[:33]
    df['collection_date'] = today
    
    if os.path.exists(hearst_file):
        # appending to old
        df_ = pd.read_csv(hearst_file, sep='\t')
        df = df[~df['station'].isin(df_['station'])]
        df = df_.append(df) 
    
    df.to_csv(hearst_file, index=False, sep='\t')

    
def download_stationindex():
    '''
    stationindex has metadata about many tv stations in different states.
    '''
    def parse_station(row):
        '''Parses bs4 html to create a dictionary (row in the dataset)'''
                
        station_name = row.find_all('td')[1].find('a').text
        spans = row.find('td', attrs={'width':'100%'}).find_all('span', attrs={"class":'text-bold'}) 
        row = {'station' : station_name}
        for span in spans:
            # each span becomes a different column:
            col_name = span.text.rstrip(':').strip(' ').replace(' ', '_').lower().replace('web_site', 'website')
            val = span.next_sibling
            if col_name == 'website':
                # this needs to be validateed, 
                # there are some incorrect strings being passed as URLs
                val = val.next_sibling.text
            if col_name == 'city':
                state = val.split(', ')[-1]
                val = val.split(', ')[0]
                row['state'] = state
            row[col_name] = val

        return row
    
    print("Downloading StationIndex")
    tv_markets = [
        'http://www.stationindex.com/tv/tv-markets',
        'http://www.stationindex.com/tv/tv-markets-100'
    ]

    market_urls = []
    for url in tv_markets:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')
        table = soup.find('table', attrs={'class' : 'table table-striped table-condensed'})
        urls = ['http://www.stationindex.com' + _.get('href') for _ in table.find_all('a')]
        market_urls.extend(urls)

    data = []
    for url in tqdm(market_urls):
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')
        rows = soup.find_all('tr')
        data.extend([parse_station(row) for row in rows])     

    df = pd.DataFrame(data)
    df['source'] = 'stationindex'
    df['collection_date'] = today

    if os.path.exists(stationindex_file):
        # appending to old
        df_ = pd.read_csv(stationindex_file, sep='\t')
        df = df[~df['station'].isin(df_['station'])]
        df = df_.append(df) 
        
    df.to_csv(stationindex_file, index=False, sep='\t')

    
def download_usnpl():
    '''
    usnpl has metadata about many newspapers in different states.
    '''
    def parse_row(soup):
        '''
        For each media publication in the html, 
        we're going to strip the city name, the publication name,
        the website url, and social links (if they exist)

        The input `soup` is a beautiful soup object.
        the output is a dict of the parsed fields.
        '''
        city = soup.find('b').text
        name = soup.find('a').text
        web = soup.find('a').get('href')

        fb = soup.find('a', text='F')
        if fb:
            fb= fb.get('href')
        tw = soup.find('a', text='T')
        yt =soup.find('a', text='V')
        if yt:
            yt = yt.get('href')
        if tw:
            tw=tw.get('href').replace('http://www.twitter.com/', '').rstrip('/')

        return {
            'Facebook' : fb,
            'Twitter_Name' : tw,
            'Youtube' : yt,
            'Name' : name,
            'Website' : web
        }
    
    print("Downloading USNPL")
    sites = []
    for state in states:
        url = 'http://www.usnpl.com/{}news.php'.format(state)
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')

        data_possibilities = soup.find_all('div' ,{"id" : 'data_box'})
        for i, raw_table in enumerate(data_possibilities[1:]):
            j = 1 if i == 0 else 0
            medium = raw_table.find('h3').text
            if medium == 'Newspapers':
                data_table = str(raw_table).split('<br/><br/>\n</div>\n')[j]
                entries_to_parse = data_table.rstrip('</div>').split('\n<br/>\n')
            elif medium in ['Magazines', 'College Newspapers']:
                data_table = str(raw_table).split('<title>Untitled Document</title>')[1]
                entries_to_parse = data_table.rstrip('</div>').split('\n<br/>\n')
            else:
                break

            for row in tqdm(entries_to_parse):
                row = row.strip('\r').strip('\n')
                if row:
                    entry = parse_row(BeautifulSoup(row, 'lxml'))
                    entry['Geography'] = state.upper()
                    entry['Medium'] = medium
                    sites.append(entry)
            time.sleep(1)
    df = pd.DataFrame(sites)
    df['Website'] = df['Website'].str.rstrip('/')
    df['source'] = 'usnpl.com'
    df['collection_date'] = today
    
    if os.path.exists(usnpl_file):
        # appending to old
        df_ = pd.read_csv(usnpl_file, sep='\t')
        df = df[~df['Name'].isin(df_['Name'])]
        df = df_.append(df) 
    
    df.to_csv(usnpl_file, index=False, sep='\t')
    
    
def download_all_datasets():
    '''
    Downloads datasets from the 7 sources.
    '''
    download_hearst()
    download_meredith()
    download_nexstar()
    download_sinclair()
    download_tribune()
    download_stationindex()
    download_usnpl()
    
if __name__ == "__main__":
    download_all_datasets()
    