from imdb import IMDb
from bs4 import BeautifulSoup
from textblob import TextBlob
import requests
from datetime import datetime
import json
import re

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


def get_imdb_reviews(movie_id):
    url = f"https://www.imdb.com/title/{movie_id}/reviews"
    response = requests.get(url)
    reviews = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        review_elements = soup.find_all('div', class_='review-container')
        for element in review_elements:
            review_text = element.find('div', class_='text show-more__control').get_text().strip()
            review_date = datetime.strptime(element.find('span', class_='review-date').get_text(), '%d %B %Y')
            reviews.append((review_text, review_date))
    return reviews

def analyze_sentiments(reviews):
    polarities = [TextBlob(review[0]).sentiment.polarity for review in reviews]
    subjectivities = [TextBlob(review[0]).sentiment.subjectivity for review in reviews]

    avg_polarity = sum(polarities) / len(polarities) if polarities else 0
    avg_subjectivity = sum(subjectivities) / len(subjectivities) if subjectivities else 0

    return avg_polarity, avg_subjectivity

# Remplacez 'tt0111161' par l'ID du film souhaité
movie_id = 'tt0111161'
release_date = get_movie_release_date(movie_id[2:])

reviews = get_imdb_reviews(movie_id)
before_release = [review for review in reviews if review[1] < release_date]
after_release = [review for review in reviews if review[1] >= release_date]

sentiment_before, subjectivity_before = analyze_sentiments(before_release)
sentiment_after, subjectivity_after = analyze_sentiments(after_release)

print(f"Moyenne des sentiments avant la sortie : {sentiment_before}")
print(f"Moyenne de la subjectivité avant la sortie : {subjectivity_before}")
print(f"Moyenne des sentiments après la sortie : {sentiment_after}")
print(f"Moyenne de la subjectivité après la sortie : {subjectivity_after}")
