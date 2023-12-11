import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from datetime import datetime
import json

# package NTLK en plus de TextBlob

with open('clefAPI.json', 'r') as config_file:
    config = json.load(config_file)

api_key = config['tmdb']['api_key']

film_id = 'tt0111161'  
#tt0111161 # Exemple avec "The Shawshank Redemption"
# 899082 # Harry potter 20 ans après

# Récupérer la date de sortie du film depuis TMDb API
url_date_release = f"https://api.themoviedb.org/3/movie/{film_id}?api_key={api_key}&language=en-US"
response = requests.get(url_date_release)

if response.status_code == 200:
    film_details = response.json()
    date_sortie_str = film_details.get("release_date", "")
    if date_sortie_str:
        date_sortie = datetime.strptime(date_sortie_str, "%Y-%m-%d")
        print(f"Date de sortie du film : {date_sortie}")
    else:
        print("Date de sortie non trouvée")
else:
    print("Erreur lors de la requête :", response.status_code)

# Récupérer les avis sur IMDb
url_film = f"https://www.imdb.com/title/{film_id}/reviews"

response = requests.get(url_film)

reviews_dict = {}

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    review_elements = soup.find_all('div', class_='review-container')
    for element in review_elements:
        review_text = element.find('div', class_='text show-more__control').get_text().strip()
        review_date_str = element.find('span', class_='review-date').get_text().strip()
        review_date = datetime.strptime(review_date_str, '%d %B %Y').date()
        reviews_dict[review_date] = review_text
else:
    print("Erreur lors de la requête :", response.status_code)

print("Nb d'avis pour ce film :",len(reviews_dict))


# Classer les avis en fonction de la date de sortie du film


for key, review in reviews_dict.items():
    blob = TextBlob(review)
    sentiment = blob.sentiment
    print(f"{key}: Sentiment polarity = {sentiment.polarity}, Sentiment Subjectivity = {sentiment.subjectivity}")
    
avis_avant = {}
avis_apres = {}

for review_date, review_text in reviews_dict.items():
    if review_date < date_sortie.date():
        avis_avant[review_date] = review_text
    else:
        avis_apres[review_date] = review_text

# print("Avis Avant la Sortie:")
# for date, review in avis_avant.items():
#     print(f"{date}: {review}\n")

print("Avis Après la Sortie:")
for date, review in avis_apres.items():
    print(f"{date}: {review}\n")
#print("avis_apres", avis_apres)