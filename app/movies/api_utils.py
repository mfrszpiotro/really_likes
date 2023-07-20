import requests
from app.movies.models import Movie
from unidecode import unidecode

def eliminate_duplicates(list_of_dicts, key):
    unique_dicts = []
    keys_set = set()

    for dictionary in list_of_dicts:
        if dictionary[key] not in keys_set:
            keys_set.add(dictionary[key])
            unique_dicts.append(dictionary)

    return unique_dicts

def get_movie_details(id):
    url = "https://api.themoviedb.org/3/movie/{}".format(id)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYmYxODNiNTU4NTk1NTAxMDU3YzRmZGNiMjdkZjM5YiIsInN1YiI6IjY0YTAyYTI0ZDUxOTFmMDBlMjYzOTRjMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.auBno1g8lHhknr7TwBMTGMNvsYBqViqJ3nJNK05HN0E",
    }
    response = requests.get(url, headers=headers)
    content = response.json()
    return content["release_date"][0:4], content["runtime"]


def init_movies(database):
    url = "https://api.themoviedb.org/3/person/40239/movie_credits?language=cz-CZ"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYmYxODNiNTU4NTk1NTAxMDU3YzRmZGNiMjdkZjM5YiIsInN1YiI6IjY0YTAyYTI0ZDUxOTFmMDBlMjYzOTRjMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.auBno1g8lHhknr7TwBMTGMNvsYBqViqJ3nJNK05HN0E",
    }
    response = requests.get(url, headers=headers)
    url_content = response.json()
    for appear in eliminate_duplicates(url_content.get("cast", []), "title"):
        details = get_movie_details(appear.get("id"))
        movie = Movie(
            seen="no",
            orig_title=appear.get("original_title", ""),
            name=appear.get("title", ""),
            search=unidecode(appear.get("original_title", "")).strip().casefold(),
            img=appear.get("poster_path", "missing.jpg"),
            appear_type="cast",
            job=appear.get("job", ""),
            descr="Natka chyba jeszcze nie oglądała tego filmu!",
            year=details[0],
            runtime=details[1],
        )
        database.session.add(movie)
    for appear in eliminate_duplicates(url_content.get("crew", []), "title"):
        if not appear.get("original_title", "") == "Já truchlivý bůh":
            details = get_movie_details(appear.get("id"))
            movie = Movie(
                seen="no",
                orig_title=appear.get("original_title", ""),
                name=appear.get("title", ""),
                search=unidecode(appear.get("original_title", "")).strip().casefold(),
                img=appear.get("poster_path", "missing.jpg"),
                appear_type="crew",
                job=appear.get("job", ""),
                descr="Natka chyba jeszcze nie oglądała tego filmu!",
                year=details[0],
                runtime=details[1],
            )
            database.session.add(movie)
    database.session.commit()