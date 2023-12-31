from imdb import IMDb
from bs4 import BeautifulSoup
from textblob import TextBlob
import requests
from datetime import datetime
import json
import re
import pandas as pd
#import nltk
# pip install -U textblob-fr # pour installer le package français

############ API TMDb #####################

with open('clefAPI.json', 'r') as config_file:
    config = json.load(config_file)

api_key = config['tmdb']['api_key']

############ Fonctions #####################

# la fonction get_movie_release_date() prend en paramètre l'ID IMDb d'un film et retourne sa date de sortie

def get_movie_release_date(movie_id):
    ia = IMDb()
    movie = ia.get_movie(movie_id)
    if 'original air date' in movie:
        release_date_str = movie['original air date']
        match = re.search(r'(\d{2} \w{3} \d{4})', release_date_str)
        if match:
            date_str = match.group(1)
            return datetime.strptime(date_str, '%d %b %Y')
    return None

# la fonction get_movies_between_dates() prend en paramètre deux dates au format YYYY-MM-DD et 
# retourne une liste de tuples contenant l'ID et le titre des films sortis entre ces deux dates

def get_movies_between_dates(start_date, end_date, api_key):
    base_url = "https://api.themoviedb.org/3/discover/movie"
    url = f"{base_url}?api_key={api_key}&primary_release_date.gte={start_date}&primary_release_date.lte={end_date}&region=FR"
    response = requests.get(url)
    if response.status_code == 200:
        movies_data = response.json()['results']
        return [(movie['id'], movie['title']) for movie in movies_data]
    else:
        print("Erreur lors de la requête :", response.status_code)
        return []
    
# la fonction get_imdb_reviews() prend en paramètre l'ID IMDb d'un film et 
# retourne une liste de tuples contenant le texte et la date de chaque avis

def get_imdb_reviews(movie_id): # FONCTIONNE
    url = f"https://www.imdb.com/title/{movie_id}/reviews"
    response = requests.get(url)
    reviews = {}
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        review_elements = soup.find_all('div', class_='review-container')
        if not review_elements:
            print(f"Aucune critique trouvée pour {movie_id}")
            return reviews
        for element in review_elements:
            review_text = element.find('div', class_='text show-more__control').get_text().strip()
            review_date = datetime.strptime(element.find('span', class_='review-date').get_text(), '%d %B %Y')
            reviews[review_date] = review_text
    else:
        print(f"Erreur lors de la récupération des avis pour {movie_id}: {response.status_code}")
    return reviews

def get_movies_with_imdb_id(start_date, end_date, api_key):
    base_url = "https://api.themoviedb.org/3/discover/movie"
    url = f"{base_url}?api_key={api_key}&primary_release_date.gte={start_date}&primary_release_date.lte={end_date}&region=FR"
    response = requests.get(url)
    if response.status_code == 200:
        movies_data = response.json()['results']
        return [(movie['id'], movie['imdb_id'], movie['title']) for movie in movies_data if 'imdb_id' in movie]
    else:
        print("Erreur lors de la requête :", response.status_code)
        return []

# la fonction process_movies() prend en paramètre une liste d'identifiants de films et retourne une liste de dictionnaires contenant les informations suivantes :
# - ID du film
# - Sentiment moyen des avis après la sortie du film
# - Subjectivité moyenne des avis après la sortie du film
# - Date de sortie du film
# - Nombre d'avis sur IMDb

def analyze_sentiments(reviews):
    polarities = [TextBlob(review[0]).sentiment.polarity for review in reviews]
    subjectivities = [TextBlob(review[0]).sentiment.subjectivity for review in reviews]

    avg_polarity = sum(polarities) / len(polarities) if polarities else 0
    avg_subjectivity = sum(subjectivities) / len(subjectivities) if subjectivities else 0

    return avg_polarity, avg_subjectivity

def process_movies(movie_ids):
    results = []
    for movie_id in movie_ids:
        release_date = get_movie_release_date(str(movie_id))
        reviews = get_imdb_reviews('tt' + str(movie_id))
        after_release = [review for review in reviews if review[1] >= release_date]
        sentiment_after, subjectivity_after = analyze_sentiments(after_release)
        results.append({'Movie ID': movie_id, 'Sentiment After': sentiment_after, 'Subjectivity After': subjectivity_after, 'Release Date': release_date, 'Nb avis': len(reviews)})
    return results



############# Main #####################

start_date = "2022-01-01"
end_date = "2022-01-31"

# RAPPEL : PB DE DATES !!

movies = get_movies_with_imdb_id(start_date, end_date, api_key)
results = process_movies([movie[0] for movie in movies])
results_df = pd.DataFrame(results)

#print(results_df)

movie_id = 'tt0111161'
#tt2098632 batman
release_date = get_movie_release_date(movie_id[2:])

reviews = get_imdb_reviews(movie_id)
before_release = [review for review in reviews if review[1] < release_date]
after_release = [review for review in reviews if review[1] >= release_date]

sentiment_before, subjectivity_before = analyze_sentiments(before_release)
sentiment_after, subjectivity_after = analyze_sentiments(after_release)

#print(f"Moyenne des sentiments avant la sortie : {sentiment_before}")
#print(f"Moyenne de la subjectivité avant la sortie : {subjectivity_before}")
#print(f"Moyenne des sentiments après la sortie : {sentiment_after}")
#print(f"Moyenne de la subjectivité après la sortie : {subjectivity_after}")

#print(get_movie_release_date('0111161'))
#print(get_imdb_reviews('tt0111161'))

# Récupérer les avis sur IMDb de get_imdb_reviews pour l'id tt0111161

for review_date, review_text in reviews.items():
    # afficher de maniere claire les avis (date et texte)
    print(f"{review_date}: {review_text}\n")
    
    







