import requests
import json
from dotenv import load_dotenv
import os
from imdb import IMDb

ia = IMDb()

load_dotenv()
KEY = os.getenv("TMDB_KEY")
request_url = "https://api.themoviedb.org/3/discover/movie?api_key={KEY}&sort_by=popularity.desc&include_adult=true&include_video=false&page=2&year=2021&vote_count.gte=100&with_watch_monetization_types=flatrate".format(KEY=KEY)
total_pages = 1
movies = {}
# Scrape the data from the API
for page in range(1, total_pages + 1):
     response = requests.get(request_url.format(page=page))
     data = json.loads(response.text)
     # Add to movies dictionary
     for movie in data['results']:
          # Search for movie on IMDB
          imdb_movie = ia.search_movie(movie['title'])
          print("Scrapping {movie}".format(movie=movie['title']))
          # Get movie id
          imdb_movie_id = imdb_movie[0].movieID
          # Add to dictionary
          movies[imdb_movie_id] = movie

print("Finished Scrapping")

# Convert movies dictionary to dataframe
import pandas as pd
df = pd.DataFrame.from_dict(movies, orient='index')
# Save df to csv
df.to_csv('data/imdb.csv')
print("Finished Saving")
