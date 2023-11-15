import requests
import json
import pandas as pd

with open('clefAPI.json', 'r') as config_file:
    config = json.load(config_file)

api_key = config['tmdb']['api_key']
access_token = config['tmdb']['access_token']

base_url = "https://api.themoviedb.org/3/"
discover_url = f"{base_url}discover/movie?api_key={api_key}&primary_release_year=2022"

response = requests.get(discover_url)

movies_dict = {}
movies_list = []

start_date = "2022-01-01"
end_date = "2022-12-31"

initial_url = f"{base_url}discover/movie?api_key={api_key}&primary_release_date.gte={start_date}&primary_release_date.lte={end_date}&region=FR"
initial_response = requests.get(initial_url)

if initial_response.status_code == 200:
    total_pages = initial_response.json()['total_pages']
    for page in range(1, total_pages + 1):
        discover_url = f"{initial_url}&page={page}"
        response = requests.get(discover_url)
        
        if response.status_code == 200:
            movies_data = response.json()['results']
            for movie in movies_data:
                title = movie.get("title", "Titre Inconnu")
                release_date = movie.get("release_date", "Date Inconnue")
                movies_list.append({'Title': title, 'Release Date': release_date})
        else:
            print("Erreur lors de la requête :", response.status_code)
            break
else:
    print("Erreur lors de la requête initiale :", initial_response.status_code)

movies_df = pd.DataFrame(movies_list)

print(movies_df.head())
print("Le nb de page est de :",total_pages)
print("Le nb de film extrait est de :",len(movies_df))
print("Le nb de film unique est de :",len(movies_df['Title'].unique()))

