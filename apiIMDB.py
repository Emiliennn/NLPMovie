from imdb import IMDb

# Créer une instance de IMDb
ia = IMDb()

# Rechercher un film par son titre
movie_title = "The Shawshank Redemption"
search_results = ia.search_movie(movie_title)

if search_results:
    movie = search_results[0]  # Prendre le premier résultat
    ia.update(movie)

    # Afficher toutes les clés disponibles
    print(movie.keys())

    # Tenter d'afficher la date de sortie
    release_date_key = 'release date'  # Vous devrez peut-être ajuster cette clé
    if release_date_key in movie:
        print(f"Date de sortie: {movie[release_date_key]}")
    else:
        print("Date de sortie non trouvée")
else:
    print("Film non trouvé")
