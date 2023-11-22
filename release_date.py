import re
from datetime import datetime
from imdb import IMDb

def get_movie_release_date(movie_id):
    ia = IMDb()
    movie = ia.get_movie(movie_id)
    if 'original air date' in movie:
        release_date_str = movie['original air date']
        # Utilisation d'une expression régulière pour extraire la date
        match = re.search(r'(\d{2} \w{3} \d{4})', release_date_str)
        if match:
            date_str = match.group(1)
            return datetime.strptime(date_str, '%d %b %Y')
    return None

# Exemple d'utilisation
movie_id = '0111161'  # ID IMDb sans "tt"
release_date = get_movie_release_date(movie_id)
print(f"Date de sortie: {release_date}")
