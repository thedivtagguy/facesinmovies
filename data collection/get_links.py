###############################################################
#                                                             #
# Python script to download all the posters from the TMDB API #
# Based on the IMDB id of the movie, and then store details   #
# in a csv file.                                              #
#                                                             #
# Script Adapted from https://gist.github.com/baderj/7414775  #
#                                                             #
###############################################################


import os
from dotenv import load_dotenv
import requests

load_dotenv()
# Get TMDB_API_KEY from .env file
KEY = os.getenv('TMDB_KEY')
CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}' 
IMAGES = "./posters/"
def _get_json(url):
    r = requests.get(url)
    return r.json()
    
def _download_images(urls, path='.'):
    """download all images in list 'urls' to 'path' """

    for nr, url in enumerate(urls):
        r = requests.get(url)
        filetype = r.headers['content-type'].split('/')[-1]
        filename = 'poster_{0}.{1}'.format(nr+1,filetype)
        filepath = os.path.join(path, filename)
        # Download only if file is jpeg jpg or png
        if filetype in ['jpeg', 'jpg', 'png']:
            with open(filepath,'wb') as w:
                w.write(r.content)

def get_poster_urls(imdbid):
    """ return image urls of posters for IMDB id
        returns all poster images from 'themoviedb.org'. Uses the
        maximum available size. 
        Args:
            imdbid (str): IMDB id of the movie
        Returns:
            list: list of urls to the images
    """
    config = _get_json(CONFIG_PATTERN.format(key=KEY))
    print(config['change_keys'][6])
    base_url = config['images']['base_url']
    sizes = config['images']['poster_sizes']
    """
        'sizes' should be sorted in ascending order, so
            max_size = sizes[-1]
        should get the largest size as well.        
    """
    def size_str_to_int(x):
        return float("inf") if x == 'original' else int(x[1:])
    max_size = max(sizes, key=size_str_to_int)

    posters = _get_json(IMG_PATTERN.format(key=KEY,imdbid=imdbid))['posters']
    poster_urls = []
    count = 0
    for poster in posters:
        rel_path = poster['file_path']
        url = "{0}{1}{2}".format(base_url, max_size, rel_path)
        poster_urls.append(url) 

    return poster_urls

    
def tmdb_posters(imdbid, count=None, outpath='.'):    
    urls = get_poster_urls(imdbid)
    # Choose 10 random posters from the list
    # if count is None:
    #     count = 10
    # urls = urls[:count]
    # _download_images(urls, outpath)



tmdb_posters('tt1160419')