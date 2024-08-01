import pandas as pd
import requests
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv('api_key.env')
tmdb_api_key = os.getenv('TMDB_API_KEY')

detailed_movies = []

def get_page_details(page_number):
    tmdb_discover_url = f'https://api.themoviedb.org/3/discover/movie?api_key={tmdb_api_key}&page={page_number}'
    response = requests.get(tmdb_discover_url)
    if response.status_code == 200:
        return response.json().get('results', [])

def get_movie_details(page_number):
    movies = get_page_details(page_number)
    for movie in movies:
        movie_id = movie['id']
        tmdb_movie_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}'
        response = requests.get(tmdb_movie_url)
        if response.status_code == 200:
            detailed_movies.append(response.json())

for page in range(1,2):
    get_movie_details(page)

df = pd.DataFrame(detailed_movies)
df.to_csv('detailed_movies.csv', index=False)

