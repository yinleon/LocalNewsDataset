# LOCAL NEWS OUTLET DATASET
By Leon Yin<br>
On 2018-05-31

## Introduction
There are no readily machine-readible lists of state-level news organizations that I was satisfied with. In order to change that, I wrote several scripts to download and merge local newspapers (from usnpl.com), and TV stations (from stationindex.com, and several sites from leading media organizations: including Meridith corp, Sinclair broadcasting group, Nexstar media group, Tribune media, and Hearst).

This project is intended to be a starting point for analysis regarding local news. There are often outlets that these sources missed. To accomidate this, there is [json file]() in config that one can make additions to. If there are domains I am missing, please submit an issue or send me a message at @leonyin.


## How is this Repo Organized?
The `nbs` directory has Jupyter Notebooks used to develop the python scripts found in `py`.
In addition to the state and name of each media outlet, I also collect their web domain and social (Twitter, Facebook, Youtube) IDs where available.

## Methodology
Several websites are [scraped]() using the requests and beautifulsoup Python packages. The column names are then normalized, and [merged]().

## Gotchas
There can be several entires with the same domain.<br>
Why? Certain city-level publications are subdomains of larger state-level sites.

## Acknowldegements
I'd like to acknowledge the work of usnpl, and tvstation index for compiling the majoroty of local news outlets used in this project.