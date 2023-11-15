import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from datetime import datetime

# package NTLK en plus de TextBlob

# ID du film sur IMDb
film_id = 'tt0111161'  # Exemple avec "The Shawshank Redemption"

date_sortie = datetime(1994, 9, 23)

# URL de la page des avis sur IMDb
url = f"https://www.imdb.com/title/{film_id}/reviews"

# Faire la requête HTTP
response = requests.get(url)

# Initialiser un dictionnaire pour stocker les avis et leurs dates
reviews_dict = {}

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    review_elements = soup.find_all('div', class_='review-container')
    for element in review_elements:
        review_text = element.find('div', class_='text show-more__control').get_text().strip()
        review_date = element.find('span', class_='review-date').get_text().strip()
        reviews_dict[f"Avis du {review_date}"] = review_text
else:
    print("Erreur lors de la requête :", response.status_code)

# Affichage du dictionnaire des avis
# for date, review in reviews_dict.items():
#     print(f"{date}: {review}\n")
    

print("Nb d'avis pour ce film :",len(reviews_dict))

for key, review in reviews_dict.items():
    blob = TextBlob(review)
    sentiment = blob.sentiment
    print(f"{key}: Sentiment = {sentiment.polarity}, Subjectivity = {sentiment.subjectivity}")
    
avis_avant = {}
avis_apres = {}

for key, review in reviews_dict.items():
    # Extraire la date de l'avis directement de la clé
    date_avis_str = key.replace("Avis du ", "")
    try:
        date_avis = datetime.strptime(date_avis_str, '%d %B %Y')
        if date_avis < date_sortie:
            avis_avant[key] = review
        else:
            avis_apres[key] = review
    except ValueError:
        print(f"Erreur de conversion de date pour: {key}")

# Afficher les résultats
print("Avis Avant la Sortie:")
for date, review in avis_avant.items():
    print(f"{date}: {review}\n")

print("Avis Après la Sortie:")
for date, review in avis_apres.items():
    print(f"{date}: {review}\n")
