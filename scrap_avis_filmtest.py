import requests
from bs4 import BeautifulSoup

# ID du film sur IMDb
film_id = 'tt0111161'  # Exemple avec "The Shawshank Redemption"

# URL de la page des avis sur IMDb
url = f"https://www.imdb.com/title/{film_id}/reviews"

# Faire la requête HTTP
response = requests.get(url)

# Initialiser un dictionnaire pour stocker les avis et leurs dates
reviews_dict = {}

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    # Rechercher les éléments contenant les avis et les dates
    review_elements = soup.find_all('div', class_='review-container')
    for element in review_elements:
        review = element.find('div', class_='text show-more__control').get_text().strip()
        # La date peut être trouvée dans un autre élément, à identifier
        # Par exemple, si la date est dans un élément ayant la classe 'review-date'
        review_date = element.find('span', class_='review-date').get_text().strip()
        reviews_dict[review] = review_date
else:
    print("Erreur lors de la requête :", response.status_code)

# Affichage du dictionnaire des avis
for review, date in reviews_dict.items():
    print(f"Avis (publié le {date}): {review}\n")
