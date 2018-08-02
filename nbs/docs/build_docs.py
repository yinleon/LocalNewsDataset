import os
import pandas as pd
from IPython.core.display import HTML, display, Markdown, Latex

# common column definitions
website = 'The website of the media outlet exactly as we found it online.'
source = 'Where was this record scraped from?'
collection_date = 'when was this record collected?'
state = 'The two letter state abbreviation of the media outlet.'
owner = 'The corporate owner of the station.'
facebook = "The URL to the media outlet's Facebook presence."
youtube = "The URL to the media outlet's YouTube presence."
twitter_name = "The Twitter screen name of the news outlet."
twitter_url = "The URL to the Twitter screen name of the news outlet."
city = 'The name of the city that the TV station broadcasts from.'
station_name= 'The name of the TV station IE ("KRIV"). If anyone knows the origin of this naming convention, I would love to know!'
network = 'The franchise or brand name that the station belongs to IE Fox'
google = "The URL to the media outlet's Google Plus presence."


hearst_docs = {
    'columns': {
        'city' : city, 
        'facebook' : facebook, 
        'network' : network, 
        'state' : state, 
        'station' : station_name, 
        'twitter' : twitter_url, 
        'website' : website, 
        'broadcaster' : owner, 
        'source' : source, 
        'collection_date' : collection_date, 
    },
    "file" : '../data/hearst.tsv',
    "url" : 'TODO',
    "script" : 'TODO',
    "description" : 'An intermediate file of news outlets owned by Hearst scraped from their website'
}

meredith_docs = {
    'columns' : {
        'city' : city, 
        'facebook' : facebook, 
        'google' : google, 
        'network' : network, 
        'state' : state, 
        'station' : station_name, 
        'twitter' : twitter_url, 
        'website' : website, 
        'broadcaster' : owner, 
        'source' : source, 
        'collection_date' : collection_date,
    },
    "file" : '../data/meredith.tsv',
    "url" : 'TODO',
    "script" : 'TODO',
    "description" : 'An intermediate file of news outlets owned by Meredith scraped from their website'
}

nexstar_docs = { 
    'columns' : {
        'station' : station_name, 
        'website' : website, 
        'city' : city, 
        'state' : state, 
        'broadcaster' : owner, 
        'source' : source,
        'collection_date' : collection_date
    },
    "file" : '../data/nexstar.tsv',
    "url" : 'TODO',
    "script" : 'TODO',
    "description" : 'An intermediate file of news outlets owned by Nexstar scraped from their website'
}

sinclair_docs = {
    'columns' : {
        'city' : city, 
        'geo' : 'The raw geolocation field from the website. We parse this field to get `city` and `state`', 
        'network' : network, 
        'state' : state, 
        'station' : station_name, 
        'website' : website, 
        'broadcaster' : owner, 
        'source' : source, 
        'collection_date' : collection_date, 
    },
    "file" : '../data/sinclair.tsv',
    "url" : 'TODO',
    "script" : 'TODO',
    "description" : 'An intermediate file of news outlets owned by Sinclair scraped from their website'
}

tribune_docs = {
    'columns' : {  
        'city' : city, 
        'facebook' : facebook, 
        'network' : network, 
        'station' : station_name, 
        'twitter' : twitter_url, 
        'website' : website, 
        'youtube' : youtube, 
        'broadcaster' : owner, 
        'source' : source, 
        'state' : state, 
        'collection_date' : collection_date ,
    },
    "file" : '../data/tribune.tsv',
    "url" : 'TODO',
    "script" : 'TODO',
    "description" : 'An intermediate file of news outlets owned by Tribune scraped from their website.'
}


station_index_docs = {
    'columns' : {  
        'city' : city, 
        'id' : 'The human-recognizable name for the TV station.', 
        'owner' : owner, 
        'state' : state, 
        'station_info' : 'Typically related to the frequency of the transmission', 
        'station_name' : station_name, 
        'subchannels' : 'Alternative names for the TV station', 
        'website' : website, 
        'source' : source, 
        'collection_date' : collection_date, 
    },
    "file" : '../data/station_index.tsv',
    "url" : 'TODO',
    "script" : 'TODO',
    "description" : 'An intermediate file of TV stations compiled on stationindex.com. The website is scraped according to the market (reigon), and again according to the owner. The two scraped datasets are merged and duplicates are dropped. When dropping duplicates, precedence is given to the entry scraped owners.'
    
}

usnpl_docs = { 
    'columns' : {   
        'Facebook' : facebook, 
        'Geography' : state, 
        'Medium' : 'Whether the news outlet us a newspaper (includes online), magazine, or college newspaper.', 
        'Name' : station_name, 
        'Twitter_Name' : twitter_name, 
        'Website' : website, 
        'Youtube' : youtube, 
        'source' : source, 
        'collection_date' : collection_date
    },
    "file" : '../data/usnpl.tsv',
    "url" : 'TODO',
    "script" : 'TODO',
    "description" : 'An intermediate file of News papers, magazines and college papers compiled by usnpl.com. The website is scraped by visiting state-specific pages using requests and BeautifulSoup, websites and social media are collected wherever possible.'
}

output_docs = {
    'columns' : {
        'name' : station_name, 
        'state' : state, 
        'website' : website, 
        'domain' : 'The domain that houses the media outlet. It is standardized (no "www" or "http://"). Sometimes multiple media outlets direct to the same domain (but seprate sub-domain).', 
        'twitter' : twitter_name, 
        'youtube' : youtube, 
        'facebook' : facebook, 
        'owner' : owner, 
        'medium' : 'Whether the news outlet us a newspaper (includes online), magazine or a TV station', 
        'source' : source, 
        'collection_date' : collection_date,
    },
    "file" : '../data/local_news_dataset_2018.csv',
    "url" : 'TODO',
    "script" : 'TODO',
    "description" : 'The intermediaries are merged (using this script), and preprocessed resulting in this file',
    "sep" : ','
}

docs = [
    sinclair_docs,
    meredith_docs,
    nexstar_docs,
    hearst_docs,
    tribune_docs,
    station_index_docs,
    usnpl_docs,
]

table_header = '''| Column Name | Description | N Unique Values |
| --- | --- | --- |'''

intro_markdown = '''## Inventory
These are the files in the `../data/` folder.

### Outputs
- [local_news_dataset_2018.csv](#local_news_dataset_2018)
'''

def generate_docs_for_dataset(doc_dict, return_to_top=True):
    '''
    Given a dictionary, this properly formats the documentation!
    '''
    # Introduction
    filename = os.path.basename(doc_dict['file']).split('.')[0]
    display(Markdown(f"## <a name='{filename}'>{filename}.tsv</a>"))
    display(Markdown(doc_dict['description']))
    display(Markdown(f"Read the raw file from this URL: \n `{doc_dict['url']}`\n"))
    display(Markdown(f"See the code used to make this dataset: \n `{doc_dict['script']}`\n"))
    display(Markdown(''))

    
    # sample of the data
    display(Markdown("#### What Does the Data Look Like?"))
    df = pd.read_csv(doc_dict['file'], sep=doc_dict.get('sep', '\t'))
    display(Markdown(f"Sample of `{doc_dict['file']}` (N = {len(df)})"))
    display(df.sample(3, random_state=303).reset_index(drop=True))
    display(Markdown(''))

    
    # columns
    doc_string = ''
    doc_string = "#### What do the columns mean?" + '\n'
    doc_string += table_header + '\n'
    for k, v in doc_dict.get('columns').items():
        doc_string += f"| `{k}` | {v} | {len(df[k].unique())} |" + '\n'
    display(Markdown(doc_string))
    display(Markdown(''))
    if return_to_top:
        display(Markdown('[Top of Data Sheet](#datasheet)'))
    display(Markdown(''))
  
def generate_intro():
    display(Markdown(intro_markdown))
    table_of_contents = '### Intermediates \n'
    for dataset in docs:
        filename = os.path.basename(dataset['file']).split('.')[0]
        table_of_contents += f" - [{filename}.tsv](#filename)\n"
    display(Markdown(table_of_contents))
    display(Markdown('<hr>'))
        

import plotly.plotly as py

def plot_chloro(df, title=''):
    scl = [# Let first 10% (0.1) of the values have color rgb(0, 0, 0)
        [0, 'rgb(180, 180, 180)'],
        [0.1, 'rgb(180, 180, 180)'],
        
        [0.1, 'rgb(160, 160, 160)'],
        [0.2, 'rgb(160, 160, 160)'],
        [0.2, 'rgb(140, 140, 140)'],
        [0.3, 'rgb(140, 140, 140)'],

        [0.3, 'rgb(120, 120, 120)'],
        [0.4, 'rgb(120, 120, 120)'],

        [0.4, 'rgb(100, 100, 100)'],
        [0.5, 'rgb(100, 100, 100)'],

        [0.5, 'rgb(80, 80, 80)'],
        [0.6, 'rgb(80, 80, 80)'],

        [0.6, 'rgb(60, 60, 60)'],
        [0.7, 'rgb(60, 60, 60)'],

        [0.7, 'rgb(40, 40, 40)'],
        [0.8, 'rgb(40, 40, 40)'],

        [0.8, 'rgb(20, 20, 20)'],
        [0.9, 'rgb(20, 20, 20)'],

        [0.9, 'rgb(0, 0, 0)'],
        [1.0, 'rgb(0, 0, 0)']]
    
    # wrangle the dataset
    vals = df.state.value_counts()
    states =vals.index
    counts = vals.values
    
    # set up annotations
    text = []
    for state in states:
        calc = df[df['state'] == state]['medium'].value_counts()
        desc = '<b>Breakdown by Medium:</b><br>'
        for k,v in calc.items():
            desc += f'{k} = {v}<br>'
        
        calc = df[df['state'] == state]['owner'].value_counts().head(5)
        desc += '<b>Top 5 Media Owners:</b><br>'
        for k,v in calc.items():
            desc += f'{k} = {v}<br>'
            
        text.append(desc)


    data = [ dict(
            type='choropleth',
            colorscale = scl,
            autocolorscale = False,
            locations = states,
            z = vals,
            locationmode = 'USA-states',
            text = text,
            marker = dict(
                line = dict (
                    color = 'rgb(255,255,255)',
                    width = 2
                ) ),
            colorbar = dict(
                title = "Number of News Outlets Per State")
            ) ]

    layout = dict(
            title = title,
            geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showlakes = True,
                lakecolor = 'rgb(255, 255, 255)'),
                )

    fig = dict( data=data, layout=layout )
    return py.iplot(fig, filename='d3-cloropleth-map' )

def chloropleth():
    
    display(Markdown('Below is an interactive [Plot.ly](https://plot.ly) chloropleth map of state-level representation in this dataset. Scroll over each state to get a list of the top mediums and owners.'))
    df = pd.read_csv(output_docs['file'])
    display(plot_chloro(df, title = 'Coverage of State-Level Media Outlets from the Local News Dataset'))
 

def summary_stats():
    df = pd.read_csv(output_docs['file'])
        
    display(Markdown('#### Breakdown of mediums in the Local News Dataset'))
    display(df.medium.value_counts().to_frame())
    display(Markdown(''))
    
    display(Markdown('#### Breakdown of data sources in the Local News Dataset'))
    display(df.source.value_counts().to_frame())
    display(Markdown('`User Input` are custom additions added from the contents of [this JSON file](#TODO) in [this section](#TODO) of the `merge.py'))
    display(Markdown(''))



def generate_docs():
    # generate intro
    generate_intro()

    # generate dataset docs:
    for dataset in docs:
        generate_docs_for_dataset(dataset)
    
    # output details
    generate_docs_for_dataset(output_docs, return_to_top=False)
    summary_stats()
    chloropleth()
    
    