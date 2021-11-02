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
    try:
        for nr, url in enumerate(urls):
            r = requests.get(url)
            filetype = r.headers['content-type'].split('/')[-1]
            filename = 'poster_{0}.{1}'.format(nr+1,filetype)
            filepath = os.path.join(path, filename)
            # Download only if file is jpeg jpg or png
            if filetype in ['jpeg', 'jpg', 'png']:
                with open(filepath,'wb') as w:
                    w.write(r.content)
    except Exception as e:
        print(e)
    

def get_poster_urls(imdbid):
    """ return image urls of posters for IMDB id
        Args:
            imdbid (str): IMDB id of the movie
        Returns:
            list: list of urls to the images
    """
    try:
        config = _get_json(CONFIG_PATTERN.format(key=KEY))
        base_url = config['images']['base_url']
        
        posters = _get_json(IMG_PATTERN.format(key=KEY,imdbid=imdbid))['posters']
        poster_urls = []

        for poster in posters:
            rel_path = poster['file_path']
            url = "{0}{1}{2}".format(base_url, 'w342', rel_path)
            poster_urls.append(url) 
        
        # choose 10 or lesser random posters
        random.shuffle(poster_urls)
        return poster_urls
    except Exception as e:
        print(e)
        return []

# Get the movie name
def get_details(imdbid):
    base_url = 'https://api.themoviedb.org/3/movie/{imdbid}?api_key={api_key}'
    details = _get_json(base_url.format(imdbid=imdbid, api_key=KEY))
    try:
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
    except Exception as e:
        print(e)
        return {}


def tmdb_posters(imdbid, count=10):    
    try:
        urls = get_poster_urls(imdbid)
        movie = get_details(imdbid)
        print("Downloading for {movie}".format(movie = movie['title']))
        outpath = ""
        # Create a folder for the movie
        if not os.path.exists(IMAGES + movie['title'] +  " - " + movie['imdb_id']):
            os.makedirs(IMAGES + movie['title'] +  " - " + movie['imdb_id'])
        outpath = IMAGES + movie['title']  +  " - " + movie['imdb_id'] + "/"
        if count is not None:
            urls = urls[:count]
        _download_images(urls, outpath)
        print("------- Finished -------")
    except Exception as e:
        print(e)
        print("------- Failed -------")

ids = []
# Read in the IMDB ids from the IMDb movies.csv
with open('data/IMDB movies.csv', 'r', encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        ids.append(line.split(',')[0])

# Download posters for each movie
for imdbid in ids:
    tmdb_posters(imdbid)
