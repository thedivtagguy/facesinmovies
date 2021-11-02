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
import random

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
        Args:
            imdbid (str): IMDB id of the movie
        Returns:
            list: list of urls to the images
    """
    config = _get_json(CONFIG_PATTERN.format(key=KEY))
    print(config['change_keys'][6])
    base_url = config['images']['base_url']
   
    posters = _get_json(IMG_PATTERN.format(key=KEY,imdbid=imdbid))['posters']
    poster_urls = []

    for poster in posters:
        rel_path = poster['file_path']
        url = "{0}{1}{2}".format(base_url, 'w342', rel_path)
        poster_urls.append(url) 
    
    # choose 10 random posters
    print(len(poster_urls))
    poster_urls = random.sample(poster_urls, 20)
    return poster_urls


# Get the movie name
def get_details(imdbid):
    base_url = 'https://api.themoviedb.org/3/movie/{imdbid}?api_key={api_key}'
    details = _get_json(base_url.format(imdbid=imdbid, api_key=KEY))
    genres = [genre['name'] for genre in details['genres']]
    title = details['title']
    imdb_id = details['imdb_id']
    country = details['production_countries'][0]['name']
    language = details['original_language']
    release_date = details['release_date']
    production_companies = [company['name'] for company in details['production_companies']]
    runtime = details['runtime']
    overview = details['overview']
    return {'title': title, 'genres': genres, 'imdb_id': imdb_id, 'country': country, 'language': language, 'release_date': release_date, 'production_companies': production_companies, 'runtime': runtime, 'overview': overview}


def tmdb_posters(imdbid, count=None):    
    urls = get_poster_urls(imdbid)
    movie = get_details(imdbid)
    outpath = ""
    # Create a folder for the movie
    if not os.path.exists(IMAGES + movie['title']):
        os.makedirs(IMAGES + movie['title'])
    outpath = IMAGES + movie['title'] + "/"
    _download_images(urls, outpath)

# Create a CSV containing details of all movies
def create_csv(movies):
    with open('movies.csv', 'w') as f:
        for movie in movies:
            f.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}\n".format(movie['title'], movie['genres'], movie['imdb_id'], movie['country'], movie['language'], movie['release_date'], movie['production_companies'], movie['runtime'], movie['overview'], movie['poster_urls'], movie['backdrop_urls']))


tmdb_posters('tt1160419')
dune= get_details('tt1160419')
create_csv(dune)
