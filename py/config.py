import os
import datetime

# where is data stored?
data_dir = '../data/'

# intermediates
tribune_file = os.path.join(data_dir, 'tribune.tsv')
sinclair_file = os.path.join(data_dir, 'sinclair.tsv')
nexstar_file = os.path.join(data_dir, 'nexstar.tsv')
meredith_file = os.path.join(data_dir, 'meredith.tsv')
hearst_file = os.path.join(data_dir, 'hearst.tsv')
stationindex_file = os.path.join(data_dir, 'station_index.tsv')
usnpl_file = os.path.join(data_dir, 'usnpl.tsv')

# this is where user entries go!
custom_station_file = os.path.join(data_dir, 'custom_additions.json')

# this is the output!
local_news_dataset_file  = os.path.join(data_dir, 'local_news_dataset_2018.csv') 

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# variables
today = datetime.datetime.now()
version = 0



# for normalizing station info.
owner_mapping = {
    'Meredith Corporation' : 'Meredith',
    'Sinclair Broadcast Group' : 'Sinclair',
    'Nexstar Media Group' : 'Nexstar',
    'Hearst Television' : 'Hearst'
}

station_index_mapping = {
    'owner' : 'broadcaster'
}

national = [
    'comettv.com',
    'tbn.org',
    'iontelevision.com',
    'tct-net.org',
    'sbgi.net',
    'daystar.com',
]

look_up = {' Honolulu' : 'HI',
 ' Kalamazoo. MI' : 'MI',
' San Antonio' : 'TX'}

col_standard = {
    'station' : 'name',
    'twitter_name' : 'twitter',
    'geography' : 'state',
    'broadcaster' : 'owner'
}

cols_standard_nexstar = {
    'Web Site' : 'website',
    'Station' : 'station',
    'Affiliation' : 'network'
} 

cols_nexstar = ['station', 'website', 'city', 'state', 'broadcaster', 'source']

cols = ['name', 'state', 'website', 'twitter', 'youtube', 'facebook', 'owner', 'medium', 'source', 'collection_date']
cols_final = ['name', 'state', 'website', 'domain', 'twitter', 'youtube', 'facebook', 'owner', 'medium', 'source', 'collection_date']

# to align nexstar websites to station names
nexstar_alignment = {

    'krqe.com' : [
        'KRQE',
        'KBIM',
        'KREZ',
    ],

    'kwbq.com' : [
        'KWBQ',
        'KASY',
        'KRWB'
    ] ,

    'kark.com' : [
        'KARK',
        'KARZ'
    ],

    'fox16.com' : [
        'KLRT'
    ],

    'cwarkansas.com' : [
        'KASN '
    ],

    'woodtv.com' : [
        'WOOD',
    ],

    'wotv4women.com' : [
        'WOTV',
        'WXSP-CD'

    ],
    
    'wkbn.com' : [
        'WKBN'
    ],
    
    'wytv.com' : [
        'WYTV',
        'WYFX-LD'
    ]  
}

# for USNPL
states = '''ak	  al	  ar	  az	  ca	  co	  ct	  dc	  de	  fl	  ga	  hi	  ia	  id	  il	  in	  ks   ky	  la	  ma	  md	  me	  mi	  mn	  mo	  ms	  mt	  nc	  nd	  ne	  nh	  nj	  nm	  nv	  ny	  oh	  ok	  or	  pa	  ri	  sc	  sd	  tn	  tx	  ut	  va	  vt	  wa	  wi	  wv	  wy	'''
states = [s.strip() for s in states.split('  ')]

# for stationindex
city_state = {
    'New York' : 'NY',
    'Los Angeles' : 'CA',
    'Chicago' : 'IL',
    'Philadelphia' : 'PA',
    'Dallas' : 'TX',
    'Washington, D.C.' : 'DC',
    'Houston' : "TX",
    'Seattle' : 'WA',
    'South Florida' : 'FL',
    'Denver' : 'CO',
    'Cleveland': 'OH',
    'Sacramento' : 'CA',
    'San Diego' : 'CA',
    'St. Louis' : 'MO',
    'Portland' : 'OR',
    'Indianapolis' : 'IN',
    'Hartford' :'CT',
    'Kansas City' :'MO',
    'Salt Lake City' : 'UT',
    'Milwaukee' : 'WI',
    'Waterbury' : 'CT',
    'Grand Rapids' : 'MI',
    'Oklahoma City': 'OK',
    'Harrisburg' : 'VA',
    'Norfolk' : 'VA',
    'Greensboro/High Point/Winston-Salem' : 'NC',
    'Memphis' : 'TN',
    'New Orleans' : 'LA',
    'Wilkes-Barre/Scranton' : 'PA',
    'Richmond' : 'VA',
    'Des Moines' : 'IL',
    'Huntsville' : 'AL',
    'Moline, IL / Davenport, IA' : "IL/IA",
    'Fort Smith' : "AK",
    'America' : 'National'
}

not_actually_local = [
    'variety.com', 'investors.com', 'hollywoodreporter.com', 'bizjournals.com'
]