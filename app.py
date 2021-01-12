from typing import List
import datetime
import db

db.create_tables()


def prompt_add_movie():
    title = input("Movie Title: ")
    release_date = input("Release date (dd-mm-YYYY): ")
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    timestamp = parsed_date.timestamp()

    db.add_movie(title, timestamp)


def prompt_watch_movie():
    username = input("Who watched the movie?: ")
    movie_id = input("Movie ID: ")
    db.watch_movies(username, movie_id)


def prompt_search_movie():
    pattern = input("Enter the partial movie title: ")
    movies = db.search_movie(pattern)
    if movies:
        print_movies("FOUND", movies)
    else:
        print(f"Didn't find any movie that match the pattern: {pattern}")


def print_movies(header: str, movies: List):
    # Indexes
    ID = 0
    TITLE = 1
    TIMESTAMP = 2

    print(f"--- {header} MOVIES ---")
    for movie in movies:
        movie_date = datetime.datetime.fromtimestamp(movie[TIMESTAMP])
        human_date = movie_date.strftime("%d-%b-%Y")
        print(f"{movie[ID]}: {movie[TITLE]} (on {human_date})")
    print("---\n")


welcome = "WELCOME TO THE WATCHLIST APP\n\n"

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies.
4) Watch a movie.
5) View watched movies.
6) Add new user.
7) Search Movie.
8) Exit.

Your selection: """

print(welcome)

while (user_input := input(menu)) != "8":
    if user_input == "1":
        prompt_add_movie()

    elif user_input == "2":
        movies = db.get_movies(upcoming=True)
        print_movies("UPCOMING", movies)

    elif user_input == "3":
        movies = db.get_movies(upcoming=False)
        print_movies("ALL", movies)

    elif user_input == "4":
        prompt_watch_movie()

    elif user_input == "5":
        username = input("Username: ")
        movies = db.get_watched_movies(username)
        if movies:
            print_movies(username, movies)
        else:
            print(f"{username} didn't watch any movie yet\n")

    elif user_input == "6":
        username = input("New user: ")
        db.add_user(username)

    elif user_input == "7":
        prompt_search_movie()

    else:
        print("Invalid input, try again")
