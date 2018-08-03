# LOCAL NEWS OUTLET DATASET
By Leon Yin<br>
On 2018-05-31

## Introduction
This dataset is a machine-readible directory of state-level newspapers, tv stations and magazines. In addition to basic information such as the name of the outlet and state it is located in, all available information regarding web presence, social media (twitter, youtube, facebook) and their owners is scraped, too.

The sources of this dataset are [usnpl.com](www.usnpl.com)-- newspapers and magazines by state, [stationindex.com](www.stationindex.com) -- tv stations by state and by owner, and homepages of the media corporations [Meredith](http://www.meredith.com/local-media/broadcast-and-digital), [Sinclair](http://sbgi.net/tv-channels/), [Nexstar](https://www.nexstar.tv/stations/), [Tribune](http://www.tribunemedia.com/our-brands/) and [Hearst](http://www.hearst.com/broadcasting/our-markets).

This dataset was inspired by Propublica's [Congress API](https://projects.propublica.org/api-docs/congress-api/). I hope that this dataset will serve a similar purpose as a starting point for research and applications, as well as a bridge between datasets from social media, news articles and online communities.

While you use this dataset, if you see irregularities, questionable entries, or missing outlets please [submit an issue](https://github.com/yinleon/LocalNewsDataset/issues/new) on Github or contact me on [Twitter](https://twitter.com/LeonYin). I'd love to hear how this dataset is put to work 

Happy hunting xo

For an indepth [introduction](https://nbviewer.jupyter.org/github/yinleon/LocalNewsDataset/blob/master/nbs/local_news_dataset.ipynb?flush_cache=true#intro), [specs](https://nbviewer.jupyter.org/github/yinleon/LocalNewsDataset/blob/master/nbs/local_news_dataset.ipynb?flush_cache=true#specs), [data sheet](https://nbviewer.jupyter.org/github/yinleon/LocalNewsDataset/blob/master/nbs/local_news_dataset.ipynb?flush_cache=true#datasheet), and [quickstart](https://nbviewer.jupyter.org/github/yinleon/LocalNewsDataset/blob/master/nbs/local_news_dataset.ipynb?flush_cache=true#use) check out this [Jupyter Notebook](https://nbviewer.jupyter.org/github/yinleon/LocalNewsDataset/blob/master/nbs/local_news_dataset.ipynb?flush_cache=true#datasheet) in `nbs/local_news_dataset.ipynb`.


## What's the data look like?
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>state</th>
      <th>website</th>
      <th>domain</th>
      <th>twitter</th>
      <th>youtube</th>
      <th>facebook</th>
      <th>owner</th>
      <th>medium</th>
      <th>source</th>
      <th>collection_date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>KWHE</td>
      <td>HI</td>
      <td>http://www.kwhe.com/</td>
      <td>kwhe.com</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>LeSea</td>
      <td>TV station</td>
      <td>stationindex</td>
      <td>2018-08-02 14:55:24.612585</td>
    </tr>
    <tr>
      <th>1</th>
      <td>WGVK</td>
      <td>MI</td>
      <td>http://www.wgvu.org/</td>
      <td>wgvu.org</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Grand Valley State University</td>
      <td>TV station</td>
      <td>stationindex</td>
      <td>2018-08-02 14:55:24.612585</td>
    </tr>
    <tr>
      <th>2</th>
      <td>KNIC-CD</td>
      <td>TX</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Univision</td>
      <td>TV station</td>
      <td>stationindex</td>
      <td>2018-08-02 14:55:24.612585</td>
    </tr>
  </tbody>
</table>

You can also browse the dataset on [Google Sheets](https://docs.google.com/spreadsheets/d/1f3PjT2A7-qY0SHcDW30Bc_FXYC_7RxnZfCKyXpoWeuY/edit?usp=sharing)<br>
Or look at the raw dataset on [Github](https://github.com/yinleon/LocalNewsDataset/blob/master/data/local_news_dataset_2018.csv)<br>
Or just browse the Jupyter Notebook's [tech specs](https://nbviewer.jupyter.org/github/yinleon/LocalNewsDataset/blob/master/nbs/local_news_dataset.ipynb?flush_cache=true#local_news_dataset_2018).


## How is this Repo Organized?
The `nbs` directory has exmaples of how to use this dataset. The dataset was created in Python. The scripts to re-create and update the dataset are in the `py` directory..
In addition to the state and name of each media outlet, I also collect their web domain and social (Twitter, Facebook, Youtube) IDs where available.

## Methodology
Several websites are [scraped]() using the requests and beautifulsoup Python packages. The column names are then normalized, and [merged]().

## Gotchas
There can be several entires with the same domain.<br>
Why? Certain city-level publications are subdomains of larger state-level sites.

## Acknowledgements
I'd like to acknowledge the work of the people behind usnpl.com and stationindex.com for compiling lists of local media outlets. Andreu Casas and Gregory Eady provided invaluable comments to improve this dataset for public release. I am funded and supported by the SMaPP Lab at NYU, thank you Josh Tucker, Jonathan Nagler, Richard Bonneau and my collegue Nicole Baram.

## Citation
If this dataset is helpful to you please cite it as:
```
@misc{Yin:2018
author = {Leon Yin},
title = {Local News Dataset},
year = {2018}
howpublished= {\url{https://github.com/yinleon/LocalNewsDataset}} 

```